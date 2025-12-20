import os
import re
import csv
from glob import glob

def extract_time(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
        match = re.search(r'Time=([\d\.]+)', content)
        return float(match.group(1)) if match else None

def collect_opt_results():
    data = {}
    for f in glob('../opt_results/*.out'):
        basename = os.path.basename(f)
        parts = basename.split('_')
        opt = parts[1]
        n = parts[2][1:]
        prog_type = parts[0]
        run = parts[3].replace('run', '').replace('.out', '')
        
        key = (prog_type, opt, n)
        if key not in data:
            data[key] = []
        
        time = extract_time(f)
        if time:
            data[key].append(time)
    
    with open('opt_results.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['type', 'opt', 'N', 'time'])
        for (prog_type, opt, n), times in data.items():
            if times:
                avg_time = sum(times) / len(times)
                writer.writerow([prog_type, opt, int(n), avg_time])

def collect_scaling_results():
    data = {}
    for f in glob('../scaling_results/*.out'):
        basename = os.path.basename(f)
        if 'mpi' in basename:
            parts = basename.split('_')
            prog_type = parts[0]
            n = parts[1][1:]
            p = parts[2][1:]
            run = parts[3].replace('run', '').replace('.out', '')
            key = (prog_type, n, p)
        else:
            parts = basename.split('_')
            prog_type = parts[0]
            n = parts[1][1:]
            t = parts[2][1:]
            run = parts[3].replace('run', '').replace('.out', '')
            key = (prog_type, n, t)
        
        if key not in data:
            data[key] = []
        
        time = extract_time(f)
        if time:
            data[key].append(time)
    
    with open('scaling_results.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['type', 'N', 'p', 'time'])
        for (prog_type, n, p), times in data.items():
            if times:
                avg_time = sum(times) / len(times)
                writer.writerow([prog_type, int(n), int(p), avg_time])

if __name__ == '__main__':
    collect_opt_results()
    collect_scaling_results()