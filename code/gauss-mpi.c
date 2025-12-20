#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include <mpi.h>

int main(int argc, char **argv) {
    MPI_Init(&argc, &argv);
    
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    
    if (argc < 2) {
        if (rank == 0) printf("Usage: mpirun -np NPROC %s N [max_iter]\n", argv[0]);
        MPI_Finalize();
        return 1;
    }
    
    int N = atoi(argv[1]);
    int max_iter = (argc > 2) ? atoi(argv[2]) : N;
    if (max_iter > N) max_iter = N;
    
    int rows_per_proc = N / size;
    int extra_rows = N % size;
    int start_row, local_rows;
    
    if (rank < extra_rows) {
        start_row = rank * (rows_per_proc + 1);
        local_rows = rows_per_proc + 1;
    } else {
        start_row = rank * rows_per_proc + extra_rows;
        local_rows = rows_per_proc;
    }
    
    double *A_local = NULL;
    double *X = NULL;
    double *row_i = NULL;
    
    if (local_rows > 0) {
        A_local = (double *)malloc(local_rows * (N+1) * sizeof(double));
    }
    X = (double *)malloc(N * sizeof(double));
    row_i = (double *)malloc((N+1) * sizeof(double));
    
    if ((local_rows > 0 && !A_local) || !X || !row_i) {
        fprintf(stderr, "Rank %d: Memory allocation failed\n", rank);
        MPI_Abort(MPI_COMM_WORLD, 1);
    }

    for (int i = 0; i < local_rows; i++) {
        int global_i = start_row + i;
        for (int j = 0; j < N; j++) {
            A_local[i*(N+1)+j] = (double)(rand() % 100) / 100.0;
        }
        A_local[i*(N+1)+global_i] = 1.0 + N * 2.0;
        A_local[i*(N+1)+N] = (double)(rand() % 100) / 10.0;
    }
    
    MPI_Barrier(MPI_COMM_WORLD);
    double t0 = MPI_Wtime();
    
    for (int i = 0; i < max_iter; i++) {
        int owner;
        if (i < extra_rows * (rows_per_proc + 1)) {
            owner = i / (rows_per_proc + 1);
        } else {
            owner = extra_rows + (i - extra_rows * (rows_per_proc + 1)) / rows_per_proc;
        }

        if (rank == owner) {
            int local_i = i - start_row;
            for (int j = 0; j <= N; j++) {
                row_i[j] = A_local[local_i*(N+1)+j];
            }
        }
        
        MPI_Bcast(row_i, N+1, MPI_DOUBLE, owner, MPI_COMM_WORLD);
        
        for (int k = 0; k < local_rows; k++) {
            int global_k = start_row + k;
            if (global_k > i) {
                double factor = A_local[k*(N+1)+i] / row_i[i];
                for (int j = i+1; j <= N; j++) {
                    A_local[k*(N+1)+j] -= factor * row_i[j];
                }
                A_local[k*(N+1)+i] = 0.0;
            }
        }
    }
    
    for (int j = N-1; j >= 0; j--) {
        int owner;
        if (j < extra_rows * (rows_per_proc + 1)) {
            owner = j / (rows_per_proc + 1);
        } else {
            owner = extra_rows + (j - extra_rows * (rows_per_proc + 1)) / rows_per_proc;
        }
        
        if (rank == owner) {
            int local_j = j - start_row;
            double sum = 0.0;
            for (int k = j+1; k < N; k++) {
                sum += A_local[local_j*(N+1)+k] * X[k];
            }
            X[j] = (A_local[local_j*(N+1)+N] - sum) / A_local[local_j*(N+1)+j];
        }
        
        MPI_Bcast(&X[j], 1, MPI_DOUBLE, owner, MPI_COMM_WORLD);
    }
    
    double t1 = MPI_Wtime();
    
    if (rank == 0) {
        printf("Time=%g\n", t1-t0);
        
        printf("X[0..4]=");
        for (int i = 0; i < (N>5?5:N); i++) {
            printf(" %.4g", X[i]);
        }
        printf("\n");
    }
    
    if (A_local) free(A_local);
    free(X);
    free(row_i);
    
    MPI_Finalize();
    return 0;
}