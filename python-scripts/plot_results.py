import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

def load_opt_data():
    try:
        df = pd.read_csv('opt_results.csv')
        return df
    except FileNotFoundError:
        print("Error: opt_results.csv not found")
        return None

def load_scaling_data():
    try:
        df = pd.read_csv('scaling_results.csv')
        return df
    except FileNotFoundError:
        print("Error: scaling_results.csv not found")
        return None
    
def plot_speedup(df_scaling):
    if df_scaling is None:
        return
    
    for prog in ['omp-for', 'omp-task', 'mpi']:
        plt.figure(figsize=(12, 8))
        data_prog = df_scaling[df_scaling['type'] == prog]
        
        if data_prog.empty:
            plt.close()
            continue
        
        sizes = sorted(data_prog['N'].unique())
        has_data = False
        
        for n in sizes:
            data_n = data_prog[data_prog['N'] == n].sort_values('p')
            if not data_n.empty:
                time_1 = data_n[data_n['p'] == 1]['time'].values
                if len(time_1) > 0:
                    speedup = time_1[0] / data_n['time'].values
                    plt.plot(data_n['p'], speedup, marker='o', linewidth=2, label=f'N={n}')
                    has_data = True
        
        if has_data:
            plt.title(f'{prog} - Speedup')
            plt.xlabel('Threads/Processes')
            plt.ylabel('Speedup')
            plt.grid(True, alpha=0.3)
            plt.legend()
            plt.savefig(f'{prog}_speedup.png', dpi=150, bbox_inches='tight')
        plt.close()

def plot_optimizations(df_opt):
    if df_opt is None:
        return
    
    types = df_opt['type'].unique()
    
    for prog in types:
        plt.figure(figsize=(10, 6))
        data_prog = df_opt[df_opt['type'] == prog]
        opts = data_prog['opt'].unique()
        
        has_data = False
        for opt in opts:
            data = data_prog[data_prog['opt'] == opt].sort_values('N')
            if not data.empty:
                plt.plot(data['N'], data['time'], marker='o', label=f'{opt}')
                has_data = True
        
        if has_data:
            plt.title(f'{prog} - Optimization Levels')
            plt.xlabel('Matrix Size (N)')
            plt.ylabel('Time (s)')
            plt.grid(True, alpha=0.3)
            plt.legend()
            plt.savefig(f'{prog}_optimization.png', dpi=150, bbox_inches='tight')
        plt.close()

def plot_scaling_2d(df_scaling):
    if df_scaling is None:
        return
    
    for prog in ['omp-for', 'omp-task', 'mpi']:
        plt.figure(figsize=(12, 8))
        data_prog = df_scaling[df_scaling['type'] == prog]
        
        if data_prog.empty:
            plt.close()
            continue
        
        sizes = sorted(data_prog['N'].unique())
        has_data = False
        
        for n in sizes:
            data_n = data_prog[data_prog['N'] == n].sort_values('p')
            if not data_n.empty:
                plt.plot(data_n['p'], data_n['time'], marker='o', linewidth=2, label=f'N={n}')
                has_data = True
        
        if has_data:
            plt.title(f'{prog} - Scaling (2D)')
            plt.xlabel('Threads/Processes')
            plt.ylabel('Time (s)')
            plt.grid(True, alpha=0.3)
            plt.legend()
            plt.savefig(f'{prog}_scaling_2d.png', dpi=150, bbox_inches='tight')
        plt.close()

def plot_scaling_3d(df_scaling):
    if df_scaling is None:
        return
    
    for prog in ['omp-for', 'omp-task', 'mpi']:
        data_prog = df_scaling[df_scaling['type'] == prog]
        
        if data_prog.empty:
            continue
        
        N_values = sorted(data_prog['N'].unique())
        p_values = sorted(data_prog['p'].unique())
        
        X, Y = np.meshgrid(p_values, N_values)
        Z = np.zeros_like(X, dtype=float)
        
        for i, N in enumerate(N_values):
            for j, p in enumerate(p_values):
                cell = data_prog[(data_prog['N'] == N) & (data_prog['p'] == p)]
                if not cell.empty:
                    Z[i, j] = cell['time'].mean()
                else:
                    Z[i, j] = np.nan
        
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        surf = ax.plot_surface(X, Y, Z, cmap='plasma', 
                              alpha=0.9, 
                              edgecolor='k', 
                              linewidth=0.5,
                              antialiased=True)
        
        ax.set_xlabel('Threads/Processes')
        ax.set_ylabel('Matrix Size (N)')
        ax.set_zlabel('Time (s)')
        ax.set_title(f'{prog} - Execution Time')
        
        fig.colorbar(surf, ax=ax, shrink=0.6, aspect=20, pad=0.1, label='Time (s)')
        
        ax.view_init(elev=25, azim=45)
        
        plt.tight_layout()
        plt.savefig(f'{prog}_scaling_3d.png', dpi=150, bbox_inches='tight')
        plt.close()

        
def main():
    df_opt = load_opt_data()
    df_scaling = load_scaling_data()
    
    if df_opt is not None:
        plot_optimizations(df_opt)
    
    if df_scaling is not None:
        plot_scaling_2d(df_scaling)
        plot_scaling_3d(df_scaling)
        plot_speedup(df_scaling)
    
    print("All plots saved")

if __name__ == "__main__":
    main()