# Experiment A headline (containment)

Threshold t* = 0.55 (lowest threshold with precision >= 0.95). At t*: precision 0.9698, recall 0.9018, 8 false-positive hits across 285 cases, 5950 negative pairs scored > 0.

Detector: char 5-grams, MinHash 128 perms, source window 100 chars, origination filter ON, convergence filter K=0, evidence floor 40, target-origination filter OFF.

## verbatim: recall at t* by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 | 500 |
|---|---|---|---|---|---|
| prose | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| code | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| terse | 1.00 (n=5) | 0.60 (n=5) | 1.00 (n=5) | 1.00 (n=5) | n/a |

## reformatted: recall at t* by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 | 500 |
|---|---|---|---|---|---|
| prose | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| code | 0.20 (n=5) | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| terse | 0.40 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | n/a |

## truncated: recall at t* by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 | 500 |
|---|---|---|---|---|---|
| prose | 0.40 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| code | 0.20 (n=5) | 1.00 (n=5) | 0.80 (n=5) | 0.80 (n=5) | 1.00 (n=5) |
| structured | 0.60 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 0.80 (n=5) | 1.00 (n=5) |
| terse | 0.00 (n=5) | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) | n/a |

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
| 0.00-0.25 | 109 | 0.89 |
| 0.25-0.50 | 116 | 0.97 |
| 0.50-0.75 | 57 | 0.82 |
| 0.75-1.00 | 3 | 0.00 |

## PR sweep

| t | precision | recall | fp hits |
|---|---|---|---|
| 0.05 | 0.103 | 1.0 | 2483 |
| 0.1 | 0.3205 | 0.9965 | 602 |
| 0.15 | 0.4343 | 0.9965 | 370 |
| 0.2 | 0.7493 | 0.9965 | 95 |
| 0.25 | 0.8503 | 0.9965 | 50 |
| 0.3 | 0.9 | 0.9789 | 31 |
| 0.35 | 0.93 | 0.9789 | 21 |
| 0.4 | 0.9452 | 0.9684 | 16 |
| 0.45 | 0.9444 | 0.9544 | 16 |
| 0.5 | 0.9466 | 0.9333 | 15 |
| 0.55 | 0.9698 | 0.9018 | 8 |
| 0.6 | 0.9768 | 0.8877 | 6 |
| 0.65 | 0.9803 | 0.8737 | 5 |
| 0.7 | 0.9837 | 0.8456 | 4 |
| 0.75 | 0.9872 | 0.814 | 3 |
| 0.8 | 0.9955 | 0.7719 | 1 |
| 0.85 | 0.9953 | 0.7368 | 1 |
| 0.9 | 0.995 | 0.7018 | 1 |
| 0.95 | 0.9948 | 0.6702 | 1 |
| 1.0 | 1.0 | 0.614 | 0 |