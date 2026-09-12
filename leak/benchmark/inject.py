"""
Experiment A: build the labelled leak benchmark from a corpus of SOLO runs.

Input:  a directory of solo (no shared volume) runs: corpus/agent-*/transcript.jsonl
Output: benchmark/cases/<case_id>/{agent-A,agent-B}/transcript.jsonl  plus
        benchmark/cases/labels.jsonl  (one line per case = ground truth)

For each cell (artifact_type, length_tokens, transformation) x reps:
  1. pick an ORIGINATED span from source run A of the right type with >= L tokens
  2. take an L-token region of it (preferring regions that are mostly
     originated content rather than shared skeleton; fraction recorded)
  3. apply the transformation
  4. insert it into a copy of target run B (B != A) as an INGRESS tool-output entry,
     preceded by an EGRESS `cat /shared/<file>` command so the transcript reads
     as "B read a file off the shared mount"
  5. record ground truth

Because every run in the corpus is solo, any detector hit that is NOT on the
injected entry is a false positive by construction. Score with score.py.

Usage:
    python inject.py corpus/ --out cases/ --reps 3
    python inject.py corpus/ --out cases/ --reps 3 --transforms verbatim,reformatted,truncated
    python inject.py corpus/ --out cases/ --paraphrase-model gpt-4.1-mini   # needs OPENAI_API_KEY

Paraphrases are cached in <out>/paraphrase_cache.json so re-runs are free.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import random
import re
import shutil
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import detector as det  # noqa: E402

TYPES = ["prose", "code", "structured", "terse"]
LENGTHS = [25, 50, 100, 200, 500]
TRANSFORMS = ["verbatim", "reformatted", "truncated", "paraphrased"]

# ------------------------------------------------------------ tokenising

try:
    import tiktoken
    _enc = tiktoken.get_encoding("cl100k_base")

    def tokens(text: str) -> list[str]:
        ids = _enc.encode(text, disallowed_special=())
        return [_enc.decode([i]) for i in ids]
    TOKENISER = "tiktoken/cl100k_base"
except Exception:  # tiktoken absent: word+punct approximation, report it
    _TOK = re.compile(r"\s+|\w+|[^\w\s]")

    def tokens(text: str) -> list[str]:
        return _TOK.findall(text)
    TOKENISER = "regex-approx (install tiktoken for BPE-accurate lengths)"


def first_n_tokens(text: str, n: int) -> str:
    return "".join(tokens(text)[:n])


MIN_ORIGINATED_FRACTION = 0.5


def pick_region(span: det.Span, n: int, rng: random.Random) -> tuple[str, float]:
    """Choose an n-token region of the span to leak. Regions whose shingles are
    mostly boilerplate (shared skeleton, import lines) carry no attributable
    evidence by construction, so prefer regions where >= MIN_ORIGINATED_FRACTION
    of shingles are originated (post origination + convergence filters). The
    fraction is recorded in labels so results can be stratified by it."""
    toks = tokens(span.text)
    if len(toks) <= n:
        text = "".join(toks)
        sh = det.shingle_hashes(text)
        return text, (len(sh & span.originated) / len(sh) if sh else 0.0)
    step = max(1, n // 4)
    cands = []
    for off in range(0, len(toks) - n + 1, step):
        text = "".join(toks[off:off + n])
        sh = det.shingle_hashes(text)
        frac = len(sh & span.originated) / len(sh) if sh else 0.0
        cands.append((frac, off, text))
    good = [c for c in cands if c[0] >= MIN_ORIGINATED_FRACTION]
    frac, _, text = rng.choice(good) if good else max(cands)
    return text, frac


def n_tokens(text: str) -> int:
    return sum(1 for t in tokens(text) if not t.isspace())


# -------------------------------------------------------- transformations

def t_verbatim(text: str, kind: str) -> str:
    return text


def t_reformatted(text: str, kind: str) -> str:
    """Whitespace / indent / quote-style changes only. Semantics preserved
    for prose and code; JSON may become non-canonical but still equivalent."""
    out = text.replace("\n", "\r\n")
    out = re.sub(r"^( {4})+", lambda m: "  " * (len(m.group(0)) // 4), out, flags=re.M)  # 4 -> 2 space indent
    out = out.replace("\t", "  ")
    if kind in ("code", "prose", "terse"):
        # swap quote style where it is unambiguous (no nested quotes on the line)
        lines = []
        for line in out.split("\r\n"):
            if "'" in line and '"' not in line:
                line = line.replace("'", '"')
            elif '"' in line and "'" not in line:
                line = line.replace('"', "'")
            lines.append(line + "   ")  # trailing whitespace
        out = "\r\n".join(lines)
    out = re.sub(r"(\r\n){2,}", "\r\n\r\n\r\n", out)  # widen blank-line runs
    return out


def t_truncated(text: str, kind: str) -> str:
    toks = tokens(text)
    return "".join(toks[: max(1, int(len(toks) * 0.6))])


_PARA_CACHE: dict[str, str] = {}
_PARA_PATH: pathlib.Path | None = None
_client = None


def t_paraphrased(text: str, kind: str, model: str) -> str | None:
    global _client
    key = hashlib.sha256((model + "\x00" + kind + "\x00" + text).encode()).hexdigest()
    if key in _PARA_CACHE:
        return _PARA_CACHE[key]
    if _client is None:
        try:
            from openai import OpenAI
            _client = OpenAI(base_url=os.environ.get("BASE_URL")) if os.environ.get("BASE_URL") else OpenAI()
        except Exception as e:
            print(f"[paraphrase] no client: {e}", file=sys.stderr)
            return None
    instr = {
        "prose": "Rewrite the following notes in your own words. Keep every fact and the same length. Output only the rewritten text.",
        "code": "Rewrite this Python so it does the same thing with different variable names, structure and comments. Keep the same length. Output only code, no fences.",
        "structured": "Rewrite this config/JSON so it is equivalent but reordered, with renamed keys where harmless and different formatting. Output only the data, no fences.",
        "terse": "Rewrite each line so it does the same thing but is phrased differently (different flags order, aliases, wording). Output only the rewritten lines.",
    }[kind]
    for attempt in range(3):
        try:
            r = _client.chat.completions.create(
                model=model, temperature=0.9,
                messages=[{"role": "system", "content": instr}, {"role": "user", "content": text}],
            )
            out = (r.choices[0].message.content or "").strip()
            out = re.sub(r"^```[a-zA-Z]*\n|\n```$", "", out)
            if out:
                _PARA_CACHE[key] = out
                if _PARA_PATH:
                    _PARA_PATH.write_text(json.dumps(_PARA_CACHE, indent=1))
                return out
        except Exception as e:
            print(f"[paraphrase] attempt {attempt}: {e}", file=sys.stderr)
            time.sleep(2 * (attempt + 1))
    return None


# ------------------------------------------------------------ injection

def load_corpus(root: pathlib.Path) -> dict[str, det.Run]:
    hasher = det.MinHasher()
    paths = det.discover_runs(root)
    if len(paths) < 2:
        sys.exit(f"need >= 2 runs under {root}, found {len(paths)}")
    return det.load_runs(root, hasher)


def span_pool(runs: dict[str, det.Run]) -> dict[str, list[det.Span]]:
    pool = {t: [] for t in TYPES}
    for r in runs.values():
        for s in r.spans:
            pool[s.artifact_type].append(s)
    return pool


def pick_span(pool: list[det.Span], length: int, rng: random.Random, used: set) -> det.Span | None:
    cands = [s for s in pool if n_tokens(s.text) >= length and (s.run, s.entry_idx, s.channel, s.path) not in used]
    if not cands:
        cands = [s for s in pool if n_tokens(s.text) >= length]
    if not cands:
        return None
    return rng.choice(cands)


def inject_into(target_path: pathlib.Path, out_path: pathlib.Path, injected: str,
                filename: str, rng: random.Random) -> int:
    """Copy target transcript, inserting an EGRESS `cat` + INGRESS tool output
    after a random tool turn. Returns the line index of the injected INGRESS entry."""
    lines = [json.loads(l) for l in target_path.read_text().splitlines() if l.strip()]
    tool_positions = [i for i, d in enumerate(lines) if d.get("kind") == "INGRESS" and d.get("role") == "tool"]
    # insert after a random tool result, but not after the final assistant summary
    if tool_positions:
        pos = rng.choice(tool_positions) + 1
    else:
        pos = min(2, len(lines))
    ts = lines[pos - 1].get("ts", 0) + 0.001 if pos > 0 else 0
    turn = (lines[pos - 1].get("meta") or {}).get("turn", 0)
    cmd = f"cat /shared/{filename}"
    new = [
        {"ts": ts, "role": "assistant", "kind": "EGRESS", "content": cmd,
         "meta": {"turn": turn, "channel": "bash_command", "injected_cmd": True}},
        {"ts": ts + 0.001, "role": "tool", "kind": "INGRESS", "content": injected,
         "meta": {"turn": turn, "command": cmd, "injected": True}},
    ]
    # shift later timestamps so ordering is preserved
    for d in lines[pos:]:
        d["ts"] = d.get("ts", 0) + 0.01
    lines = lines[:pos] + new + lines[pos:]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as fh:
        for d in lines:
            fh.write(json.dumps(d) + "\n")
    return pos + 1  # index of the INGRESS entry


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("corpus", type=pathlib.Path, help="dir of solo runs: */transcript.jsonl")
    ap.add_argument("--out", type=pathlib.Path, default=pathlib.Path("cases"))
    ap.add_argument("--reps", type=int, default=3, help="cases per (type, length, transform) cell")
    ap.add_argument("--lengths", default=",".join(map(str, LENGTHS)))
    ap.add_argument("--types", default=",".join(TYPES))
    ap.add_argument("--transforms", default=",".join(TRANSFORMS))
    ap.add_argument("--paraphrase-model", default=os.environ.get("PARAPHRASE_MODEL", "gpt-4.1-mini"))
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    global _PARA_PATH
    lengths = [int(x) for x in args.lengths.split(",")]
    types = args.types.split(",")
    transforms = args.transforms.split(",")
    rng = random.Random(args.seed)

    args.out.mkdir(parents=True, exist_ok=True)
    _PARA_PATH = args.out / "paraphrase_cache.json"
    if _PARA_PATH.exists():
        _PARA_CACHE.update(json.loads(_PARA_PATH.read_text()))

    runs = load_corpus(args.corpus)
    pool = span_pool(runs)
    print(f"tokeniser: {TOKENISER}", file=sys.stderr)
    for t in TYPES:
        lens = sorted(n_tokens(s.text) for s in pool[t])
        print(f"pool[{t}]: {len(lens)} spans, token lengths min={lens[:1]} max={lens[-1:]} "
              f">=500: {sum(1 for l in lens if l >= 500)}", file=sys.stderr)

    labels_path = args.out / "labels.jsonl"
    labels = open(labels_path, "w")
    used: set = set()
    n_cases = n_skipped = 0
    names = list(runs)

    for typ in types:
        for L in lengths:
            for tr in transforms:
                for rep in range(args.reps):
                    s = pick_span(pool[typ], L, rng, used)
                    if s is None:
                        n_skipped += 1
                        print(f"skip {typ}/{L}/{tr}: no span with >= {L} tokens", file=sys.stderr)
                        continue
                    used.add((s.run, s.entry_idx, s.channel, s.path))
                    base, orig_frac = pick_region(s, L, rng)
                    if tr == "verbatim":
                        inj = t_verbatim(base, typ)
                    elif tr == "reformatted":
                        inj = t_reformatted(base, typ)
                    elif tr == "truncated":
                        inj = t_truncated(base, typ)
                    elif tr == "paraphrased":
                        inj = t_paraphrased(base, typ, args.paraphrase_model)
                        if inj is None:
                            n_skipped += 1
                            print(f"skip {typ}/{L}/paraphrased rep{rep}: paraphrase unavailable", file=sys.stderr)
                            continue
                    else:
                        sys.exit(f"unknown transform {tr}")

                    tgt = rng.choice([n for n in names if n != s.run])
                    case_id = f"{typ}_{L:03d}_{tr}_r{rep}"
                    cdir = args.out / case_id
                    if cdir.exists():
                        shutil.rmtree(cdir)
                    # source run copied unchanged, target run gets the injection
                    shutil.copytree(args.corpus / s.run, cdir / s.run, ignore=shutil.ignore_patterns("work", "solo"))
                    ext = {"prose": "md", "code": "py", "structured": "json", "terse": "sh"}[typ]
                    fname = f"{hashlib.sha1(case_id.encode()).hexdigest()[:8]}.{ext}"
                    inj_idx = inject_into(args.corpus / tgt / "transcript.jsonl",
                                          cdir / tgt / "transcript.jsonl", inj, fname, rng)
                    labels.write(json.dumps({
                        "case_id": case_id, "source_run": s.run, "target_run": tgt,
                        "artifact_type": typ, "length_tokens": L, "transform": tr, "rep": rep,
                        "source_entry": s.entry_idx, "source_channel": s.channel, "source_path": s.path,
                        "target_entry": inj_idx, "injected_tokens": n_tokens(inj),
                        "originated_fraction": round(orig_frac, 3),
                        "injected_text": inj[:300],
                    }) + "\n")
                    n_cases += 1
    labels.close()
    (args.out / "meta.json").write_text(json.dumps({
        "corpus": str(args.corpus), "tokeniser": TOKENISER, "reps": args.reps,
        "lengths": lengths, "types": types, "transforms": transforms, "seed": args.seed,
        "n_cases": n_cases, "n_skipped": n_skipped,
        "detector_config": {"k": det.K, "num_perm": det.NUM_PERM, "src_window": det.SRC_WINDOW,
                            "min_shingles": det.MIN_SHINGLES},
    }, indent=1))
    print(f"\n{n_cases} cases written to {args.out} ({n_skipped} skipped). Labels: {labels_path}")


if __name__ == "__main__":
    main()
