#!/bin/bash
module load SpectrumMPI

cd "$(dirname "$0")"
SIZES=("4000" "8000" "12000" "16000")
THREADS=("1" "2" "4" "8")
PROCS=("1" "2" "4" "8" "20" "40" "80" "160")
REPEATS=3
mkdir -p ../results


EXE_OMP_FOR="../builds/gauss-omp-for_O2"
[[ -x $EXE_OMP_FOR ]] || { echo "ERROR: $EXE_OMP_FOR not executable"; exit 1; }

for N in ${SIZES[@]}; do
    for t in ${THREADS[@]}; do
        for r in $(seq 1 $REPEATS); do
            echo "OMP FOR N=$N t=$t run=$r"
            OMP_NUM_THREADS=$t $EXE_OMP_FOR $N 10 >../results/omp-for_N${N}_t${t}_run${r}.out 2>&1
        done
    done
done


EXE_OMP_TASK="../builds/gauss-omp-task_O2"
[[ -x $EXE_OMP_TASK ]] || { echo "ERROR: $EXE_OMP_TASK not executable"; exit 1; }

for N in ${SIZES[@]}; do
    for t in ${THREADS[@]}; do
        for r in $(seq 1 $REPEATS); do
            echo "OMP TASK N=$N t=$t run=$r"
            OMP_NUM_THREADS=$t $EXE_OMP_TASK $N 10 >../results/omp-task_N${N}_t${t}_run${r}.out 2>&1
        done
    done
done


EXE_MPI="../builds/gauss-mpi_O2"
[[ -x $EXE_MPI ]] || { echo "ERROR: $EXE_MPI not executable"; exit 1; }

for N in ${SIZES[@]}; do
    for p in ${PROCS[@]}; do
        for r in $(seq 1 $REPEATS); do
            echo "MPI N=$N p=$p run=$r"

            out="../results/mpi_N${N}_p${p}_run${r}.out"

            [[ $p -eq 1 ]] && $EXE_MPI $N 10 >$out 2>&1 || mpirun -np $p $EXE_MPI $N 10 >$out 2>&1
        done
    done
done