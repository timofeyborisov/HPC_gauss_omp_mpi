#!/bin/bash

module load SpectrumMPI

OPTS=("O1" "O2" "O3")

mkdir -p ../builds

echo "Compiling sequential"
for opt in "${OPTS[@]}"; do
    xlc -$opt -qarch=pwr8 -o ../builds/gauss-seq_${opt} ../code/gauss-seq.c -lm
done

echo "Compiling OpenMP for"
for opt in "${OPTS[@]}"; do
    xlc_r -$opt -qarch=pwr8 -qsmp=omp -o ../builds/gauss-omp-for_${opt} ../code/gauss-omp-for.c -lm
done

echo "Compiling OpenMP task"
for opt in "${OPTS[@]}"; do
    xlc_r -$opt -qarch=pwr8 -qsmp=omp -o ../builds/gauss-omp-task_${opt} ../code/gauss-omp-task.c -lm
done

echo "Compiling MPI"
for opt in "${OPTS[@]}"; do
    mpicc -$opt -qarch=pwr8 -o ../builds/gauss-mpi_${opt} ../code/gauss-mpi.c -lm
done

echo "Done"
