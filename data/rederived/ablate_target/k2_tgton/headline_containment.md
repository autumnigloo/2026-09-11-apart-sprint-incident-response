# Experiment A headline (containment)

Threshold t* = 0.2 (lowest threshold with precision >= 0.95). At t*: precision 0.99, recall 0.9875, 4 false-positive hits across 400 cases, 1513 negative pairs scored > 0.

Detector: char 5-grams, MinHash 128 perms, source window 100 chars, origination filter ON, convergence filter K=2, evidence floor 40, target-origination filter ON.

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

## verbatim: recall at fixed t=0.35 by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 | 500 |
|---|---|---|---|---|---|
| prose | 0.40 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| code | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| terse | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |

## reformatted: recall at fixed t=0.35 by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 | 500 |
|---|---|---|---|---|---|
| prose | 0.60 (n=5) | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| code | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| terse | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |

## truncated: recall at fixed t=0.35 by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 | 500 |
|---|---|---|---|---|---|
| prose | 0.40 (n=5) | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| code | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 0.60 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| terse | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |

## paraphrased: recall at fixed t=0.35 by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 | 500 |
|---|---|---|---|---|---|
| prose | 0.60 (n=5) | 0.60 (n=5) | 0.60 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| code | 0.60 (n=5) | 0.80 (n=5) | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 0.60 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| terse | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |

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
| 0.05 | 0.5229 | 1.0 | 365 |
| 0.1 | 0.8453 | 0.9975 | 73 |
| 0.15 | 0.9149 | 0.995 | 37 |
| 0.2 | 0.99 | 0.9875 | 4 |
| 0.25 | 0.9923 | 0.965 | 3 |
| 0.3 | 0.9947 | 0.945 | 2 |
| 0.35 | 1.0 | 0.9275 | 0 |
| 0.4 | 1.0 | 0.9075 | 0 |
| 0.45 | 1.0 | 0.8725 | 0 |
| 0.5 | 1.0 | 0.835 | 0 |
| 0.55 | 1.0 | 0.815 | 0 |
| 0.6 | 1.0 | 0.8 | 0 |
| 0.65 | 1.0 | 0.7725 | 0 |
| 0.7 | 1.0 | 0.71 | 0 |
| 0.75 | 1.0 | 0.6625 | 0 |
| 0.8 | 1.0 | 0.62 | 0 |
| 0.85 | 1.0 | 0.555 | 0 |
| 0.9 | 1.0 | 0.5 | 0 |
| 0.95 | 1.0 | 0.4425 | 0 |
| 1.0 | 1.0 | 0.405 | 0 |

## Negative-set false positives (no injection; every hit is an FP)

| dir | runs | t=0.5 | t=0.7 | t=0.9 |
|---|---|---|---|---|
| data/runs/corpus_all | 40 | 0 | 0 | 0 |
| data/runs/a0 | 8 | 0 | 0 | 0 |
| data/runs/a0_long | 8 | 0 | 0 | 0 |