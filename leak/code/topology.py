"""
Classify the N x N cross-run hit matrix produced by detector.py.

Labels per source run and for the fleet:
  none          no hits above threshold
  directed      A -> B only, for some pairs (each edge one-way)
  bidirectional at least one pair with A -> B and B -> A
  shared_medium one source reaches >= FANOUT targets (one-key-everywhere)

Usage:
    python topology.py hits.json                 # from detector.py --out
    python topology.py hits.json --fanout 3
    python topology.py hits.json --svg topo.svg  # optional picture
"""

from __future__ import annotations

import argparse
import json
import pathlib

FANOUT = 3


def classify(runs: list[str], m: list[list[int]], fanout: int = FANOUT) -> dict:
    n = len(runs)
    edges = [(runs[i], runs[j], m[i][j]) for i in range(n) for j in range(n) if i != j and m[i][j] > 0]
    directed, bidirectional = [], []
    seen = set()
    for i in range(n):
        for j in range(n):
            if i == j or m[i][j] == 0 or (j, i) in seen:
                continue
            if m[j][i] > 0:
                bidirectional.append((runs[i], runs[j], m[i][j], m[j][i]))
                seen.add((i, j))
            else:
                directed.append((runs[i], runs[j], m[i][j]))
    sources = {runs[i]: sum(1 for j in range(n) if i != j and m[i][j] > 0) for i in range(n)}
    broadcasters = [r for r, k in sources.items() if k >= fanout]
    if not edges:
        label = "none"
    elif broadcasters:
        label = "shared_medium"
    elif bidirectional:
        label = "bidirectional"
    else:
        label = "directed"
    return {
        "label": label,
        "n_runs": n,
        "n_edges": len(edges),
        "directed_edges": directed,
        "bidirectional_pairs": bidirectional,
        "fanout_per_source": sources,
        "broadcasters": broadcasters,
        "fanout_threshold": fanout,
    }


def render_svg(runs: list[str], m: list[list[int]], path: pathlib.Path):
    import math
    n = len(runs)
    R, cx, cy = 180, 260, 240
    pos = {i: (cx + R * math.cos(2 * math.pi * i / n), cy + R * math.sin(2 * math.pi * i / n)) for i in range(n)}
    out = ['<svg xmlns="http://www.w3.org/2000/svg" width="520" height="480" font-family="sans-serif" font-size="11">',
           '<defs><marker id="a" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">'
           '<path d="M0,0 L8,4 L0,8 z" fill="#444"/></marker></defs>']
    for i in range(n):
        for j in range(n):
            if i != j and m[i][j] > 0:
                (x1, y1), (x2, y2) = pos[i], pos[j]
                dx, dy = x2 - x1, y2 - y1
                d = math.hypot(dx, dy) or 1
                x1s, y1s = x1 + 22 * dx / d, y1 + 22 * dy / d
                x2s, y2s = x2 - 22 * dx / d, y2 - 22 * dy / d
                w = 1 + min(4, m[i][j] / 2)
                out.append(f'<line x1="{x1s:.0f}" y1="{y1s:.0f}" x2="{x2s:.0f}" y2="{y2s:.0f}" '
                           f'stroke="#444" stroke-width="{w:.1f}" marker-end="url(#a)"/>')
    for i, r in enumerate(runs):
        x, y = pos[i]
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="20" fill="#eef" stroke="#336"/>')
        out.append(f'<text x="{x:.0f}" y="{y + 4:.0f}" text-anchor="middle">{r[-8:]}</text>')
    out.append("</svg>")
    path.write_text("\n".join(out))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("hits_json", type=pathlib.Path)
    ap.add_argument("--fanout", type=int, default=FANOUT)
    ap.add_argument("--svg", type=pathlib.Path)
    args = ap.parse_args()
    d = json.loads(args.hits_json.read_text())
    runs, m = d["matrix"]["runs"], d["matrix"]["matrix"]
    res = classify(runs, m, args.fanout)
    print(json.dumps(res, indent=1))
    if args.svg:
        render_svg(runs, m, args.svg)
        print(f"wrote {args.svg}")


if __name__ == "__main__":
    main()
