#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include <mpi.h>

int main(int argc,char **argv){
    MPI_Init(&argc,&argv);
    int rank,size;
    MPI_Comm_rank(MPI_COMM_WORLD,&rank);
    MPI_Comm_size(MPI_COMM_WORLD,&size);

    int N=atoi(argv[1]);
    int max_iter=(argc>2)?atoi(argv[2]):0;

    int rows=N/size;
    int start=rank*rows;
    int end=(rank==size-1)?N:start+rows;

    double *A=(double*)malloc((end-start)*(N+1)*sizeof(double));
    double *X=(double*)malloc(N*sizeof(double));
    double *row=(double*)malloc((N+1)*sizeof(double));

    for(int i=start;i<end;i++)
        for(int j=0;j<=N;j++)
            A[(i-start)*(N+1)+j]=(i==j||j==N)?1.0:0.0;

    MPI_Barrier(MPI_COMM_WORLD);
    double t0=MPI_Wtime();

    int it=(max_iter>0&&max_iter<N)?max_iter:N-1;
    for(int i=0;i<it;i++){
        int owner=i/rows;
        if(rank==owner)
            for(int j=i;j<=N;j++)
                row[j]=A[(i-start)*(N+1)+j];
        MPI_Bcast(row+i,N-i+1,MPI_DOUBLE,owner,MPI_COMM_WORLD);

        for(int k=start;k<end;k++)
            if(k>i)
                for(int j=i+1;j<=N;j++)
                    A[(k-start)*(N+1)+j]-=A[(k-start)*(N+1)+i]*row[j]/row[i];
    }

    if(rank==size-1)
        X[N-1]=A[(N-1-start)*(N+1)+N]/A[(N-1-start)*(N+1)+(N-1)];
    MPI_Bcast(&X[N-1],1,MPI_DOUBLE,size-1,MPI_COMM_WORLD);

    for(int j=N-2;j>=0;j--){
        double local=0;
        if(j>=start&&j<end)
            for(int k=0;k<=j;k++)
                local=A[(k-start)*(N+1)+(j+1)]*X[j+1];
        double sum;
        MPI_Allreduce(&local,&sum,1,MPI_DOUBLE,MPI_SUM,MPI_COMM_WORLD);
        if(rank==0) X[j]=(1.0-sum);
        MPI_Bcast(&X[j],1,MPI_DOUBLE,0,MPI_COMM_WORLD);
    }

    double t1=MPI_Wtime();
    if(rank==0) printf("Time=%g\n",t1-t0);

    free(A); free(X); free(row);
    MPI_Finalize();
    return 0;
}