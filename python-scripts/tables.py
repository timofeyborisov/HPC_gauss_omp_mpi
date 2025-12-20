import pandas as pd
import numpy as np

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

def print_optimization_tables(df_opt):
    if df_opt is None:
        return
    
    print("="*60)
    print("OPTIMIZATION RESULTS (O2 level, 8 threads/processes)")
    print("="*60)
    
    df_o2 = df_opt[df_opt['opt'] == 'O2']
    
    for prog in ['seq', 'omp-for', 'omp-task', 'mpi']:
        print(f"\n{prog.upper()}:")
        print("-"*40)
        print(f"{'N':<10} {'Time (s)':<15}")
        print("-"*40)
        
        data = df_o2[df_o2['type'] == prog].sort_values('N')
        for _, row in data.iterrows():
            print(f"{row['N']:<10} {row['time']:<15.4f}")

def print_scaling_tables(df_scaling):
    if df_scaling is None:
        return
    
    for prog in ['omp-for', 'omp-task', 'mpi']:
        print(f"\n{'='*60}")
        print(f"{prog.upper()} SCALING RESULTS")
        print("="*60)
        
        data_prog = df_scaling[df_scaling['type'] == prog]
        sizes = sorted(data_prog['N'].unique())
        procs = sorted(data_prog['p'].unique())
        
        # Header
        header = f"{'N\\p':<8}"
        for p in procs:
            header += f" {p:<12}"
        print(header)
        print("-"*(8 + 13*len(procs)))
        
        # Data rows
        for n in sizes:
            row = f"{n:<8}"
            for p in procs:
                value = data_prog[(data_prog['N'] == n) & (data_prog['p'] == p)]['time']
                if not value.empty:
                    row += f" {value.values[0]:<12.4f}"
                else:
                    row += f" {'-':<12}"
            print(row)

def main():
    df_opt = load_opt_data()
    df_scaling = load_scaling_data()
    
    print_optimization_tables(df_opt)
    print_scaling_tables(df_scaling)

if __name__ == "__main__":
    main()