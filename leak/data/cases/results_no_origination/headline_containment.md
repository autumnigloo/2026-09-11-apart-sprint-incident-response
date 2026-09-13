# Experiment A headline (containment)

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