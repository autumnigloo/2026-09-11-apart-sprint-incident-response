# Experiment A headline (jaccard)

Threshold t* = 0.15 (lowest threshold with precision >= 0.95). At t*: precision 1.0, recall 0.9575, 0 false-positive hits across 400 cases, 1967 negative pairs scored > 0.

Detector: char 5-grams, MinHash 128 perms, source window 100 chars, origination filter ON, convergence filter K=2, evidence floor 40.

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

## verbatim: recall at fixed t=0.35 by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 | 500 |
|---|---|---|---|---|---|
| prose | 0.40 (n=5) | 0.60 (n=5) | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| code | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| terse | 1.00 (n=5) | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |

## reformatted: recall at fixed t=0.35 by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 | 500 |
|---|---|---|---|---|---|
| prose | 0.40 (n=5) | 0.00 (n=5) | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| code | 0.60 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| terse | 0.80 (n=5) | 0.80 (n=5) | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) |

## truncated: recall at fixed t=0.35 by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 | 500 |
|---|---|---|---|---|---|
| prose | 0.40 (n=5) | 0.40 (n=5) | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| code | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 0.60 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| terse | 0.80 (n=5) | 1.00 (n=5) | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) |

## paraphrased: recall at fixed t=0.35 by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 | 500 |
|---|---|---|---|---|---|
| prose | 0.20 (n=5) | 0.20 (n=5) | 0.20 (n=5) | 0.80 (n=5) | 1.00 (n=5) |
| code | 0.20 (n=5) | 0.20 (n=5) | 0.40 (n=5) | 0.60 (n=5) | 0.60 (n=5) |
| structured | 0.20 (n=5) | 1.00 (n=5) | 0.60 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| terse | 0.40 (n=5) | 0.60 (n=5) | 0.80 (n=5) | 0.60 (n=5) | 1.00 (n=5) |

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

## Split-half check (t fitted on one half of the cases, scored on the held-out half)

| fitted t | held-out recall | held-out precision | fp hits |
|---|---|---|---|
| 0.15 | 0.95 | 1.0 | 0 |
| 0.1 | 0.99 | 0.9252 | 16 |