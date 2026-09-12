"""List every bash command that touched /shared, per run dir.
    python shared_usage.py runs/swarm_directed
"""
import glob, json, sys
for root in sys.argv[1:]:
    n = 0
    for p in sorted(glob.glob(f"{root}/agent-*/transcript.jsonl")):
        for line in open(p):
            d = json.loads(line)
            if d["kind"] == "EGRESS" and d["meta"].get("channel") == "bash_command" and "/shared" in d["content"]:
                n += 1
                print(p.split("/")[-2], "turn", d["meta"].get("turn"), ":", d["content"][:110].replace("\n", " | "))
    print(f"== {root}: {n} commands touched /shared")
