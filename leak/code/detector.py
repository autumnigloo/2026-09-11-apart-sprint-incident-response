"""
Cross-run leak detector for agent evaluation sandboxes.

Pipeline:  transcript JSONL -> normalise -> char 5-gram shingles
        -> origination filter (subtract everything that entered the run's
           context before the span was emitted)
        -> convergence filter (drop shingles that >= COMMON_RUNS runs each
           originated on their own: shared skeletons are not evidence of a leak)
        -> exact shingle containment against every INGRESS entry of every other run
           (optional MinHash prefilter over sliding windows, for scale)
        -> hits + N x N cross-run matrix

Score semantics (both are reported per hit):
  containment = |window_shingles ∩ target_entry_shingles| / max(|window_shingles|, MIN_EVIDENCE)
      Answers "how much of the span reappears in this ingress entry", per 100-char
      source window, with the 40-shingle evidence floor as the denominator's lower bound.
      This is the right statistic when a short span is embedded in a larger
      tool output. It is the DEFAULT decision score.
  jaccard     = MinHash-estimated Jaccard between the span and the best-matching
      sliding window of the target entry. This is the handover's "Jaccard >= 0.7"
      config and is reported so both numbers appear in the PR sweep.

Usage:
    python detector.py runs/                       # scan all runs/agent-*/transcript.jsonl
    python detector.py runs/ --threshold 0.7 --out hits.json
    python detector.py runs/ --score jaccard
    python detector.py runs/ --no-origination      # ablation: skip the filter

Dependencies: numpy only. No network needed.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
import unicodedata
from dataclasses import dataclass, field, asdict

import numpy as np

# ----------------------------------------------------------------- config

K = 5                    # character shingle size
NUM_PERM = 128           # MinHash permutations
WINDOW = 200             # chars per target INGRESS window for the MinHash prefilter
STRIDE = 50              # target window stride
SRC_WINDOW = 100         # chars per source EGRESS window (~25 tokens): the smallest leak unit
SRC_STRIDE = 50          # source window stride
MIN_SHINGLES = 15        # spans with fewer originated shingles are ignored
MIN_EVIDENCE = 40        # containment denominator floor. A window that is mostly ingested
                         # text (echoed prompt, read-back) keeps only a handful of attributable
                         # shingles; with a raw denominator those few generic shingles score
                         # 1.0 against any run. 15 shingles fully matched now score 15/40.
                         # ~40% of a 100-char window is the smallest evidence worth a full score.
COMMON_RUNS = 2          # a shingle originated independently by >= this many runs is
                         # convergent boilerplate (import lines, __main__ guards) and is
                         # dropped from evidence. 0 disables.
PREFILTER_JACCARD = 0.2  # MinHash gate when --prefilter is on. OFF by default: a short
                         # leak inside a 200-char window has Jaccard ~ |leak|/|window|,
                         # so gating on Jaccard silently drops small leaks. Use it only
                         # for scale, and report the recall cost.


_ZW_CTRL = re.compile(r"[\u200b\u200c\u200d\u2060\ufeff]|[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
_WS = re.compile(r"[ \t\f\v]+")
_BLANKS = re.compile(r"\n{2,}")


# --------------------------------------------------------- normalisation

def normalise(text: str) -> str:
    """NFKC, strip zero-width/control chars, \\n line endings, collapse
    horizontal whitespace runs and blank-line runs. Case is PRESERVED."""
    if not text:
        return ""
    t = unicodedata.normalize("NFKC", text)
    t = t.replace("\r\n", "\n").replace("\r", "\n")
    t = _ZW_CTRL.sub("", t)
    t = _WS.sub(" ", t)
    t = "\n".join(line.strip() for line in t.split("\n"))
    t = _BLANKS.sub("\n", t)
    return t.strip()


# --------------------------------------------------------------- shingles

def _fnv1a32(s: str) -> int:
    """Stable 32-bit FNV-1a. Python's hash() is salted per process, which
    would make cached sketches non-comparable across invocations."""
    h = 0x811C9DC5
    for byte in s.encode("utf-8"):
        h ^= byte
        h = (h * 0x01000193) & 0xFFFFFFFF
    return h


def shingle_hashes(text: str, k: int = K) -> set[int]:
    """Set of stable 32-bit hashes of character k-grams over the normalised text."""
    t = normalise(text)
    if len(t) < k:
        return set()
    return {_fnv1a32(t[i:i + k]) for i in range(len(t) - k + 1)}


# ---------------------------------------------------------------- minhash

class MinHasher:
    """MinHash over NUM_PERM independent 64-bit hash functions.

    Each function is h_i(x) = splitmix64_finalizer(x XOR seed_i). A linear
    (a*x + b) mod p family is NOT used on purpose: with 32-bit inputs and
    a < 2^32 it never wraps for small x, so it is monotone on the smallest
    shingle hashes and the sketch degenerates to "min FNV value" (verified:
    Jaccard estimates of 0.8 on sets with true Jaccard 0.04)."""

    C1 = np.uint64(0xBF58476D1CE4E5B9)
    C2 = np.uint64(0x94D049BB133111EB)

    def __init__(self, num_perm: int = NUM_PERM, seed: int = 1):
        rng = np.random.RandomState(seed)
        self.seeds = rng.randint(0, 2**63 - 1, size=num_perm, dtype=np.int64).astype(np.uint64)
        self.num_perm = num_perm

    def sketch(self, hashes: set[int]) -> np.ndarray:
        if not hashes:
            return np.full(self.num_perm, np.iinfo(np.uint64).max, dtype=np.uint64)
        x = np.fromiter(hashes, dtype=np.uint64, count=len(hashes))
        with np.errstate(over="ignore"):
            z = x[None, :] ^ self.seeds[:, None]          # P x N
            z ^= z >> np.uint64(30); z *= self.C1
            z ^= z >> np.uint64(27); z *= self.C2
            z ^= z >> np.uint64(31)
        return z.min(axis=1)

    @staticmethod
    def jaccard(s1: np.ndarray, s2: np.ndarray) -> float:
        return float(np.mean(s1 == s2))


# ------------------------------------------------------------ transcripts

@dataclass
class Entry:
    idx: int
    ts: float
    role: str
    kind: str          # INGRESS | EGRESS
    content: str
    meta: dict


def load_transcript(path: pathlib.Path) -> list[Entry]:
    entries = []
    with open(path) as fh:
        for i, line in enumerate(fh):
            line = line.strip()
            if not line:
                continue
            d = json.loads(line)
            entries.append(Entry(i, d.get("ts", i), d.get("role", ""), d.get("kind", ""),
                                 d.get("content") or "", d.get("meta") or {}))
    return entries


# ------------------------------------------------------- span extraction

_HEREDOC = re.compile(
    r"<<-?\s*(['\"]?)(?P<tag>[A-Za-z_][A-Za-z0-9_]*)\1[^\n]*\n(?P<body>.*?)\n\s*(?P=tag)\s*$",
    re.S | re.M,
)
# the file being written appears either before the heredoc marker
# (cat > /work/x.py << 'EOF') or after it (cat << 'EOF' > /work/x.py)
_REDIRECT_TARGET = re.compile(r">>?\s*([^\s;&|<>]+)")

STRUCTURED_EXT = {".json", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".conf", ".env"}
CODE_EXT = {".py", ".sh", ".js", ".ts", ".c", ".cpp", ".go", ".rs", ".java", ".rb"}
PROSE_EXT = {".md", ".txt", ".rst"}


@dataclass
class Span:
    run: str
    entry_idx: int
    turn: int | None
    channel: str       # text | heredoc | bash_command
    artifact_type: str  # prose | code | structured | terse
    path: str | None
    text: str
    shingles: set[int] = field(default_factory=set, repr=False)
    originated: set[int] = field(default_factory=set, repr=False)
    sketch: np.ndarray | None = field(default=None, repr=False)
    # (offset, originated shingles, sketch, raw shingle count) for each source window
    windows: list = field(default_factory=list, repr=False)
    raw_n: int = 0
    full_ok: bool = False

    def public(self) -> dict:
        d = asdict(self)
        for k in ("shingles", "originated", "sketch", "windows"):
            d.pop(k, None)
        d["n_shingles"] = len(self.shingles)
        d["n_originated"] = len(self.originated)
        d["text"] = self.text[:200]
        return d


def classify_path(path: str | None, fallback: str) -> str:
    if not path:
        return fallback
    ext = pathlib.Path(path).suffix.lower()
    if ext in STRUCTURED_EXT:
        return "structured"
    if ext in CODE_EXT:
        return "code"
    if ext in PROSE_EXT:
        return "prose"
    return fallback


def extract_spans(run: str, e: Entry) -> list[Span]:
    """Split one EGRESS entry into spans.

    bash_command -> each heredoc body is its own span (typed by target file
    extension); the command with heredoc bodies removed is a 'terse' span.
    text         -> one 'prose' span.
    """
    spans = []
    channel = e.meta.get("channel", "text")
    turn = e.meta.get("turn")
    if channel == "bash_command":
        cmd = e.content
        residual = cmd
        for m in _HEREDOC.finditer(cmd):
            # the header is the command line that contains the << marker
            line_start = cmd.rfind("\n", 0, m.start()) + 1
            line_end = cmd.find("\n", m.start())
            header = cmd[line_start:line_end if line_end != -1 else len(cmd)]
            tm = _REDIRECT_TARGET.findall(header)
            path = tm[-1] if tm else None
            body = m.group("body")
            spans.append(Span(run, e.idx, turn, "heredoc",
                              classify_path(path, "code"), path, body))
            residual = residual.replace(body, "")
        if residual.strip():
            spans.append(Span(run, e.idx, turn, "bash_command", "terse", None, residual))
    else:
        spans.append(Span(run, e.idx, turn, "text", "prose", None, e.content))
    for s in spans:
        s.shingles = shingle_hashes(s.text)
    return spans


# -------------------------------------------------------------------- run

@dataclass
class Run:
    name: str
    entries: list[Entry]
    spans: list[Span]                     # originated EGRESS spans
    ingress: list[Entry]
    ingress_shingles: dict[int, set[int]]  # entry idx -> shingle set
    ingress_windows: list[tuple[int, int, set[int], np.ndarray]]  # (entry idx, offset, shingles, sketch)


def build_run(name: str, path: pathlib.Path, hasher: MinHasher,
              origination: bool = True) -> Run:
    entries = sorted(load_transcript(path), key=lambda e: (e.ts, e.idx))
    seen_ingress: set[int] = set()   # everything that entered context so far
    spans: list[Span] = []
    ingress_entries: list[Entry] = []
    ingress_shingles: dict[int, set[int]] = {}
    windows: list[tuple[int, int, set[int], np.ndarray]] = []

    for e in entries:
        if e.kind == "INGRESS":
            sh = shingle_hashes(e.content)
            seen_ingress |= sh
            ingress_entries.append(e)
            ingress_shingles[e.idx] = sh
            t = normalise(e.content)
            offsets = list(range(0, max(1, len(t) - WINDOW + 1), STRIDE))
            if len(t) > WINDOW and offsets[-1] != len(t) - WINDOW:
                offsets.append(len(t) - WINDOW)   # cover the tail
            for off in offsets:
                w = t[off:off + WINDOW]
                wsh = shingle_hashes(w)
                if len(wsh) >= MIN_SHINGLES:
                    windows.append((e.idx, off, wsh, hasher.sketch(wsh)))
        elif e.kind == "EGRESS":
            for s in extract_spans(name, e):
                # origination filter: only shingles never seen in INGRESS
                # *before this moment* are attributable to this run.
                s.originated = (s.shingles - seen_ingress) if origination else set(s.shingles)
                s.raw_n = len(s.shingles)
                full_ok = len(s.originated) >= MIN_SHINGLES
                # window the span so a partial copy (one function, one
                # paragraph) is still detectable against a long span
                t = normalise(s.text)
                for off in range(0, max(1, len(t) - SRC_WINDOW + 1), SRC_STRIDE):
                    raw = shingle_hashes(t[off:off + SRC_WINDOW])
                    wsh = (raw - seen_ingress) if origination else raw
                    if len(wsh) >= MIN_SHINGLES:
                        s.windows.append((off, wsh, hasher.sketch(wsh), len(raw)))
                if full_ok or s.windows:
                    s.full_ok = full_ok
                    s.sketch = hasher.sketch(s.originated) if s.originated else None
                    spans.append(s)
    return Run(name, entries, spans, ingress_entries, ingress_shingles, windows)


def common_shingles(runs: dict[str, "Run"], k: int = COMMON_RUNS) -> set[int]:
    """Shingles that appear in the ORIGINATED output of >= k distinct runs.
    A receiver of a leak ingests the text first, so its own copy is already
    removed by the origination filter; anything still originated by several
    runs was written independently by each (convergence), not transmitted."""
    if k <= 0:
        return set()
    count: dict[int, int] = {}
    for r in runs.values():
        seen = set()
        for s in r.spans:
            seen |= s.originated
        for h in seen:
            count[h] = count.get(h, 0) + 1
    return {h for h, c in count.items() if c >= k}


def apply_common(run: "Run", common: set[int], hasher: MinHasher) -> None:
    """Remove convergent shingles from every span and window; re-sketch."""
    if not common:
        return
    kept = []
    for s in run.spans:
        s.originated -= common
        s.full_ok = len(s.originated) >= MIN_SHINGLES
        s.sketch = hasher.sketch(s.originated) if s.originated else None
        new_w = []
        for off, wsh, _, raw_n in s.windows:
            wsh = wsh - common
            if len(wsh) >= MIN_SHINGLES:
                new_w.append((off, wsh, hasher.sketch(wsh), raw_n))
        s.windows = new_w
        if s.full_ok or s.windows:
            kept.append(s)
    run.spans = kept
    # prune target windows the same way so the reported Jaccard is like-for-like
    new_tw = []
    for eidx, off, wsh, _ in run.ingress_windows:
        wsh = wsh - common
        if len(wsh) >= MIN_SHINGLES:
            new_tw.append((eidx, off, wsh, hasher.sketch(wsh)))
    run.ingress_windows = new_tw


def load_runs(root: pathlib.Path, hasher: MinHasher, origination: bool = True,
              common_runs: int = COMMON_RUNS, common_ref: set[int] | None = None) -> dict[str, "Run"]:
    """Build every run under root, then apply the convergence filter.
    common_ref: pass a precomputed common set (e.g. from a larger solo corpus)
    instead of estimating it from these runs alone."""
    paths = discover_runs(root)
    runs = {n: build_run(n, p, hasher, origination) for n, p in paths.items()}
    common = common_ref if common_ref is not None else common_shingles(runs, common_runs)
    for r in runs.values():
        apply_common(r, common, hasher)
    return runs


def discover_runs(root: pathlib.Path) -> dict[str, pathlib.Path]:
    runs = {}
    for p in sorted(root.glob("*/transcript.jsonl")):
        runs[p.parent.name] = p
    if not runs and (root / "transcript.jsonl").exists():
        runs[root.name] = root / "transcript.jsonl"
    return runs


# --------------------------------------------------------------- scanning

@dataclass
class Hit:
    source_run: str
    target_run: str
    source_entry: int
    source_turn: int | None
    target_entry: int
    artifact_type: str
    channel: str
    path: str | None
    containment: float   # best source-window containment in the target entry
    coverage: float      # whole-span containment (how much of the span reappears)
    jaccard: float       # MinHash Jaccard, best source window vs best target window
    window_offset: int
    n_originated: int
    source_preview: str
    target_meta: dict


def scan_pair(src: Run, tgt: Run, hasher: MinHasher, prefilter: bool = False) -> list[Hit]:
    """Every originated span (and its windows) of src, checked against every
    INGRESS entry of tgt. One Hit per (span, target entry) with a nonzero score."""
    hits = []
    tgt_by_idx = {e.idx: e for e in tgt.ingress}
    tsk = np.stack([w[3] for w in tgt.ingress_windows]) if tgt.ingress_windows else None
    for s in src.spans:
        units = ([(-1, s.originated, s.sketch)] if s.full_ok else []) + \
                [(off, wsh, sk) for off, wsh, sk, _ in s.windows]
        # MinHash: per target entry, best Jaccard over (unit, target window).
        # Always computed for reporting; only used as a gate with prefilter=True.
        best_jac: dict[int, float] = {}
        if tsk is not None:
            usk = np.stack([u[2] for u in units])                   # U x P
            eq = (usk[:, None, :] == tsk[None, :, :]).mean(axis=2)  # U x W
            best_per_w = eq.max(axis=0)
            for (eidx, _, _, _), j in zip(tgt.ingress_windows, best_per_w):
                if j > best_jac.get(eidx, 0.0):
                    best_jac[eidx] = float(j)
        if prefilter:
            candidates = [e for e, j in best_jac.items() if j >= PREFILTER_JACCARD]
            candidates += [e.idx for e in tgt.ingress if e.idx not in best_jac]
        else:
            candidates = [e.idx for e in tgt.ingress]
        for eidx in candidates:
            tsh = tgt.ingress_shingles[eidx]
            if not tsh:
                continue
            coverage = len(s.originated & tsh) / len(s.originated) if s.originated else 0.0
            best_c, best_off = 0.0, -1
            for off, wsh, _ in units:
                c = len(wsh & tsh) / max(len(wsh), MIN_EVIDENCE)
                if c > best_c:
                    best_c, best_off = c, off
            if best_c == 0.0:
                continue
            e = tgt_by_idx[eidx]
            hits.append(Hit(src.name, tgt.name, s.entry_idx, s.turn, eidx,
                            s.artifact_type, s.channel, s.path,
                            round(best_c, 4), round(coverage, 4),
                            round(best_jac.get(eidx, 0.0), 4), best_off,
                            len(s.originated), s.text[:120], e.meta))
    return hits


def scan_all(runs: dict[str, Run], hasher: MinHasher, prefilter: bool = False) -> list[Hit]:
    all_hits = []
    names = list(runs)
    for a in names:
        for b in names:
            if a == b:
                continue
            all_hits.extend(scan_pair(runs[a], runs[b], hasher, prefilter))
    return all_hits


def matrix(runs: list[str], hits: list[Hit], score: str, threshold: float) -> dict:
    """N x N count matrix: M[src][tgt] = number of hits >= threshold."""
    idx = {r: i for i, r in enumerate(runs)}
    m = np.zeros((len(runs), len(runs)), dtype=int)
    for h in hits:
        if getattr(h, score) >= threshold:
            m[idx[h.source_run], idx[h.target_run]] += 1
    return {"runs": runs, "matrix": m.tolist()}


# -------------------------------------------------------------------- cli

def main():
    global MIN_EVIDENCE
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("root", type=pathlib.Path, help="directory containing */transcript.jsonl")
    ap.add_argument("--threshold", type=float, default=0.7)
    ap.add_argument("--score", choices=["containment", "coverage", "jaccard"], default="containment")
    ap.add_argument("--no-origination", action="store_true", help="ablation: skip the origination filter")
    ap.add_argument("--prefilter", action="store_true",
                    help="gate exact verification on MinHash Jaccard >= %.2f (faster, loses small leaks)" % PREFILTER_JACCARD)
    ap.add_argument("--common-runs", type=int, default=COMMON_RUNS,
                    help="drop shingles originated by >= K runs (convergence filter); 0 disables")
    ap.add_argument("--min-evidence", type=int, default=MIN_EVIDENCE,
                    help="containment denominator floor in shingles; 0 disables (ablation)")
    ap.add_argument("--out", type=pathlib.Path, help="write hits + matrix as JSON")
    ap.add_argument("--all-scores", action="store_true", help="keep sub-threshold hits in --out (for PR sweeps)")
    args = ap.parse_args()

    paths = discover_runs(args.root)
    if not paths:
        sys.exit(f"no transcripts under {args.root}")
    MIN_EVIDENCE = args.min_evidence
    hasher = MinHasher()
    runs = load_runs(args.root, hasher, origination=not args.no_origination, common_runs=args.common_runs)
    for n, r in runs.items():
        print(f"[{n}] entries={len(r.entries)} ingress={len(r.ingress)} "
              f"originated_spans={len(r.spans)} windows={len(r.ingress_windows)}", file=sys.stderr)

    hits = scan_all(runs, hasher, prefilter=args.prefilter)
    above = [h for h in hits if getattr(h, args.score) >= args.threshold]
    mat = matrix(list(runs), above, args.score, 0.0)

    print(f"\n{len(above)} hits at {args.score} >= {args.threshold}")
    for h in sorted(above, key=lambda h: -getattr(h, args.score))[:50]:
        print(f"  {h.source_run} -> {h.target_run}  cont={h.containment:.2f} cov={h.coverage:.2f} jac={h.jaccard:.2f} "
              f"[{h.artifact_type}/{h.channel}] {h.path or ''}  {h.source_preview[:60]!r}")
    print("\nmatrix (rows=source, cols=target):")
    print("        " + " ".join(f"{r[-6:]:>7}" for r in mat["runs"]))
    for r, row in zip(mat["runs"], mat["matrix"]):
        print(f"{r[-7:]:>7} " + " ".join(f"{v:>7}" for v in row))

    if args.out:
        payload = {
            "config": {"k": K, "num_perm": NUM_PERM, "window": WINDOW, "stride": STRIDE,
                       "src_window": SRC_WINDOW, "src_stride": SRC_STRIDE,
                       "min_shingles": MIN_SHINGLES, "min_evidence": args.min_evidence,
                       "common_runs": args.common_runs, "score": args.score,
                       "threshold": args.threshold, "origination": not args.no_origination},
            "hits": [asdict(h) for h in (hits if args.all_scores else above)],
            "matrix": mat,
        }
        args.out.write_text(json.dumps(payload, indent=1))
        print(f"\nwrote {args.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
