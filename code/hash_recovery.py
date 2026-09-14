"""How much of a run's text comes back from the hash set §6b would share?

The cross-organisational protocol proposes exchanging originated shingle hashes
instead of transcripts, on the premise that hashes are not text. They are not
text, but they are not a redaction either: character 5-grams overlap by four
characters, so the set is a de Bruijn graph and the text is a walk through it.

This assembles greedily from guessable footholds and reports two numbers: the
longest verbatim stretch recovered (exact-reconstruction risk) and the assembled
string itself (content-disclosure risk, which is the larger of the two).

    python hash_recovery.py data/runs/corpus_all/agent-38/transcript.jsonl
"""
import argparse, pathlib, sys, time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import detector as det  # noqa: E402

ALPHA = [chr(c) for c in range(32, 127)] + ["\n"]
FOOTHOLDS = ["impor", "def _", "self.", "retur", " the ", "class", "  def", "#!/us", "    ", "}\n"]


def assemble(S: set[int], seed: str, width: int = 500, maxlen: int = 1500) -> str:
    """Beam search over 4-character overlaps. Each shingle is spent once: a set
    loses repetition counts, so reusing edges would run round cycles forever."""
    succ: dict[str, list[tuple[str, int]]] = {}

    def successors(sfx):
        r = succ.get(sfx)
        if r is None:
            r = [(c, det._fnv1a32(sfx + c)) for c in ALPHA if det._fnv1a32(sfx + c) in S]
            succ[sfx] = r
        return r

    cur, best = [(seed, frozenset([det._fnv1a32(seed)]))], seed
    for _ in range(maxlen):
        nxt: dict[tuple[str, int], tuple[str, frozenset]] = {}
        for s, used in cur:
            for c, hh in successors(s[-4:]):
                if hh in used:
                    continue
                t = s + c
                k = (t[-4:], len(used))
                if k not in nxt:
                    nxt[k] = (t, used | {hh})
                if len(t) > len(best):
                    best = t
        if not nxt:
            break
        cur = [v for _, v in sorted(nxt.items(), key=lambda kv: -len(kv[1][0]))[:width]]
    return best


def longest_verbatim(a: str, b: str) -> int:
    n = 0
    for i in range(len(a)):
        for j in range(i + n + 1, len(a) + 1):
            if a[i:j] in b:
                n = j - i
            else:
                break
    return n


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("transcript", type=pathlib.Path)
    ap.add_argument("--raw", action="store_true",
                    help="use the unfiltered shingles of the span instead of the originated set")
    a = ap.parse_args()

    run = det.build_run(a.transcript.parent.name, a.transcript, det.MinHasher(), origination=True)
    span = max(run.spans, key=lambda s: len(s.originated))
    truth = det.normalise(span.text)
    S = det.shingle_hashes(span.text) if a.raw else set(span.originated)

    t0 = time.time()
    seeds = [s for s in FOOTHOLDS if det._fnv1a32(s) in S]
    if not seeds:
        print("no foothold found from the common-5-gram guess list")
        return 0
    rec = max((assemble(S, s) for s in seeds), key=len)
    el = time.time() - t0

    print(f"{a.transcript.parent.name}: {len(truth)} chars of source text")
    print(f"  {len(S)} unsalted 32-bit hashes {'(raw)' if a.raw else '(originated — what §6b sends)'}")
    print(f"  footholds guessed: {seeds}")
    print(f"  assembled {len(rec)} chars in {el:.1f}s")
    print(f"  longest verbatim stretch of the original: {longest_verbatim(rec, truth)} chars")
    print("-" * 70)
    print(rec[:800])
    print("-" * 70)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
