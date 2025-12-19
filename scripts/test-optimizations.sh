\#!/bin/bash

OPTS=("O1" "O2" "O3")
SIZES=("4000" "8000" "12000" "16000")
REPEATS=3
WALLTIME="00:20"
OUT="../opt_results"

mkdir -p $OUT

for opt in "${OPTS[@]}"; do
    for N in "${SIZES[@]}"; do

        for ((r=1;r<=REPEATS;r++)); do
            mpisubmit.pl -p 1 -t 1 -w $WALLTIME \
                ../builds/gauss-seq_${opt} \
                --stdout $OUT/seq_${opt}_N${N}_run${r}.out \
                -- $N 10
        done
        sleep 2

        for ((r=1;r<=REPEATS;r++)); do
            mpisubmit.pl -p 1 -t 8 -w $WALLTIME \
                env OMP_NUM_THREADS=8 ../builds/gauss-omp-for_${opt} \
                --stdout $OUT/omp-for_${opt}_N${N}_run${r}.out \
                -- $N 10
        done
        sleep 2

        for ((r=1;r<=REPEATS;r++)); do
            mpisubmit.pl -p 1 -t 8 -w $WALLTIME \
                env OMP_NUM_THREADS=8 ../builds/gauss-omp-task_${opt} \
                --stdout $OUT/omp-task_${opt}_N${N}_run${r}.out \
                -- $N 10
        done
        sleep 2

        for ((r=1;r<=REPEATS;r++)); do
            mpisubmit.pl -p 8 -t 1 -w $WALLTIME \
                ../builds/gauss-mpi_${opt} \
                --stdout $OUT/mpi_${opt}_N${N}_run${r}.out \
                -- $N 10
        done

    done
done
