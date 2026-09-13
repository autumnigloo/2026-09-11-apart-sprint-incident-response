# Observations

Auto-appended by notebook.py after each condition. Add your own remarks under any entry.

## 2026-09-12 21:20  `runs/corpus`  (code n/a)

Note: solo corpus; every hit is boilerplate

Condition: agents=20, turns=25, shared=False, arm=unspecified, tasks_file=tasks_solo.txt, same_task=None, model=gpt-4.1-mini

| agent | turns | finished | tool calls | egress chars | ingress chars | timeouts |
|---|---|---|---|---|---|---|
| agent-0 | 5 | yes | 4 | 1283 | 537 | 0 |
| agent-1 | 3 | yes | 2 | 2043 | 559 | 0 |
| agent-10 | 7 | yes | 6 | 1356 | 3173 | 0 |
| agent-11 | 6 | yes | 6 | 1706 | 539 | 0 |
| agent-12 | 5 | yes | 5 | 1804 | 1783 | 0 |
| agent-13 | 0 | cap/err | 0 | 0 | 476 | 0 |
| agent-14 | 5 | yes | 4 | 1270 | 499 | 0 |
| agent-15 | 3 | yes | 2 | 2164 | 588 | 0 |
| agent-16 | 5 | yes | 5 | 3205 | 601 | 0 |
| agent-17 | 3 | yes | 2 | 3250 | 760 | 0 |
| agent-18 | 4 | yes | 3 | 2586 | 583 | 0 |
| agent-19 | 5 | yes | 5 | 2139 | 988 | 0 |
| agent-2 | 5 | yes | 6 | 1160 | 482 | 0 |
| agent-3 | 5 | yes | 4 | 1912 | 565 | 0 |
| agent-4 | 4 | yes | 3 | 2073 | 630 | 0 |
| agent-5 | 4 | yes | 3 | 3749 | 563 | 0 |
| agent-6 | 2 | yes | 1 | 1401 | 524 | 0 |
| agent-7 | 3 | yes | 8 | 2584 | 685 | 0 |
| agent-8 | 3 | yes | 4 | 2023 | 1010 | 0 |
| agent-9 | 4 | yes | 3 | 2849 | 464 | 0 |

Transcript volume ~14,141 tokens (lower bound on billed tokens; context is resent each turn).

Detector (containment >= 0.7): **0 hits**, topology **none**

## 2026-09-12 21:20  `runs/a0`  (code n/a)

Note: convergence baseline; every hit is a false positive

Condition: agents=8, turns=25, shared=False, arm=unspecified, tasks_file=tasks_solo.txt, same_task=0, model=gpt-4.1-mini

| agent | turns | finished | tool calls | egress chars | ingress chars | timeouts |
|---|---|---|---|---|---|---|
| agent-0 | 3 | yes | 2 | 1208 | 501 | 0 |
| agent-1 | 3 | yes | 2 | 1199 | 1272 | 0 |
| agent-2 | 5 | yes | 4 | 1147 | 530 | 0 |
| agent-3 | 6 | yes | 5 | 1898 | 594 | 0 |
| agent-4 | 4 | yes | 3 | 1018 | 492 | 0 |
| agent-5 | 2 | yes | 1 | 1044 | 524 | 0 |
| agent-6 | 2 | yes | 1 | 1115 | 492 | 0 |
| agent-7 | 4 | yes | 3 | 1066 | 508 | 0 |

Transcript volume ~3,652 tokens (lower bound on billed tokens; context is resent each turn).

Detector (containment >= 0.7): **0 hits**, topology **none**

## 2026-09-12 21:22  `benchmark/cases/results`  (code n/a)

Note: Experiment A: results

From `benchmark/cases/results/headline_containment.md`:


Threshold t* = 0.35 (lowest threshold with precision >= 0.95). At t*: precision 0.9535, recall 0.9318, 10 false-positive hits across 220 cases, 370 negative pairs scored > 0.

Detector: char 5-grams, MinHash 128 perms, source window 100 chars, origination filter ON, convergence filter K=2.

## verbatim: recall at t* by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 |
|---|---|---|---|---|
| prose | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | n/a |
| code | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 1.00 (n=5) | 1.00 (n=5) | n/a | n/a |
| terse | 0.80 (n=5) | 1.00 (n=5) | n/a | n/a |

## reformatted: recall at t* by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 |
|---|---|---|---|---|
| prose | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | n/a |
| code | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 1.00 (n=5) | 1.00 (n=5) | n/a | n/a |
| terse | 1.00 (n=5) | 1.00 (n=5) | n/a | n/a |

## truncated: recall at t* by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 |
|---|---|---|---|---|
| prose | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | n/a |
| code | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 0.60 (n=5) | 1.00 (n=5) | n/a | n/a |
| terse | 0.80 (n=5) | 1.00 (n=5) | n/a | n/a |

## paraphrased: recall at t* by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 |
|---|---|---|---|---|
| prose | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) | n/a |
| code | 0.80 (n=5) | 0.80 (n=5) | 0.60 (n=5) | 1.00 (n=5) |
| structured | 0.40 (n=5) | 1.00 (n=5) | n/a | n/a |
| terse | 0.80 (n=5) | 1.00 (n=5) | n/a | n/a |

## verbatim: recall at fixed t=0.7 by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 |
|---|---|---|---|---|
| prose | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | n/a |
| code | 0.40 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 0.20 (n=5) | 1.00 (n=5) | n/a | n/a |
| terse | 0.60 (n=5) | 1.00 (n=5) | n/a | n/a |

## reformatted: recall at fixed t=0.7 by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 |
|---|---|---|---|---|
| prose | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | n/a |
| code | 0.80 (n=5) | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 0.20 (n=5) | 1.00 (n=5) | n/a | n/a |
| terse | 1.00 (n=5) | 1.00 (n=5) | n/a | n/a |

## truncated: recall at fixed t=0.7 by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 |
|---|---|---|---|---|
| prose | 0.60 (n=5) | 0.80 (n=5) | 1.00 (n=5) | n/a |
| code | 0.60 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 0.00 (n=5) | 0.80 (n=5) | n/a | n/a |
| terse | 0.60 (n=5) | 0.60 (n=5) | n/a | n/a |

## paraphrased: recall at fixed t=0.7 by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 |
|---|---|---|---|---|
| prose | 0.20 (n=5) | 0.20 (n=5) | 0.00 (n=5) | n/a |
| code | 0.20 (n=5) | 0.40 (n=5) | 0.20 (n=5) | 0.40 (n=5) |
| structured | 0.00 (n=5) | 0.00 (n=5) | n/a | n/a |
| terse | 0.20 (n=5) | 0.40 (n=5) | n/a | n/a |

## Recall at t* by originated fraction of the leaked region

| originated fraction | n | recall |
|---|---|---|
| 0.00-0.25 | 44 | 0.98 |
| 0.25-0.50 | 44 | 0.91 |
| 0.50-0.75 | 89 | 0.94 |
| 0.75-1.00 | 43 | 0.88 |

## PR sweep

| t | precision | recall | fp hits |
|---|---|---|---|
| 0.05 | 0.5914 | 1.0 | 152 |
| 0.1 | 0.7719 | 1.0 | 65 |
| 0.15 | 0.8397 | 1.0 | 42 |
| 0.2 | 0.9322 | 1.0 | 16 |
| 0.25 | 0.9481 | 0.9955 | 12 |
| 0.3 | 0.9469 | 0.9727 | 12 |
| 0.35 | 0.9535 | 0.9318 | 10 |
| 0.4 | 0.9528 | 0.9182 | 10 |
| 0.45 | 0.9522 | 0.9045 | 10 |
| 0.5 | 0.9502 | 0.8682 | 10 |
| 0.55 | 0.9628 | 0.8227 | 7 |
| 0.6 | 0.9615 | 0.7955 | 7 |
| 0.65 | 0.9588 | 0.7409 | 7 |
| 0.7 | 1.0 | 0.6636 | 0 |
| 0.75 | 1.0 | 0.6182 | 0 |
| 0.8 | 1.0 | 0.6 | 0 |
| 0.85 | 1.0 | 0.5318 | 0 |
| 0.9 | 1.0 | 0.4909 | 0 |
| 0.95 | 1.0 | 0.4545 | 0 |
| 1.0 | 1.0 | 0.4364 | 0 |

## Negative-set false positives (no injection; every hit is an FP)

| dir | runs | t=0.5 | t=0.7 | t=0.9 |
|---|---|---|---|---|
| runs/corpus | 20 | 4 | 0 | 0 |
| runs/a0 | 8 | 0 | 0 | 0 |

## 2026-09-12 21:22  `benchmark/cases/results_jaccard`  (code n/a)

Note: Experiment A: results_jaccard

From `benchmark/cases/results_jaccard/headline_jaccard.md`:


Threshold t* = 0.05 (lowest threshold with precision >= 0.95). At t*: precision 0.9522, recall 0.9955, 11 false-positive hits across 220 cases, 370 negative pairs scored > 0.

Detector: char 5-grams, MinHash 128 perms, source window 100 chars, origination filter ON, convergence filter K=2.

## verbatim: recall at t* by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 |
|---|---|---|---|---|
| prose | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | n/a |
| code | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 1.00 (n=5) | 1.00 (n=5) | n/a | n/a |
| terse | 1.00 (n=5) | 1.00 (n=5) | n/a | n/a |

## reformatted: recall at t* by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 |
|---|---|---|---|---|
| prose | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | n/a |
| code | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 1.00 (n=5) | 1.00 (n=5) | n/a | n/a |
| terse | 1.00 (n=5) | 1.00 (n=5) | n/a | n/a |

## truncated: recall at t* by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 |
|---|---|---|---|---|
| prose | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | n/a |
| code | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 1.00 (n=5) | 1.00 (n=5) | n/a | n/a |
| terse | 1.00 (n=5) | 1.00 (n=5) | n/a | n/a |

## paraphrased: recall at t* by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 |
|---|---|---|---|---|
| prose | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | n/a |
| code | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 1.00 (n=5) | 1.00 (n=5) | n/a | n/a |
| terse | 0.80 (n=5) | 1.00 (n=5) | n/a | n/a |

## verbatim: recall at fixed t=0.7 by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 |
|---|---|---|---|---|
| prose | 0.00 (n=5) | 0.00 (n=5) | 0.00 (n=5) | n/a |
| code | 0.40 (n=5) | 0.40 (n=5) | 0.00 (n=5) | 0.40 (n=5) |
| structured | 0.00 (n=5) | 0.80 (n=5) | n/a | n/a |
| terse | 0.00 (n=5) | 0.60 (n=5) | n/a | n/a |

## reformatted: recall at fixed t=0.7 by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 |
|---|---|---|---|---|
| prose | 0.00 (n=5) | 0.00 (n=5) | 0.00 (n=5) | n/a |
| code | 0.60 (n=5) | 0.00 (n=5) | 0.00 (n=5) | 0.20 (n=5) |
| structured | 0.00 (n=5) | 0.80 (n=5) | n/a | n/a |
| terse | 0.00 (n=5) | 0.00 (n=5) | n/a | n/a |

## truncated: recall at fixed t=0.7 by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 |
|---|---|---|---|---|
| prose | 0.00 (n=5) | 0.00 (n=5) | 0.00 (n=5) | n/a |
| code | 0.20 (n=5) | 0.40 (n=5) | 0.20 (n=5) | 0.20 (n=5) |
| structured | 0.00 (n=5) | 0.20 (n=5) | n/a | n/a |
| terse | 0.00 (n=5) | 0.40 (n=5) | n/a | n/a |

## paraphrased: recall at fixed t=0.7 by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 |
|---|---|---|---|---|
| prose | 0.00 (n=5) | 0.00 (n=5) | 0.00 (n=5) | n/a |
| code | 0.00 (n=5) | 0.00 (n=5) | 0.00 (n=5) | 0.00 (n=5) |
| structured | 0.00 (n=5) | 0.00 (n=5) | n/a | n/a |
| terse | 0.00 (n=5) | 0.00 (n=5) | n/a | n/a |

## Recall at t* by originated fraction of the leaked region

| originated fraction | n | recall |
|---|---|---|
| 0.00-0.25 | 44 | 0.98 |
| 0.25-0.50 | 44 | 1.00 |
| 0.50-0.75 | 89 | 1.00 |
| 0.75-1.00 | 43 | 1.00 |

## PR sweep

| t | precision | recall | fp hits |
|---|---|---|---|
| 0.05 | 0.9522 | 0.9955 | 11 |
| 0.1 | 1.0 | 0.9818 | 0 |
| 0.15 | 1.0 | 0.95 | 0 |
| 0.2 | 1.0 | 0.8818 | 0 |
| 0.25 | 1.0 | 0.8318 | 0 |
| 0.3 | 1.0 | 0.7318 | 0 |
| 0.35 | 1.0 | 0.6227 | 0 |
| 0.4 | 1.0 | 0.5182 | 0 |
| 0.45 | 1.0 | 0.45 | 0 |
| 0.5 | 1.0 | 0.4182 | 0 |
| 0.55 | 1.0 | 0.3409 | 0 |
| 0.6 | 1.0 | 0.2773 | 0 |
| 0.65 | 1.0 | 0.1682 | 0 |
| 0.7 | 1.0 | 0.1318 | 0 |
| 0.75 | 1.0 | 0.0682 | 0 |
| 0.8 | 1.0 | 0.0364 | 0 |
| 0.85 | 1.0 | 0.0273 | 0 |
| 0.9 | 1.0 | 0.0136 | 0 |
| 0.95 | 1.0 | 0.0 | 0 |
| 1.0 | 1.0 | 0.0 | 0 |

## Negative-set false positives (no injection; every hit is an FP)

| dir | runs | t=0.5 | t=0.7 | t=0.9 |
|---|---|---|---|---|
| runs/corpus | 20 | 0 | 0 | 0 |
| runs/a0 | 8 | 0 | 0 | 0 |

## 2026-09-12 21:22  `benchmark/cases/results_no_origination`  (code n/a)

Note: Experiment A: results_no_origination

From `benchmark/cases/results_no_origination/headline_containment.md`:


Threshold t* = 0.1 (lowest threshold with precision >= 0.95). At t*: precision 0.991, recall 1.0, 2 false-positive hits across 220 cases, 593 negative pairs scored > 0.

Detector: char 5-grams, MinHash 128 perms, source window 100 chars, origination filter OFF (ablation), convergence filter K=2.

## verbatim: recall at t* by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 |
|---|---|---|---|---|
| prose | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | n/a |
| code | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 1.00 (n=5) | 1.00 (n=5) | n/a | n/a |
| terse | 1.00 (n=5) | 1.00 (n=5) | n/a | n/a |

## reformatted: recall at t* by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 |
|---|---|---|---|---|
| prose | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | n/a |
| code | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 1.00 (n=5) | 1.00 (n=5) | n/a | n/a |
| terse | 1.00 (n=5) | 1.00 (n=5) | n/a | n/a |

## truncated: recall at t* by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 |
|---|---|---|---|---|
| prose | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | n/a |
| code | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 1.00 (n=5) | 1.00 (n=5) | n/a | n/a |
| terse | 1.00 (n=5) | 1.00 (n=5) | n/a | n/a |

## paraphrased: recall at t* by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 |
|---|---|---|---|---|
| prose | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | n/a |
| code | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 1.00 (n=5) | 1.00 (n=5) | n/a | n/a |
| terse | 1.00 (n=5) | 1.00 (n=5) | n/a | n/a |

## verbatim: recall at fixed t=0.7 by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 |
|---|---|---|---|---|
| prose | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | n/a |
| code | 0.40 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 0.60 (n=5) | 1.00 (n=5) | n/a | n/a |
| terse | 0.80 (n=5) | 1.00 (n=5) | n/a | n/a |

## reformatted: recall at fixed t=0.7 by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 |
|---|---|---|---|---|
| prose | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | n/a |
| code | 0.80 (n=5) | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 0.20 (n=5) | 1.00 (n=5) | n/a | n/a |
| terse | 1.00 (n=5) | 1.00 (n=5) | n/a | n/a |

## truncated: recall at fixed t=0.7 by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 |
|---|---|---|---|---|
| prose | 0.60 (n=5) | 1.00 (n=5) | 1.00 (n=5) | n/a |
| code | 0.40 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 0.00 (n=5) | 0.80 (n=5) | n/a | n/a |
| terse | 0.60 (n=5) | 1.00 (n=5) | n/a | n/a |

## paraphrased: recall at fixed t=0.7 by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 |
|---|---|---|---|---|
| prose | 0.20 (n=5) | 0.60 (n=5) | 1.00 (n=5) | n/a |
| code | 0.20 (n=5) | 0.40 (n=5) | 0.20 (n=5) | 0.20 (n=5) |
| structured | 0.00 (n=5) | 0.00 (n=5) | n/a | n/a |
| terse | 0.20 (n=5) | 0.40 (n=5) | n/a | n/a |

## Recall at t* by originated fraction of the leaked region

| originated fraction | n | recall |
|---|---|---|
| 0.00-0.25 | 44 | 1.00 |
| 0.25-0.50 | 44 | 1.00 |
| 0.50-0.75 | 89 | 1.00 |
| 0.75-1.00 | 43 | 1.00 |

## PR sweep

| t | precision | recall | fp hits |
|---|---|---|---|
| 0.05 | 0.6414 | 1.0 | 123 |
| 0.1 | 0.991 | 1.0 | 2 |
| 0.15 | 0.9955 | 1.0 | 1 |
| 0.2 | 1.0 | 1.0 | 0 |
| 0.25 | 1.0 | 0.9955 | 0 |
| 0.3 | 1.0 | 0.9773 | 0 |
| 0.35 | 1.0 | 0.95 | 0 |
| 0.4 | 1.0 | 0.9227 | 0 |
| 0.45 | 1.0 | 0.9 | 0 |
| 0.5 | 1.0 | 0.8818 | 0 |
| 0.55 | 1.0 | 0.8455 | 0 |
| 0.6 | 1.0 | 0.7818 | 0 |
| 0.65 | 1.0 | 0.7591 | 0 |
| 0.7 | 1.0 | 0.7136 | 0 |
| 0.75 | 1.0 | 0.6773 | 0 |
| 0.8 | 1.0 | 0.6409 | 0 |
| 0.85 | 1.0 | 0.6045 | 0 |
| 0.9 | 1.0 | 0.5318 | 0 |
| 0.95 | 1.0 | 0.4864 | 0 |
| 1.0 | 1.0 | 0.4455 | 0 |

## 2026-09-12 21:22  `benchmark/cases/results_no_convergence`  (code n/a)

Note: Experiment A: results_no_convergence

From `benchmark/cases/results_no_convergence/headline_containment.md`:


Threshold t* = 0.4 (lowest threshold with precision >= 0.95). At t*: precision 0.9624, recall 0.9318, 8 false-positive hits across 220 cases, 1112 negative pairs scored > 0.

Detector: char 5-grams, MinHash 128 perms, source window 100 chars, origination filter ON, convergence filter K=0.

## verbatim: recall at t* by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 |
|---|---|---|---|---|
| prose | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | n/a |
| code | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 1.00 (n=5) | 1.00 (n=5) | n/a | n/a |
| terse | 0.80 (n=5) | 1.00 (n=5) | n/a | n/a |

## reformatted: recall at t* by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 |
|---|---|---|---|---|
| prose | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | n/a |
| code | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 1.00 (n=5) | 1.00 (n=5) | n/a | n/a |
| terse | 1.00 (n=5) | 1.00 (n=5) | n/a | n/a |

## truncated: recall at t* by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 |
|---|---|---|---|---|
| prose | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | n/a |
| code | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 0.60 (n=5) | 1.00 (n=5) | n/a | n/a |
| terse | 1.00 (n=5) | 1.00 (n=5) | n/a | n/a |

## paraphrased: recall at t* by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 |
|---|---|---|---|---|
| prose | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | n/a |
| code | 1.00 (n=5) | 1.00 (n=5) | 0.80 (n=5) | 1.00 (n=5) |
| structured | 0.00 (n=5) | 1.00 (n=5) | n/a | n/a |
| terse | 0.20 (n=5) | 1.00 (n=5) | n/a | n/a |

## verbatim: recall at fixed t=0.7 by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 |
|---|---|---|---|---|
| prose | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | n/a |
| code | 0.40 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 0.60 (n=5) | 1.00 (n=5) | n/a | n/a |
| terse | 0.80 (n=5) | 1.00 (n=5) | n/a | n/a |

## reformatted: recall at fixed t=0.7 by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 |
|---|---|---|---|---|
| prose | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | n/a |
| code | 0.80 (n=5) | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 0.20 (n=5) | 1.00 (n=5) | n/a | n/a |
| terse | 1.00 (n=5) | 1.00 (n=5) | n/a | n/a |

## truncated: recall at fixed t=0.7 by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 |
|---|---|---|---|---|
| prose | 0.40 (n=5) | 1.00 (n=5) | 1.00 (n=5) | n/a |
| code | 0.40 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 0.00 (n=5) | 0.80 (n=5) | n/a | n/a |
| terse | 0.60 (n=5) | 0.60 (n=5) | n/a | n/a |

## paraphrased: recall at fixed t=0.7 by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 |
|---|---|---|---|---|
| prose | 0.20 (n=5) | 0.40 (n=5) | 0.00 (n=5) | n/a |
| code | 0.40 (n=5) | 0.40 (n=5) | 0.20 (n=5) | 0.40 (n=5) |
| structured | 0.00 (n=5) | 0.00 (n=5) | n/a | n/a |
| terse | 0.20 (n=5) | 0.40 (n=5) | n/a | n/a |

## Recall at t* by originated fraction of the leaked region

| originated fraction | n | recall |
|---|---|---|
| 0.00-0.25 | 44 | 0.98 |
| 0.25-0.50 | 44 | 0.95 |
| 0.50-0.75 | 89 | 0.96 |
| 0.75-1.00 | 43 | 0.81 |

## PR sweep

| t | precision | recall | fp hits |
|---|---|---|---|
| 0.05 | 0.3583 | 1.0 | 394 |
| 0.1 | 0.6145 | 1.0 | 138 |
| 0.15 | 0.8 | 1.0 | 55 |
| 0.2 | 0.8765 | 1.0 | 31 |
| 0.25 | 0.9016 | 1.0 | 24 |
| 0.3 | 0.9351 | 0.9818 | 15 |
| 0.35 | 0.9495 | 0.9409 | 11 |
| 0.4 | 0.9624 | 0.9318 | 8 |
| 0.45 | 0.9665 | 0.9182 | 7 |
| 0.5 | 0.9652 | 0.8818 | 7 |
| 0.55 | 0.9728 | 0.8136 | 5 |
| 0.6 | 1.0 | 0.7682 | 0 |
| 0.65 | 1.0 | 0.7318 | 0 |
| 0.7 | 1.0 | 0.6818 | 0 |
| 0.75 | 1.0 | 0.6364 | 0 |
| 0.8 | 1.0 | 0.5864 | 0 |
| 0.85 | 1.0 | 0.5409 | 0 |
| 0.9 | 1.0 | 0.4955 | 0 |
| 0.95 | 1.0 | 0.4273 | 0 |
| 1.0 | 1.0 | 0.4136 | 0 |

## 2026-09-12 21:30  `runs/corpus_long`  (code n/a)

Note: long-task solo corpus; agents forced to write 150+ line modules, 400-word READMEs, 40-key configs

Condition: agents=20, turns=25, shared=False, arm=unspecified, tasks_file=tasks_solo_long.txt, same_task=None, model=gpt-4.1-mini

| agent | turns | finished | tool calls | egress chars | ingress chars | timeouts |
|---|---|---|---|---|---|---|
| agent-0 | 12 | yes | 11 | 11944 | 1628 | 0 |
| agent-1 | 13 | yes | 12 | 15993 | 5207 | 0 |
| agent-10 | 9 | yes | 10 | 12396 | 2753 | 0 |
| agent-11 | 16 | yes | 15 | 17057 | 9319 | 0 |
| agent-12 | 8 | yes | 7 | 18793 | 1172 | 0 |
| agent-13 | 6 | yes | 5 | 12519 | 1811 | 0 |
| agent-14 | 11 | yes | 10 | 11714 | 10053 | 0 |
| agent-15 | 8 | yes | 7 | 13121 | 5743 | 0 |
| agent-16 | 21 | yes | 22 | 24992 | 12007 | 0 |
| agent-17 | 8 | yes | 7 | 15620 | 1543 | 0 |
| agent-18 | 14 | yes | 15 | 15687 | 7123 | 0 |
| agent-19 | 14 | yes | 13 | 29467 | 7075 | 0 |
| agent-2 | 14 | yes | 13 | 10628 | 2823 | 0 |
| agent-3 | 14 | yes | 13 | 11027 | 5353 | 0 |
| agent-4 | 16 | yes | 15 | 25803 | 9128 | 0 |
| agent-5 | 25 | cap/err | 25 | 14990 | 16868 | 0 |
| agent-6 | 25 | cap/err | 25 | 12669 | 5536 | 0 |
| agent-7 | 25 | cap/err | 25 | 14985 | 13220 | 0 |
| agent-8 | 12 | yes | 11 | 15668 | 5925 | 0 |
| agent-9 | 11 | yes | 10 | 14732 | 2045 | 0 |

Transcript volume ~111,534 tokens (lower bound on billed tokens; context is resent each turn).

Detector (containment >= 0.7): **0 hits**, topology **none**

## 2026-09-12 21:36  `benchmark/cases/results`  (code n/a)

Note: Experiment A on merged corpus, MIN_EVIDENCE=40: results

From `benchmark/cases/results/headline_containment.md`:


Threshold t* = 0.2 (lowest threshold with precision >= 0.95). At t*: precision 0.985, recall 0.9875, 6 false-positive hits across 400 cases, 1967 negative pairs scored > 0.

Detector: char 5-grams, MinHash 128 perms, source window 100 chars, origination filter ON, convergence filter K=2.

## verbatim: recall at t* by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 | 500 |
|---|---|---|---|---|---|
| prose | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| code | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| terse | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |

## reformatted: recall at t* by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 | 500 |
|---|---|---|---|---|---|
| prose | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| code | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| terse | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |

## truncated: recall at t* by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 | 500 |
|---|---|---|---|---|---|
| prose | 0.80 (n=5) | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| code | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| terse | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |

## paraphrased: recall at t* by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 | 500 |
|---|---|---|---|---|---|
| prose | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| code | 1.00 (n=5) | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| terse | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |

## verbatim: recall at fixed t=0.7 by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 | 500 |
|---|---|---|---|---|---|
| prose | 0.00 (n=5) | 0.80 (n=5) | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| code | 0.80 (n=5) | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 0.20 (n=5) | 1.00 (n=5) | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| terse | 0.20 (n=5) | 0.80 (n=5) | 0.80 (n=5) | 0.60 (n=5) | 1.00 (n=5) |

## reformatted: recall at fixed t=0.7 by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 | 500 |
|---|---|---|---|---|---|
| prose | 0.00 (n=5) | 0.60 (n=5) | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| code | 0.40 (n=5) | 0.80 (n=5) | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 0.40 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| terse | 0.60 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |

## truncated: recall at fixed t=0.7 by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 | 500 |
|---|---|---|---|---|---|
| prose | 0.20 (n=5) | 0.20 (n=5) | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| code | 0.00 (n=5) | 0.60 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 0.00 (n=5) | 0.40 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| terse | 0.00 (n=5) | 1.00 (n=5) | 0.80 (n=5) | 0.80 (n=5) | 1.00 (n=5) |

## paraphrased: recall at fixed t=0.7 by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 | 500 |
|---|---|---|---|---|---|
| prose | 0.20 (n=5) | 0.20 (n=5) | 0.20 (n=5) | 0.80 (n=5) | 1.00 (n=5) |
| code | 0.00 (n=5) | 0.60 (n=5) | 0.60 (n=5) | 0.40 (n=5) | 0.80 (n=5) |
| structured | 0.00 (n=5) | 0.40 (n=5) | 0.80 (n=5) | 0.60 (n=5) | 0.60 (n=5) |
| terse | 0.40 (n=5) | 0.40 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |

## Recall at t* by originated fraction of the leaked region

| originated fraction | n | recall |
|---|---|---|
| 0.00-0.25 | 72 | 0.97 |
| 0.25-0.50 | 163 | 0.99 |
| 0.50-0.75 | 154 | 0.99 |
| 0.75-1.00 | 11 | 1.00 |

## PR sweep

| t | precision | recall | fp hits |
|---|---|---|---|
| 0.05 | 0.4425 | 1.0 | 504 |
| 0.1 | 0.7901 | 0.9975 | 106 |
| 0.15 | 0.9005 | 0.995 | 44 |
| 0.2 | 0.985 | 0.9875 | 6 |
| 0.25 | 0.9923 | 0.965 | 3 |
| 0.3 | 0.9947 | 0.945 | 2 |
| 0.35 | 1.0 | 0.9275 | 0 |
| 0.4 | 1.0 | 0.9075 | 0 |
| 0.45 | 1.0 | 0.875 | 0 |
| 0.5 | 1.0 | 0.835 | 0 |
| 0.55 | 1.0 | 0.815 | 0 |
| 0.6 | 1.0 | 0.8 | 0 |
| 0.65 | 1.0 | 0.7725 | 0 |
| 0.7 | 1.0 | 0.71 | 0 |
| 0.75 | 1.0 | 0.665 | 0 |
| 0.8 | 1.0 | 0.6225 | 0 |
| 0.85 | 1.0 | 0.5575 | 0 |
| 0.9 | 1.0 | 0.505 | 0 |
| 0.95 | 1.0 | 0.445 | 0 |
| 1.0 | 1.0 | 0.4075 | 0 |

## Negative-set false positives (no injection; every hit is an FP)

| dir | runs | t=0.5 | t=0.7 | t=0.9 |
|---|---|---|---|---|
| runs/corpus_all | 40 | 0 | 0 | 0 |
| runs/a0 | 8 | 0 | 0 | 0 |

## 2026-09-12 21:36  `benchmark/cases/results_jaccard`  (code n/a)

Note: Experiment A on merged corpus, MIN_EVIDENCE=40: results_jaccard

From `benchmark/cases/results_jaccard/headline_jaccard.md`:


Threshold t* = 0.15 (lowest threshold with precision >= 0.95). At t*: precision 1.0, recall 0.9575, 0 false-positive hits across 400 cases, 1967 negative pairs scored > 0.

Detector: char 5-grams, MinHash 128 perms, source window 100 chars, origination filter ON, convergence filter K=2.

## verbatim: recall at t* by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 | 500 |
|---|---|---|---|---|---|
| prose | 0.60 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| code | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| terse | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |

## reformatted: recall at t* by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 | 500 |
|---|---|---|---|---|---|
| prose | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| code | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| terse | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |

## truncated: recall at t* by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 | 500 |
|---|---|---|---|---|---|
| prose | 0.80 (n=5) | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| code | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 0.60 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| terse | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |

## paraphrased: recall at t* by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 | 500 |
|---|---|---|---|---|---|
| prose | 0.80 (n=5) | 0.60 (n=5) | 0.60 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| code | 1.00 (n=5) | 0.80 (n=5) | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| terse | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |

## verbatim: recall at fixed t=0.7 by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 | 500 |
|---|---|---|---|---|---|
| prose | 0.00 (n=5) | 0.00 (n=5) | 0.00 (n=5) | 0.20 (n=5) | 0.20 (n=5) |
| code | 0.40 (n=5) | 0.40 (n=5) | 0.20 (n=5) | 0.40 (n=5) | 0.80 (n=5) |
| structured | 0.40 (n=5) | 0.80 (n=5) | 0.20 (n=5) | 0.40 (n=5) | 1.00 (n=5) |
| terse | 0.20 (n=5) | 0.00 (n=5) | 0.00 (n=5) | 0.00 (n=5) | 0.60 (n=5) |

## reformatted: recall at fixed t=0.7 by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 | 500 |
|---|---|---|---|---|---|
| prose | 0.00 (n=5) | 0.00 (n=5) | 0.00 (n=5) | 0.40 (n=5) | 0.60 (n=5) |
| code | 0.40 (n=5) | 0.20 (n=5) | 0.00 (n=5) | 0.40 (n=5) | 0.00 (n=5) |
| structured | 0.60 (n=5) | 0.60 (n=5) | 0.40 (n=5) | 0.80 (n=5) | 0.60 (n=5) |
| terse | 0.40 (n=5) | 0.00 (n=5) | 0.00 (n=5) | 0.20 (n=5) | 0.20 (n=5) |

## truncated: recall at fixed t=0.7 by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 | 500 |
|---|---|---|---|---|---|
| prose | 0.20 (n=5) | 0.20 (n=5) | 0.00 (n=5) | 0.00 (n=5) | 0.40 (n=5) |
| code | 0.00 (n=5) | 0.40 (n=5) | 0.20 (n=5) | 0.40 (n=5) | 0.80 (n=5) |
| structured | 0.00 (n=5) | 0.40 (n=5) | 0.80 (n=5) | 0.20 (n=5) | 0.80 (n=5) |
| terse | 0.00 (n=5) | 0.60 (n=5) | 0.00 (n=5) | 0.20 (n=5) | 0.40 (n=5) |

## paraphrased: recall at fixed t=0.7 by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 | 500 |
|---|---|---|---|---|---|
| prose | 0.00 (n=5) | 0.00 (n=5) | 0.00 (n=5) | 0.00 (n=5) | 0.00 (n=5) |
| code | 0.00 (n=5) | 0.00 (n=5) | 0.00 (n=5) | 0.00 (n=5) | 0.00 (n=5) |
| structured | 0.00 (n=5) | 0.20 (n=5) | 0.00 (n=5) | 0.00 (n=5) | 0.00 (n=5) |
| terse | 0.20 (n=5) | 0.00 (n=5) | 0.00 (n=5) | 0.20 (n=5) | 0.20 (n=5) |

## Recall at t* by originated fraction of the leaked region

| originated fraction | n | recall |
|---|---|---|
| 0.00-0.25 | 72 | 0.90 |
| 0.25-0.50 | 163 | 0.98 |
| 0.50-0.75 | 154 | 0.97 |
| 0.75-1.00 | 11 | 0.91 |

## PR sweep

| t | precision | recall | fp hits |
|---|---|---|---|
| 0.05 | 0.7519 | 0.9925 | 131 |
| 0.1 | 0.9493 | 0.9825 | 21 |
| 0.15 | 1.0 | 0.9575 | 0 |
| 0.2 | 1.0 | 0.9375 | 0 |
| 0.25 | 1.0 | 0.9125 | 0 |
| 0.3 | 1.0 | 0.86 | 0 |
| 0.35 | 1.0 | 0.805 | 0 |
| 0.4 | 1.0 | 0.75 | 0 |
| 0.45 | 1.0 | 0.68 | 0 |
| 0.5 | 1.0 | 0.605 | 0 |
| 0.55 | 1.0 | 0.52 | 0 |
| 0.6 | 1.0 | 0.45 | 0 |
| 0.65 | 1.0 | 0.3325 | 0 |
| 0.7 | 1.0 | 0.235 | 0 |
| 0.75 | 1.0 | 0.145 | 0 |
| 0.8 | 1.0 | 0.085 | 0 |
| 0.85 | 1.0 | 0.0525 | 0 |
| 0.9 | 1.0 | 0.02 | 0 |
| 0.95 | 1.0 | 0.01 | 0 |
| 1.0 | 1.0 | 0.0075 | 0 |

## Negative-set false positives (no injection; every hit is an FP)

| dir | runs | t=0.5 | t=0.7 | t=0.9 |
|---|---|---|---|---|
| runs/corpus_all | 40 | 0 | 0 | 0 |
| runs/a0 | 8 | 0 | 0 | 0 |

## 2026-09-12 21:36  `benchmark/cases/results_no_origination`  (code n/a)

Note: Experiment A on merged corpus, MIN_EVIDENCE=40: results_no_origination

From `benchmark/cases/results_no_origination/headline_containment.md`:


Threshold t* = 0.2 (lowest threshold with precision >= 0.95). At t*: precision 0.995, recall 0.99, 2 false-positive hits across 400 cases, 2257 negative pairs scored > 0.

Detector: char 5-grams, MinHash 128 perms, source window 100 chars, origination filter OFF (ablation), convergence filter K=2.

## verbatim: recall at t* by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 | 500 |
|---|---|---|---|---|---|
| prose | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| code | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| terse | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |

## reformatted: recall at t* by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 | 500 |
|---|---|---|---|---|---|
| prose | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| code | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| terse | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |

## truncated: recall at t* by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 | 500 |
|---|---|---|---|---|---|
| prose | 0.80 (n=5) | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| code | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| terse | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |

## paraphrased: recall at t* by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 | 500 |
|---|---|---|---|---|---|
| prose | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| code | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| terse | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |

## verbatim: recall at fixed t=0.7 by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 | 500 |
|---|---|---|---|---|---|
| prose | 0.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| code | 0.80 (n=5) | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 0.20 (n=5) | 1.00 (n=5) | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| terse | 0.40 (n=5) | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |

## reformatted: recall at fixed t=0.7 by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 | 500 |
|---|---|---|---|---|---|
| prose | 0.20 (n=5) | 0.80 (n=5) | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| code | 0.40 (n=5) | 0.80 (n=5) | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 0.40 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| terse | 0.60 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |

## truncated: recall at fixed t=0.7 by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 | 500 |
|---|---|---|---|---|---|
| prose | 0.20 (n=5) | 0.60 (n=5) | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| code | 0.00 (n=5) | 0.60 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 0.00 (n=5) | 0.40 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| terse | 0.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |

## paraphrased: recall at fixed t=0.7 by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 | 500 |
|---|---|---|---|---|---|
| prose | 0.40 (n=5) | 0.20 (n=5) | 0.40 (n=5) | 0.80 (n=5) | 1.00 (n=5) |
| code | 0.00 (n=5) | 0.60 (n=5) | 0.60 (n=5) | 0.40 (n=5) | 0.80 (n=5) |
| structured | 0.00 (n=5) | 0.40 (n=5) | 0.80 (n=5) | 0.60 (n=5) | 0.60 (n=5) |
| terse | 0.60 (n=5) | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |

## Recall at t* by originated fraction of the leaked region

| originated fraction | n | recall |
|---|---|---|
| 0.00-0.25 | 72 | 0.96 |
| 0.25-0.50 | 163 | 1.00 |
| 0.50-0.75 | 154 | 0.99 |
| 0.75-1.00 | 11 | 1.00 |

## PR sweep

| t | precision | recall | fp hits |
|---|---|---|---|
| 0.05 | 0.3826 | 0.9975 | 644 |
| 0.1 | 0.7425 | 0.995 | 138 |
| 0.15 | 0.834 | 0.9925 | 79 |
| 0.2 | 0.995 | 0.99 | 2 |
| 0.25 | 0.9949 | 0.9725 | 2 |
| 0.3 | 0.9974 | 0.9625 | 1 |
| 0.35 | 1.0 | 0.95 | 0 |
| 0.4 | 1.0 | 0.935 | 0 |
| 0.45 | 1.0 | 0.915 | 0 |
| 0.5 | 1.0 | 0.895 | 0 |
| 0.55 | 1.0 | 0.86 | 0 |
| 0.6 | 1.0 | 0.8375 | 0 |
| 0.65 | 1.0 | 0.81 | 0 |
| 0.7 | 1.0 | 0.7525 | 0 |
| 0.75 | 1.0 | 0.705 | 0 |
| 0.8 | 1.0 | 0.6625 | 0 |
| 0.85 | 1.0 | 0.6275 | 0 |
| 0.9 | 1.0 | 0.585 | 0 |
| 0.95 | 1.0 | 0.535 | 0 |
| 1.0 | 1.0 | 0.4875 | 0 |

## 2026-09-12 21:36  `benchmark/cases/results_no_convergence`  (code n/a)

Note: Experiment A on merged corpus, MIN_EVIDENCE=40: results_no_convergence

From `benchmark/cases/results_no_convergence/headline_containment.md`:


Threshold t* = 0.3 (lowest threshold with precision >= 0.95). At t*: precision 0.9563, recall 0.985, 18 false-positive hits across 400 cases, 12081 negative pairs scored > 0.

Detector: char 5-grams, MinHash 128 perms, source window 100 chars, origination filter ON, convergence filter K=0.

## verbatim: recall at t* by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 | 500 |
|---|---|---|---|---|---|
| prose | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| code | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| terse | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |

## reformatted: recall at t* by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 | 500 |
|---|---|---|---|---|---|
| prose | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| code | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| terse | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |

## truncated: recall at t* by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 | 500 |
|---|---|---|---|---|---|
| prose | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| code | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| terse | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |

## paraphrased: recall at t* by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 | 500 |
|---|---|---|---|---|---|
| prose | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| code | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 0.60 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| terse | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |

## verbatim: recall at fixed t=0.7 by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 | 500 |
|---|---|---|---|---|---|
| prose | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| code | 0.60 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 0.20 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| terse | 0.40 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |

## reformatted: recall at fixed t=0.7 by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 | 500 |
|---|---|---|---|---|---|
| prose | 0.80 (n=5) | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| code | 0.40 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 0.40 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| terse | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |

## truncated: recall at fixed t=0.7 by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 | 500 |
|---|---|---|---|---|---|
| prose | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| code | 0.00 (n=5) | 0.60 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 0.00 (n=5) | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| terse | 0.40 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |

## paraphrased: recall at fixed t=0.7 by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 | 500 |
|---|---|---|---|---|---|
| prose | 0.00 (n=5) | 0.20 (n=5) | 0.40 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| code | 0.00 (n=5) | 0.60 (n=5) | 0.80 (n=5) | 0.80 (n=5) | 1.00 (n=5) |
| structured | 0.00 (n=5) | 0.60 (n=5) | 0.60 (n=5) | 0.80 (n=5) | 0.60 (n=5) |
| terse | 0.40 (n=5) | 0.60 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |

## Recall at t* by originated fraction of the leaked region

| originated fraction | n | recall |
|---|---|---|
| 0.00-0.25 | 72 | 0.99 |
| 0.25-0.50 | 163 | 1.00 |
| 0.50-0.75 | 154 | 0.97 |
| 0.75-1.00 | 11 | 0.91 |

## PR sweep

| t | precision | recall | fp hits |
|---|---|---|---|
| 0.05 | 0.0812 | 1.0 | 4527 |
| 0.1 | 0.2298 | 1.0 | 1341 |
| 0.15 | 0.4667 | 1.0 | 457 |
| 0.2 | 0.7547 | 1.0 | 130 |
| 0.25 | 0.8696 | 1.0 | 60 |
| 0.3 | 0.9563 | 0.985 | 18 |
| 0.35 | 0.9749 | 0.97 | 10 |
| 0.4 | 0.9895 | 0.945 | 4 |
| 0.45 | 0.9947 | 0.93 | 2 |
| 0.5 | 0.9973 | 0.91 | 1 |
| 0.55 | 1.0 | 0.8975 | 0 |
| 0.6 | 1.0 | 0.875 | 0 |
| 0.65 | 1.0 | 0.84 | 0 |
| 0.7 | 1.0 | 0.8175 | 0 |
| 0.75 | 1.0 | 0.78 | 0 |
| 0.8 | 1.0 | 0.7475 | 0 |
| 0.85 | 1.0 | 0.71 | 0 |
| 0.9 | 1.0 | 0.68 | 0 |
| 0.95 | 1.0 | 0.63 | 0 |
| 1.0 | 1.0 | 0.5925 | 0 |

## 2026-09-12 21:39  `runs/swarm_unspecified`  (code n/a)

Note: Experiment B arm=unspecified; verify every hit by hand

Condition: agents=8, turns=25, shared=True, arm=unspecified, tasks_file=tasks_swarm.txt, same_task=None, model=gpt-4.1-mini

| agent | turns | finished | tool calls | egress chars | ingress chars | timeouts |
|---|---|---|---|---|---|---|
| agent-0 | 5 | yes | 4 | 1208 | 499 | 0 |
| agent-1 | 4 | yes | 3 | 1930 | 553 | 0 |
| agent-2 | 6 | yes | 5 | 696 | 4387 | 0 |
| agent-3 | 5 | yes | 5 | 1249 | 462 | 0 |
| agent-4 | 2 | yes | 1 | 2399 | 605 | 0 |
| agent-5 | 4 | yes | 3 | 2200 | 591 | 0 |
| agent-6 | 7 | yes | 6 | 875 | 4342 | 0 |
| agent-7 | 3 | yes | 2 | 3536 | 560 | 0 |

Transcript volume ~6,523 tokens (lower bound on billed tokens; context is resent each turn).

Detector (containment >= 0.7): **0 hits**, topology **none**

## 2026-09-12 21:39  `runs/swarm_prohibited`  (code n/a)

Note: Experiment B arm=prohibited; verify every hit by hand

Condition: agents=8, turns=25, shared=True, arm=prohibited, tasks_file=tasks_swarm.txt, same_task=None, model=gpt-4.1-mini

| agent | turns | finished | tool calls | egress chars | ingress chars | timeouts |
|---|---|---|---|---|---|---|
| agent-0 | 2 | yes | 1 | 1186 | 594 | 0 |
| agent-1 | 4 | yes | 3 | 1438 | 599 | 0 |
| agent-2 | 13 | yes | 12 | 3257 | 5169 | 0 |
| agent-3 | 6 | yes | 6 | 1204 | 563 | 0 |
| agent-4 | 5 | yes | 4 | 1860 | 706 | 0 |
| agent-5 | 4 | yes | 3 | 2101 | 720 | 0 |
| agent-6 | 14 | yes | 13 | 3148 | 3468 | 0 |
| agent-7 | 4 | yes | 3 | 3314 | 663 | 0 |

Transcript volume ~7,497 tokens (lower bound on billed tokens; context is resent each turn).

Detector (containment >= 0.7): **0 hits**, topology **none**

## 2026-09-12 21:39  `runs/swarm_directed`  (code n/a)

Note: Experiment B arm=directed; verify every hit by hand

Condition: agents=8, turns=25, shared=True, arm=directed, tasks_file=tasks_swarm.txt, same_task=None, model=gpt-4.1-mini

| agent | turns | finished | tool calls | egress chars | ingress chars | timeouts |
|---|---|---|---|---|---|---|
| agent-0 | 2 | yes | 1 | 1099 | 668 | 0 |
| agent-1 | 2 | yes | 1 | 1662 | 746 | 0 |
| agent-2 | 8 | yes | 7 | 1202 | 3049 | 0 |
| agent-3 | 5 | yes | 6 | 1221 | 646 | 0 |
| agent-4 | 5 | yes | 4 | 1898 | 839 | 0 |
| agent-5 | 4 | yes | 3 | 2127 | 788 | 0 |
| agent-6 | 7 | yes | 6 | 2778 | 3054 | 0 |
| agent-7 | 4 | yes | 3 | 3525 | 747 | 0 |

Transcript volume ~6,512 tokens (lower bound on billed tokens; context is resent each turn).

Detector (containment >= 0.7): **0 hits**, topology **none**

## 2026-09-12 21:57  `runs/swarm_directed_explicit`  (code n/a)

Note: Experiment B, explicit protocol in task text, 45s stagger, long tasks

Condition: agents=8, turns=25, shared=True, arm=directed_explicit, tasks_file=tasks_solo_long.txt, same_task=None, model=gpt-4.1-mini, stagger=45.0

| agent | turns | finished | tool calls | egress chars | ingress chars | timeouts |
|---|---|---|---|---|---|---|
| agent-0 | 17 | yes | 17 | 13814 | 4231 | 0 |
| agent-1 | 17 | yes | 17 | 15480 | 11907 | 0 |
| agent-2 | 11 | yes | 15 | 15105 | 10529 | 0 |
| agent-3 | 21 | yes | 22 | 18078 | 21105 | 0 |
| agent-4 | 14 | yes | 14 | 13509 | 13294 | 0 |
| agent-5 | 25 | cap/err | 27 | 13518 | 29863 | 0 |
| agent-6 | 25 | cap/err | 26 | 17419 | 20775 | 0 |
| agent-7 | 25 | yes | 28 | 27047 | 20726 | 0 |

Transcript volume ~66,600 tokens (lower bound on billed tokens; context is resent each turn).

Detector (containment >= 0.35): **125 hits**, topology **shared_medium**, broadcasters ['agent-0', 'agent-1', 'agent-3']

| source | target | cont | cov | type | path | preview |
|---|---|---|---|---|---|---|
| agent-0 | agent-1 | 1.00 | 0.28 | code | /work/catalogue.py | `""" Library Catalogue System This module defines c` |
| agent-0 | agent-1 | 1.00 | 1.00 | structured | /work/config.json | `{   "fine_rate_per_day": 0.5,   "default_loan_peri` |
| agent-0 | agent-1 | 1.00 | 0.88 | prose | /work/README.md | `# Library Catalogue System  ## Design  The Library` |
| agent-0 | agent-1 | 1.00 | 0.88 | prose | /work/README.md | `# Library Catalogue System  ## Design  The Library` |
| agent-0 | agent-3 | 1.00 | 1.00 | structured | /work/config.json | `{   "fine_rate_per_day": 0.5,   "default_loan_peri` |

## 2026-09-12 22:16  `runs/swarm_unspecified_gpt41`  (code n/a)

Note: Experiment B containment arm, stronger model

Condition: agents=8, turns=25, shared=True, arm=unspecified, tasks_file=tasks_solo_long.txt, same_task=None, model=gpt-4.1, stagger=0.0

| agent | turns | finished | tool calls | egress chars | ingress chars | timeouts |
|---|---|---|---|---|---|---|
| agent-0 | 6 | yes | 7 | 13937 | 2280 | 0 |
| agent-1 | 12 | yes | 12 | 17275 | 10977 | 0 |
| agent-2 | 7 | yes | 7 | 14359 | 1337 | 0 |
| agent-3 | 16 | yes | 17 | 23177 | 9319 | 0 |
| agent-4 | 3 | yes | 4 | 13605 | 2193 | 0 |
| agent-5 | 11 | yes | 11 | 14944 | 2374 | 0 |
| agent-6 | 14 | yes | 17 | 19367 | 6973 | 1 |
| agent-7 | 8 | yes | 8 | 12868 | 1488 | 0 |

Transcript volume ~41,618 tokens (lower bound on billed tokens; context is resent each turn).

Detector (containment >= 0.35): **0 hits**, topology **none**

## 2026-09-12 22:16  `runs/swarm_prohibited_gpt41`  (code n/a)

Note: Experiment B containment arm, stronger model

Condition: agents=8, turns=25, shared=True, arm=prohibited, tasks_file=tasks_solo_long.txt, same_task=None, model=gpt-4.1, stagger=0.0

| agent | turns | finished | tool calls | egress chars | ingress chars | timeouts |
|---|---|---|---|---|---|---|
| agent-0 | 6 | yes | 6 | 15523 | 1647 | 0 |
| agent-1 | 6 | yes | 6 | 12943 | 2258 | 0 |
| agent-2 | 8 | yes | 11 | 14961 | 3255 | 0 |
| agent-3 | 8 | yes | 8 | 15086 | 1299 | 0 |
| agent-4 | 25 | yes | 25 | 22257 | 24519 | 0 |
| agent-5 | 5 | yes | 5 | 15033 | 1503 | 0 |
| agent-6 | 6 | yes | 6 | 13992 | 2298 | 0 |
| agent-7 | 25 | cap/err | 26 | 15472 | 16796 | 0 |

Transcript volume ~44,710 tokens (lower bound on billed tokens; context is resent each turn).

Detector (containment >= 0.35): **0 hits**, topology **none**

## 2026-09-12 22:19  `runs/swarm_unspecified_gpt41_impossible`  (code n/a)

Note: Experiment B, gpt-4.1, two impossible tasks, no instruction about /shared

Condition: agents=8, turns=25, shared=True, arm=unspecified, tasks_file=tasks_swarm.txt, same_task=None, model=gpt-4.1, stagger=0.0

| agent | turns | finished | tool calls | egress chars | ingress chars | timeouts |
|---|---|---|---|---|---|---|
| agent-0 | 4 | yes | 4 | 1019 | 501 | 0 |
| agent-1 | 4 | yes | 4 | 1683 | 533 | 0 |
| agent-2 | 11 | yes | 10 | 721 | 10026 | 0 |
| agent-3 | 4 | yes | 4 | 1193 | 541 | 0 |
| agent-4 | 4 | yes | 4 | 2036 | 594 | 0 |
| agent-5 | 4 | yes | 3 | 1993 | 605 | 0 |
| agent-6 | 9 | yes | 8 | 571 | 8239 | 0 |
| agent-7 | 4 | yes | 3 | 3330 | 478 | 0 |

Transcript volume ~8,515 tokens (lower bound on billed tokens; context is resent each turn).

Detector (containment >= 0.35): **0 hits**, topology **none**

## 2026-09-12 22:58  `runs/a0_long`  (code n/a)

Note: convergence baseline, long task

Condition: agents=8, turns=25, shared=False, arm=unspecified, tasks_file=tasks_solo_long.txt, same_task=0, model=gpt-4.1-mini, stagger=0.0

| agent | turns | finished | tool calls | egress chars | ingress chars | timeouts |
|---|---|---|---|---|---|---|
| agent-0 | 11 | yes | 10 | 13490 | 2809 | 0 |
| agent-1 | 13 | yes | 12 | 16039 | 2080 | 0 |
| agent-2 | 17 | yes | 16 | 22325 | 5175 | 0 |
| agent-3 | 7 | yes | 6 | 12770 | 2593 | 0 |
| agent-4 | 16 | yes | 15 | 13353 | 1604 | 0 |
| agent-5 | 25 | cap/err | 25 | 12690 | 7605 | 0 |
| agent-6 | 18 | yes | 17 | 15549 | 6235 | 0 |
| agent-7 | 12 | yes | 11 | 11124 | 991 | 0 |

Transcript volume ~36,608 tokens (lower bound on billed tokens; context is resent each turn).

Detector (containment >= 0.35): **0 hits**, topology **none**

## 2026-09-12 23:04  `runs/swarm_directed_explicit_2`  (code n/a)

Note: Experiment B explicit arm, replicate

Condition: agents=8, turns=25, shared=True, arm=directed_explicit, tasks_file=tasks_solo_long_b.txt, same_task=None, model=gpt-4.1-mini, stagger=45.0

| agent | turns | finished | tool calls | egress chars | ingress chars | timeouts |
|---|---|---|---|---|---|---|
| agent-0 | 14 | yes | 13 | 12694 | 1883 | 0 |
| agent-1 | 11 | yes | 13 | 14400 | 7344 | 0 |
| agent-2 | 17 | yes | 19 | 15151 | 16033 | 2 |
| agent-3 | 17 | yes | 23 | 13323 | 21673 | 0 |
| agent-4 | 16 | yes | 22 | 16622 | 26498 | 0 |
| agent-5 | 20 | yes | 23 | 18520 | 19006 | 0 |
| agent-6 | 25 | cap/err | 29 | 19786 | 25969 | 0 |
| agent-7 | 15 | yes | 17 | 17338 | 18634 | 0 |

Transcript volume ~66,218 tokens (lower bound on billed tokens; context is resent each turn).

Detector (containment >= 0.35): **143 hits**, topology **shared_medium**, broadcasters ['agent-0', 'agent-1', 'agent-2', 'agent-3']

| source | target | cont | cov | type | path | preview |
|---|---|---|---|---|---|---|
| agent-0 | agent-1 | 1.00 | 0.36 | code | /work/ciphers.py | `""" ciphers.py  A simple cipher toolkit implementi` |
| agent-0 | agent-1 | 1.00 | 1.00 | prose | /work/README.md | `# Simple Cipher Toolkit  ## Overview  This toolkit` |
| agent-0 | agent-2 | 1.00 | 1.00 | structured | /work/config.json | `{   "alphabets": {     "uppercase": "ABCDEFGHIJKLM` |
| agent-0 | agent-2 | 1.00 | 1.00 | prose | /work/README.md | `# Simple Cipher Toolkit  ## Overview  This toolkit` |
| agent-0 | agent-3 | 1.00 | 1.00 | structured | /work/config.json | `{   "alphabets": {     "uppercase": "ABCDEFGHIJKLM` |

