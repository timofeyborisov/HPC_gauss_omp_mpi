#!/bin/bash
module load SpectrumMPI

OPTS=("O1" "O2" "O3")
SIZES=("4000" "8000" "12000" "16000")
REPEATS=3
OUT="../opt_results"

mkdir -p $OUT

for opt in "${OPTS[@]}"; do
    for N in "${SIZES[@]}"; do
        # for ((r=1;r<=REPEATS;r++)); do
        #     echo "SEQ N=$N run=$r"
        #     ../builds/gauss-seq_${opt} $N 10 > $OUT/seq_${opt}_N${N}_run${r}.out 2>&1
        # done
        # sleep 2

        # for ((r=1;r<=REPEATS;r++)); do
        #     echo "OMP FOR N=$N run=$r"
        #     OMP_NUM_THREADS=8 ../builds/gauss-omp-for_${opt} $N 10 > $OUT/omp-for_${opt}_N${N}_run${r}.out 2>&1
        # done
        # sleep 2

        # for ((r=1;r<=REPEATS;r++)); do
        #     echo "OMP TASK N=$N run=$r"
        #     OMP_NUM_THREADS=8 ../builds/gauss-omp-task_${opt} $N 10 > $OUT/omp-task_${opt}_N${N}_run${r}.out 2>&1
        # done
        # sleep 2

        for ((r=1;r<=REPEATS;r++)); do
            echo "MPI N=$N run=$r"
            mpirun -np 8 ../builds/gauss-mpi_${opt} $N 10 > $OUT/mpi_${opt}_N${N}_run${r}.out 2>&1
        done
    done
done