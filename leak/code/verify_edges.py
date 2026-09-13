"""Check every edge in a swarm hits.json against what the target agent actually read.

For each (source -> target) edge, collect the target commands that produced hits and
classify: direct   = the target read a file named after the source agent
          wildcard = the target ran cat /shared/* (reads everything present)
          two-hop  = the target read only other agents' files (text travelled through them)
          unknown  = none of the above (inspect by hand)

    python verify_edges.py runs/swarm_directed_explicit/hits.json
"""
import json, re, sys, collections

path = sys.argv[1]
d = json.load(open(path))
edges = collections.defaultdict(list)
for h in d["hits"]:
    edges[(h["source_run"], h["target_run"])].append(h)

def idx(run): return int(run.rsplit("-", 1)[1])

rows, counts = [], collections.Counter()
for (s, t), hs in sorted(edges.items()):
    cmds = sorted({(h["target_meta"] or {}).get("command") or "" for h in hs})
    si = idx(s)
    kinds = set()
    via = set()
    for c in cmds:
        if re.search(rf"agent-?{si}[-_]", c): kinds.add("direct")
        elif "/shared/*" in c: kinds.add("wildcard")
        else:
            others = set(re.findall(r"agent-?(\d+)[-_]", c))
            if others: kinds.add("two-hop"); via |= others
            else: kinds.add("unknown")
    if "direct" in kinds: label = "direct"
    elif "wildcard" in kinds: label = "wildcard"
    elif "two-hop" in kinds: label = "two-hop via " + ",".join(sorted(via))
    else: label = "unknown"
    counts[label.split(" ")[0]] += 1
    backward = idx(s) > idx(t)
    rows.append((s, t, len(hs), max(h["containment"] for h in hs), label, "BACKWARD" if backward else ""))
    print(f"{s} -> {t}: {len(hs):3d} hits, max {max(h['containment'] for h in hs):.2f}  {label} {'BACKWARD' if backward else ''}")
    if label == "unknown":
        for c in cmds: print("      cmd:", c[:100])
print(f"\n{len(rows)} edges: " + ", ".join(f"{k} {v}" for k, v in counts.items())
      + f"; backward edges: {sum(1 for r in rows if r[5])}")
