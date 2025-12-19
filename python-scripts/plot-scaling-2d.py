#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("results.csv")

for method in ["omp-for", "omp-task", "mpi"]:
    d = df[df["type"] == method]

    plt.figure(figsize=(8,6))

    for N in sorted(d["N"].unique()):
        sub = d[d["N"] == N]
        x = sub.get("threads", sub.get("procs"))
        base = sub[x == 1]["time"].mean()
        speedup = base / sub["time"]

        plt.plot(x, speedup, marker="o", label=f"N={N}")

    plt.plot([1,160],[1,160],"k--",alpha=0.4)
    plt.xlabel("Threads / Processes")
    plt.ylabel("Speedup")
    plt.title(f"Scaling: {method}")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"scaling_{method}.png", dpi=300)
