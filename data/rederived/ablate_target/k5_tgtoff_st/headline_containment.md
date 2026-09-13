# Experiment A headline (containment)

Threshold t* = 0.8 (lowest threshold with precision >= 0.95). At t*: precision 0.9692, recall 0.7719, 7 false-positive hits across 285 cases, 9005 negative pairs scored > 0.

Detector: char 5-grams, MinHash 128 perms, source window 100 chars, origination filter ON, convergence filter K=5, evidence floor 40, target-origination filter OFF.

## verbatim: recall at t* by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 | 500 |
|---|---|---|---|---|---|
| prose | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| code | 0.60 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 0.40 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| terse | 0.20 (n=5) | 0.60 (n=5) | 1.00 (n=5) | 1.00 (n=5) | n/a |

## reformatted: recall at t* by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 | 500 |
|---|---|---|---|---|---|
| prose | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| code | 0.20 (n=5) | 0.40 (n=5) | 0.40 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 0.40 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| terse | 0.20 (n=5) | 0.00 (n=5) | 0.60 (n=5) | 1.00 (n=5) | n/a |

## truncated: recall at t* by span length (tokens) x artifact type

| type | 25 | 50 | 100 | 200 | 500 |
|---|---|---|---|---|---|
| prose | 0.20 (n=5) | 0.60 (n=5) | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| code | 0.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 0.60 (n=5) | 1.00 (n=5) |
| structured | 0.40 (n=5) | 0.60 (n=5) | 1.00 (n=5) | 0.80 (n=5) | 1.00 (n=5) |
| terse | 0.00 (n=5) | 0.20 (n=5) | 1.00 (n=5) | 1.00 (n=5) | n/a |

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
| code | 0.80 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) |
| structured | 0.60 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 0.80 (n=5) | 1.00 (n=5) |
| terse | 0.60 (n=5) | 1.00 (n=5) | 1.00 (n=5) | 1.00 (n=5) | n/a |

## Recall at t* by originated fraction of the leaked region

| originated fraction | n | recall |
|---|---|---|
| 0.00-0.25 | 109 | 0.80 |
| 0.25-0.50 | 116 | 0.92 |
| 0.50-0.75 | 57 | 0.46 |
| 0.75-1.00 | 3 | 0.00 |

## PR sweep

| t | precision | recall | fp hits |
|---|---|---|---|
| 0.05 | 0.0504 | 1.0 | 5366 |
| 0.1 | 0.1149 | 1.0 | 2196 |
| 0.15 | 0.1737 | 1.0 | 1356 |
| 0.2 | 0.2258 | 0.9965 | 974 |
| 0.25 | 0.2337 | 0.9965 | 931 |
| 0.3 | 0.2838 | 0.9789 | 704 |
| 0.35 | 0.3611 | 0.9719 | 490 |
| 0.4 | 0.4717 | 0.9649 | 308 |
| 0.45 | 0.572 | 0.9474 | 202 |
| 0.5 | 0.6312 | 0.9368 | 156 |
| 0.55 | 0.7179 | 0.9018 | 101 |
| 0.6 | 0.7384 | 0.8912 | 90 |
| 0.65 | 0.7878 | 0.8596 | 66 |
| 0.7 | 0.9 | 0.8211 | 26 |
| 0.75 | 0.9458 | 0.7965 | 13 |
| 0.8 | 0.9692 | 0.7719 | 7 |
| 0.85 | 0.9657 | 0.6912 | 7 |
| 0.9 | 0.963 | 0.6386 | 7 |
| 0.95 | 1.0 | 0.6105 | 0 |
| 1.0 | 1.0 | 0.5754 | 0 |