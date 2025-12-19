#!/usr/bin/env python3
import re
import glob
import pandas as pd
from pathlib import Path

TIME_RE = re.compile(r'([Tt]ime[^0-9]*)([0-9.]+)')

def extract_time(text):
    m = TIME_RE.search(text)
    return float(m.group(2)) if m else None

rows = []

for file in glob.glob("../*_results/*.out"):
    name = Path(file).name

    with open(file, errors="ignore") as f:
        t = extract_time(f.read())
    if t is None:
        continue

    parts = name.replace(".out", "").split("_")

    row = {
        "file": name,
        "time": t,
        "type": parts[0],
    }

    for p in parts:
        if p.startswith("N"):
            row["N"] = int(p[1:])
        if p.startswith("t"):
            row["threads"] = int(p[1:])
        if p.startswith("p"):
            row["procs"] = int(p[1:])
        if p in ["O1", "O2", "O3"]:
            row["opt"] = p

    rows.append(row)

df = pd.DataFrame(rows)
df.to_csv("results.csv", index=False)
print(f"Saved {len(df)} rows to results.csv")
