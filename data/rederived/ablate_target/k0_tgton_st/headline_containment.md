# Experiment A headline (containment)

Threshold t* = 0.25 (lowest threshold with precision >= 0.95). At t*: precision 1.0, recall 0.9965, 0 false-positive hits across 285 cases, 4826 negative pairs scored > 0.

Detector: char 5-grams, MinHash 128 perms, source window 100 chars, origination filter ON, convergence filter K=0, evidence floor 40, target-origination filter ON.

## verbatim: recall at t* by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 | 500 |
|---|---|---|---|---|---|
| prose | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| code | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| terse | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | n/a |

## reformatted: recall at t* by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 | 500 |
|---|---|---|---|---|---|
| prose | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| code | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| terse | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | n/a |

## truncated: recall at t* by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 | 500 |
|---|---|---|---|---|---|
| prose | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| code | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 0.80 (n=5) | 1.00 (n=5) |
| terse | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | n/a |

## verbatim: recall at fixed t=0.35 by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 | 500 |
|---|---|---|---|---|---|
| prose | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| code | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| terse | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | n/a |

## reformatted: recall at fixed t=0.35 by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 | 500 |
|---|---|---|---|---|---|
| prose | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| code | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| terse | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | n/a |

## truncated: recall at fixed t=0.35 by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 | 500 |
|---|---|---|---|---|---|
| prose | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| code | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 0.80 (n=5) | 1.00 (n=5) |
| terse | 0.60 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | n/a |

## Recall at t* by originated fraction of the leaked region

| originated fraction | n | recall |
|---|---|---|
| 0.00-0.25 | 109 | 0.99 |
| 0.25-0.50 | 116 | 1.00 |
| 0.50-0.75 | 57 | 1.00 |
| 0.75-1.00 | 3 | 1.00 |

## PR sweep

| t | precision | recall | fp hits |
|---|---|---|---|
| 0.05 | 0.1268 | 1.0 | 1963 |
| 0.1 | 0.4098 | 0.9965 | 409 |
| 0.15 | 0.5308 | 0.9965 | 251 |
| 0.2 | 0.9281 | 0.9965 | 22 |
| 0.25 | 1.0 | 0.9965 | 0 |
| 0.3 | 1.0 | 0.9789 | 0 |
| 0.35 | 1.0 | 0.9789 | 0 |
| 0.4 | 1.0 | 0.9684 | 0 |
| 0.45 | 1.0 | 0.9544 | 0 |
| 0.5 | 1.0 | 0.9333 | 0 |
| 0.55 | 1.0 | 0.9018 | 0 |
| 0.6 | 1.0 | 0.8877 | 0 |
| 0.65 | 1.0 | 0.8737 | 0 |
| 0.7 | 1.0 | 0.8456 | 0 |
| 0.75 | 1.0 | 0.814 | 0 |
| 0.8 | 1.0 | 0.7719 | 0 |
| 0.85 | 1.0 | 0.7368 | 0 |
| 0.9 | 1.0 | 0.7018 | 0 |
| 0.95 | 1.0 | 0.6702 | 0 |
| 1.0 | 1.0 | 0.614 | 0 |