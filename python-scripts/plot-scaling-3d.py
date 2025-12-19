#!/usr/bin/env python3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

df = pd.read_csv("results.csv")

for method in ["omp-for", "omp-task", "mpi"]:
    d = df[df["type"] == method]

    Ns = sorted(d["N"].unique())
    Ts = sorted(d["threads"].dropna().unique())

    X, Y = np.meshgrid(Ts, Ns)
    Z = np.zeros_like(X, dtype=float)

    for i, N in enumerate(Ns):
        for j, t in enumerate(Ts):
            cell = d[(d["N"] == N) & (d["threads"] == t)]
            Z[i,j] = cell["time"].mean() if not cell.empty else np.nan

    fig = plt.figure(figsize=(10,8))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(X, Y, Z, cmap="viridis")

    ax.set_xlabel("Threads")
    ax.set_ylabel("N")
    ax.set_zlabel("Time (s)")
    ax.set_title(f"3D scaling: {method}")

    plt.tight_layout()
    plt.savefig(f"scaling_3d_{method}.png", dpi=300)
