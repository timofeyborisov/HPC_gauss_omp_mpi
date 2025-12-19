#!/bin/bash

OMP_THREADS=("1" "2" "4" "8")
MPI_PROCS=("1" "2" "4" "8" "20" "40" "80" "160")
SIZES=("4000" "8000" "12000" "16000")
REPEATS=3
WALLTIME="00:20"
OUT="../scaling_results"

mkdir -p $OUT

for N in "${SIZES[@]}"; do
    for t in "${OMP_THREADS[@]}"; do
        for ((r=1;r<=REPEATS;r++)); do
            mpisubmit.pl -p 1 -t $t -w $WALLTIME \
                env OMP_NUM_THREADS=$t ../builds/gauss-omp-for_O2 \
                --stdout $OUT/omp-for_N${N}_t${t}_run${r}.out \
                -- $N 10
        done
        sleep 2
    done
done

for N in "${SIZES[@]}"; do
    for t in "${OMP_THREADS[@]}"; do
        for ((r=1;r<=REPEATS;r++)); do
            mpisubmit.pl -p 1 -t $t -w $WALLTIME \
                env OMP_NUM_THREADS=$t ../builds/gauss-omp-task_O2 \
                --stdout $OUT/omp-task_N${N}_t${t}_run${r}.out \
                -- $N 10
        done
        sleep 2
    done
done

for N in "${SIZES[@]}"; do
    for p in "${MPI_PROCS[@]}"; do
        for ((r=1;r<=REPEATS;r++)); do
            mpisubmit.pl -p $p -t 1 -w $WALLTIME \
                ../builds/gauss-mpi_O2 \
                --stdout $OUT/mpi_N${N}_p${p}_run${r}.out \
                -- $N 10
        done
        sleep 2
    done
done
