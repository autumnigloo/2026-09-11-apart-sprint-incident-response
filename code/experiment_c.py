"""
Experiment C: can a per-run keyed LLM watermark be detected on agent-style artifacts?

Runs a small open-weight model locally (default Qwen/Qwen2.5-0.5B-Instruct), generates
four artifact types (prose, code, structured JSON, terse shell) at several lengths, with
and without a keyed green-list watermark (Kirchenbauer et al. 2023, hash-partitioned
green list, gamma = 0.25, delta = 2.0), and measures:

  1. detection rate at 1% false-positive rate, per type x length (threshold set from the
     empirical null: unwatermarked text scored with the same key)
  2. the same after truncation to the first 50 / 100 tokens (short-span behaviour)
  3. false-positive inflation when one text is scanned against N run-keys and the max
     score is taken (N = 1, 2, 4, 8, 16, 32)
  4. mean next-token entropy per artifact type, which is the mechanism: a watermark can
     only bias choices the model actually has

Output: results_c/summary.md plus per-sample scores in results_c/scores.jsonl.

Install (Apple Silicon):
    pip install torch transformers accelerate
Run (about 30 to 60 minutes on an M4 Air at the defaults; the model downloads once):
    python experiment_c.py --n 8
    python experiment_c.py --n 4 --lengths 50,100,200      # faster smoke run
"""

from __future__ import annotations

import argparse
import json
import math
import pathlib
import random
import sys
import time

import numpy as np

try:
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer, LogitsProcessor, LogitsProcessorList
except ImportError:
    sys.exit("needs torch and transformers:  pip install torch transformers accelerate")

GAMMA = 0.25
DELTA = 2.0
P = 2147483647
NKEYS_FPR = [1, 2, 4, 8, 16, 32]

# ------------------------------------------------------------- prompts

TOPICS = ["a library catalogue", "a text adventure engine", "a bank ledger", "a recipe scaler",
          "a tournament scheduler", "a log analyser", "a flashcard trainer", "a matrix library",
          "an inventory manager", "a markdown converter", "a weather statistics tool",
          "a task planner", "a cipher toolkit", "a grades system", "a URL shortener",
          "a polynomial helper", "a parking simulator", "a CSV cleaner", "a chess validator",
          "a budget tracker"]

def prompt_for(kind: str, topic: str, length: int) -> str:
    words = int(length * 0.75)
    if kind == "prose":
        return (f"Write the README for {topic} in Python: design, usage and limitations. "
                f"About {words} words of plain prose, no code blocks, no headings.")
    if kind == "code":
        return (f"Write a Python module implementing {topic} with several functions and docstrings, "
                f"about {max(15, length // 8)} lines. Output only code, no explanation, no fences.")
    if kind == "structured":
        return (f"Write a JSON configuration file for {topic} with about {max(8, length // 6)} keys, "
                f"including nested objects and lists. Output only the JSON, no fences.")
    return (f"Write {max(3, length // 12)} bash one-liners a developer would run while building "
            f"{topic} (create files, run tests, inspect output). One command per line, no explanation.")


# ----------------------------------------------------------- watermark

M32 = 0xFFFFFFFF

def _mix_np(x: np.ndarray) -> np.ndarray:
    """32-bit avalanche mix (lowbias32). Keys must give independent green lists; a plain
    linear hash shifts every token's value by the same constant for a different key, so
    two keys' lists overlap far more than chance (measured 14-27% cross-key false alarms)."""
    x = x & M32
    x = ((x ^ (x >> 16)) * 0x7FEB352D) & M32
    x = ((x ^ (x >> 15)) * 0x846CA68B) & M32
    return (x ^ (x >> 16)) & M32


def green_mask(prev_ids: torch.Tensor, key: int, vocab: int, device) -> torch.Tensor:
    """Boolean [batch, vocab]: which next tokens are 'green' given previous token and key."""
    ids = torch.arange(vocab, device=device, dtype=torch.int64)
    x = (ids[None, :] * 1000003 + prev_ids[:, None].to(torch.int64) * 7919 + (key & M32) * 104729) & M32
    x = ((x ^ (x >> 16)) * 0x7FEB352D) & M32
    x = ((x ^ (x >> 15)) * 0x846CA68B) & M32
    x = (x ^ (x >> 16)) & M32
    return (x % 1000) < int(GAMMA * 1000)


class KGWProcessor(LogitsProcessor):
    def __init__(self, key: int, vocab: int):
        self.key, self.vocab = key, vocab

    def __call__(self, input_ids, scores):
        mask = green_mask(input_ids[:, -1], self.key, scores.shape[-1], scores.device)
        return scores + mask.to(scores.dtype) * DELTA


def z_score(token_ids: list[int], key: int) -> float:
    """Green-token z-score for a sequence under a key (tokens after the first)."""
    if len(token_ids) < 2:
        return 0.0
    prev = np.array(token_ids[:-1], dtype=np.int64)
    cur = np.array(token_ids[1:], dtype=np.int64)
    h = _mix_np((cur * 1000003 + prev * 7919 + (key & M32) * 104729) & M32)
    g = int(((h % 1000) < int(GAMMA * 1000)).sum())
    T = len(cur)
    return (g - GAMMA * T) / math.sqrt(T * GAMMA * (1 - GAMMA))


# --------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", default="Qwen/Qwen2.5-0.5B-Instruct")
    ap.add_argument("--n", type=int, default=8, help="samples per (type, length), watermarked and not")
    ap.add_argument("--lengths", default="50,100,200,500")
    ap.add_argument("--types", default="prose,code,structured,terse")
    ap.add_argument("--keys", type=int, default=32, help="size of the run-key space for the multi-key test")
    ap.add_argument("--out", type=pathlib.Path, default=pathlib.Path("data/results_c"))
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    lengths = [int(x) for x in args.lengths.split(",")]
    types = args.types.split(",")
    args.out.mkdir(parents=True, exist_ok=True)
    rng = random.Random(args.seed)
    torch.manual_seed(args.seed)

    device = "mps" if torch.backends.mps.is_available() else ("cuda" if torch.cuda.is_available() else "cpu")
    print(f"device: {device}; loading {args.model}", file=sys.stderr)
    tok = AutoTokenizer.from_pretrained(args.model)
    tok.padding_side = "left"
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    model = AutoModelForCausalLM.from_pretrained(args.model, torch_dtype=torch.float16 if device != "cpu" else torch.float32).to(device)
    model.eval()
    vocab = model.get_output_embeddings().weight.shape[0]
    keys = [rng.randrange(1, P) for _ in range(args.keys)]

    scores_fh = open(args.out / "scores.jsonl", "w")
    records = []
    t0 = time.time()

    def generate(prompts: list[str], max_new: int, key: int | None) -> list[list[int]]:
        msgs = [[{"role": "user", "content": p}] for p in prompts]
        texts = [tok.apply_chat_template(m, tokenize=False, add_generation_prompt=True) for m in msgs]
        enc = tok(texts, return_tensors="pt", padding=True).to(device)
        procs = LogitsProcessorList([KGWProcessor(key, vocab)]) if key is not None else None
        with torch.no_grad():
            out = model.generate(**enc, max_new_tokens=max_new, min_new_tokens=min(max_new, 16),
                                 do_sample=True, temperature=0.8, top_p=0.95,
                                 logits_processor=procs, pad_token_id=tok.pad_token_id)
        gen = out[:, enc["input_ids"].shape[1]:]
        res = []
        for row in gen:
            ids = [int(i) for i in row.tolist() if i != tok.pad_token_id]
            res.append(ids)
        return res

    def entropy_of(ids: list[int], prompt: str) -> tuple[float, float]:
        """Mean next-token entropy (nats) over the generated tokens, and the share of
        tokens where the model had under 0.5 nat of entropy (near-forced tokens)."""
        msgs = [{"role": "user", "content": prompt}]
        pre = tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
        pre_ids = tok(pre, return_tensors="pt")["input_ids"][0].tolist()
        full = torch.tensor([pre_ids + ids], device=device)
        with torch.no_grad():
            logits = model(full).logits[0, len(pre_ids) - 1:-1].float()
        lp = torch.log_softmax(logits, dim=-1)
        ent = -(lp.exp() * lp).sum(-1)
        return float(ent.mean()), float((ent < 0.5).float().mean())

    # ---- generate
    for kind in types:
        for L in lengths:
            topics = [rng.choice(TOPICS) for _ in range(args.n)]
            prompts = [prompt_for(kind, t, L) for t in topics]
            for watermarked in (True, False):
                key = rng.choice(keys) if watermarked else None
                ids_list = generate(prompts, L, key)
                for prompt, ids in zip(prompts, ids_list):
                    ent, low = entropy_of(ids, prompt) if len(ids) > 1 else (float("nan"), float("nan"))
                    rec = {"type": kind, "length": L, "watermarked": watermarked, "key": key,
                           "n_tokens": len(ids), "entropy": ent, "low_entropy_share": low,
                           "z_key": z_score(ids, key) if watermarked else None,
                           "z_all": [z_score(ids, k) for k in keys],
                           "z_all_50": [z_score(ids[:50], k) for k in keys],
                           "z_all_100": [z_score(ids[:100], k) for k in keys],
                           "z_key_50": z_score(ids[:50], key) if watermarked else None,
                           "z_key_100": z_score(ids[:100], key) if watermarked else None,
                           "text": tok.decode(ids)[:300]}
                    records.append(rec)
                    scores_fh.write(json.dumps(rec) + "\n")
            print(f"[{time.time()-t0:5.0f}s] {kind:10s} L={L:3d} done", file=sys.stderr)
    scores_fh.close()

    # ---- analysis
    null = [r for r in records if not r["watermarked"]]
    pos = [r for r in records if r["watermarked"]]

    # single-key threshold at 1% FPR from the empirical null: every unwatermarked sample
    # scored against every key (keys give independent green lists, so these are
    # near-independent draws), giving len(null) * len(keys) null scores.
    null_z = np.array([z for r in null for z in r["z_all"]])
    thr = float(np.quantile(null_z, 0.99)) if len(null_z) else 4.0
    def _trunc_thr(field, n):
        z = np.array([x for r in null if r["n_tokens"] >= n for x in r.get(field, [])])
        return float(np.quantile(z, 0.99)) if z.size else thr
    thr50, thr100 = _trunc_thr("z_all_50", 50), _trunc_thr("z_all_100", 100)
    thr_theory = 2.326  # one-sided z for 1%

    md = [f"# Experiment C: keyed watermark on agent-style artifacts ({args.model})", "",
          f"gamma {GAMMA}, delta {DELTA}, sampling T=0.8 top-p 0.95, {args.n} samples per cell each way, "
          f"{len(keys)} run-keys. Single-key threshold at 1% FPR from the empirical null: z >= {thr:.2f} "
          f"(theory {thr_theory}). Null scores: {len(null_z)} ({len(null)} unwatermarked samples x {len(keys)} keys).", ""]

    md += ["## Detection rate at 1% FPR by type and generated length (full sample)", "",
           "| type | " + " | ".join(str(L) for L in lengths) + " |", "|---|" + "---|" * len(lengths)]
    for kind in types:
        row = []
        for L in lengths:
            s = [r for r in pos if r["type"] == kind and r["length"] == L]
            row.append("n/a" if not s else f"{np.mean([r['z_key'] >= thr for r in s]):.2f} (n={len(s)}, mean tokens {np.mean([r['n_tokens'] for r in s]):.0f})")
        md.append(f"| {kind} | " + " | ".join(row) + " |")

    md += ["", f"## Detection rate at 1% FPR on the first 50 and first 100 tokens "
           f"(truncated-null thresholds z >= {thr50:.2f} / {thr100:.2f})", "",
           "| type | first 50 | first 100 |", "|---|---|---|"]
    for kind in types:
        s = [r for r in pos if r["type"] == kind and r["n_tokens"] >= 50]
        s100 = [r for r in pos if r["type"] == kind and r["n_tokens"] >= 100]
        a = f"{np.mean([r['z_key_50'] >= thr50 for r in s]):.2f} (n={len(s)})" if s else "n/a"
        b = f"{np.mean([r['z_key_100'] >= thr100 for r in s100]):.2f} (n={len(s100)})" if s100 else "n/a"
        md.append(f"| {kind} | {a} | {b} |")

    md += ["", "## Next-token entropy by type: the room a watermark has (unwatermarked samples)", "",
           "| type | mean entropy (nats) | share of tokens under 0.5 nat (near-forced) |", "|---|---|---|"]
    for kind in types:
        s = [r for r in null if r["type"] == kind and not math.isnan(r["entropy"])]
        md.append(f"| {kind} | {np.mean([r['entropy'] for r in s]):.2f} | {np.mean([r['low_entropy_share'] for r in s]):.2f} |")

    md += ["", "## False-positive rate when one text is scanned against N run-keys (max over keys)", "",
           "| N keys | FPR at the single-key threshold |", "|---|---|"]
    for N in NKEYS_FPR:
        if N > len(keys):
            continue
        # average over key subsets so the estimate does not depend on which keys come first
        fps = []
        for start in range(0, len(keys) - N + 1, max(1, N)):
            fps.append(np.mean([max(r["z_all"][start:start + N]) >= thr for r in null]))
        md.append(f"| {N} | {np.mean(fps):.3f} |")
    md += ["", f"Overall detection rate of the true key at this threshold: "
           f"{np.mean([r['z_key'] >= thr for r in pos]):.2f} over {len(pos)} watermarked samples.",
           "", "Reading: the single-key threshold holds 1% FPR by construction; scanning one text against "
           "N keys and keeping the maximum inflates it roughly N-fold until it saturates. A fleet of N "
           "parallel runs is exactly this regime.", ""]

    md += ["## What to compare with Experiment A", "",
           "Hashing found 100% of verbatim leaks of 100 tokens or more of every type at zero false alarms, "
           "on a model it never had access to. The table above is what a watermark achieves on the same "
           "artifact types with full model access and no transformation of the text at all.", ""]
    (args.out / "summary.md").write_text("\n".join(md))
    print("\n".join(md))


if __name__ == "__main__":
    main()
