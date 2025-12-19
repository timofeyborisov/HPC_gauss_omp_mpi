#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("results.csv")

seq = df[df["type"] == "seq"]

plt.figure(figsize=(8,6))

for opt in ["O1", "O2", "O3"]:
    d = seq[seq["opt"] == opt].groupby("N")["time"].mean()
    plt.plot(d.index, d.values, marker="o", label=opt)

plt.xlabel("N")
plt.ylabel("Time (s)")
plt.title("Sequential optimizations")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("optimizations_seq.png", dpi=300)
