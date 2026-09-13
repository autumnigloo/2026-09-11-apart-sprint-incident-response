# Experiment C: keyed watermark on agent-style artifacts (Qwen/Qwen2.5-0.5B-Instruct)

gamma 0.25, delta 2.0, sampling T=0.8 top-p 0.95, 10 samples per cell each way, 32 run-keys. Single-key threshold at 1% FPR from the empirical null: z >= 3.77 (theory 2.326). Null scores: 5120 (160 unwatermarked samples x 32 keys).

## Detection rate at 1% FPR by type and generated length (full sample)

| type | 50 | 100 | 200 | 500 |
|---|---|---|---|---|
| prose | 0.80 (n=10, mean tokens 50) | 0.80 (n=10, mean tokens 100) | 1.00 (n=10, mean tokens 200) | 1.00 (n=10, mean tokens 464) |
| code | 0.20 (n=10, mean tokens 50) | 0.80 (n=10, mean tokens 100) | 0.70 (n=10, mean tokens 200) | 1.00 (n=10, mean tokens 500) |
| structured | 0.20 (n=10, mean tokens 50) | 0.90 (n=10, mean tokens 97) | 0.70 (n=10, mean tokens 178) | 0.80 (n=10, mean tokens 201) |
| terse | 0.40 (n=10, mean tokens 48) | 1.00 (n=10, mean tokens 100) | 1.00 (n=10, mean tokens 192) | 1.00 (n=10, mean tokens 332) |

## Detection rate at 1% FPR on the first 50 and first 100 tokens

| type | first 50 | first 100 |
|---|---|---|
| prose | 0.62 (n=40) | 0.87 (n=30) |
| code | 0.38 (n=40) | 0.60 (n=30) |
| structured | 0.30 (n=40) | 0.76 (n=25) |
| terse | 0.66 (n=38) | 0.97 (n=29) |

## Next-token entropy by type: the room a watermark has (unwatermarked samples)

| type | mean entropy (nats) | share of tokens under 0.5 nat (near-forced) |
|---|---|---|
| prose | 1.38 | 0.29 |
| code | 0.75 | 0.53 |
| structured | 0.73 | 0.66 |
| terse | 1.27 | 0.34 |

## False-positive rate when one text is scanned against N run-keys (max over keys)

| N keys | FPR at the single-key threshold |
|---|---|
| 1 | 0.010 |
| 2 | 0.021 |
| 4 | 0.041 |
| 8 | 0.073 |
| 16 | 0.109 |
| 32 | 0.156 |

Overall detection rate of the true key at this threshold: 0.77 over 160 watermarked samples.

Reading: the single-key threshold holds 1% FPR by construction; scanning one text against N keys and keeping the maximum inflates it roughly N-fold until it saturates. A fleet of N parallel runs is exactly this regime.

## What to compare with Experiment A

Hashing found 100% of verbatim leaks of 100 tokens or more of every type at zero false alarms, on a model it never had access to. The table above is what a watermark achieves on the same artifact types with full model access and no transformation of the text at all.
