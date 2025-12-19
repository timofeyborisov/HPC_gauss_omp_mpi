#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include <omp.h>

void prt1a(char *t1,double *v,int n,char *t2);

int N;
double *A;
#define A(i,j) A[(i)*(N+1)+(j)]
double *X;

int main(int argc,char **argv){
    int i,j,k;
    int max_iter=0;

    N=atoi(argv[1]);
    if(argc>2) max_iter=atoi(argv[2]);

    A=(double*)malloc(N*(N+1)*sizeof(double));
    X=(double*)malloc(N*sizeof(double));

    #pragma omp parallel for private(j)
    for(i=0;i<N;i++)
        for(j=0;j<=N;j++)
            A(i,j)=(i==j||j==N)?1.0:0.0;

    double t0=omp_get_wtime();

    int it=(max_iter>0&&max_iter<N)?max_iter:N-1;

    #pragma omp parallel
    #pragma omp single
    for(i=0;i<it;i++){
        for(k=i+1;k<N;k++)
            #pragma omp task firstprivate(i,k)
            for(j=i+1;j<=N;j++)
                A(k,j)-=A(k,i)*A(i,j)/A(i,i);
        #pragma omp taskwait
    }

    X[N-1]=A(N-1,N)/A(N-1,N-1);
    for(j=N-2;j>=0;j--){
        for(k=0;k<=j;k++)
            A(k,N)-=A(k,j+1)*X[j+1];
        X[j]=A(j,N)/A(j,j);
    }

    double t1=omp_get_wtime();
    printf("Time=%g\n",t1-t0);
    prt1a("X=(",X,N>9?9:N,"...)\n");

    free(A); free(X);
    return 0;
}

void prt1a(char *t1,double *v,int n,char *t2){
    int j;
    printf("%s",t1);
    for(j=0;j<n;j++)
        printf("%.4g%s",v[j],", ");
    printf("%s",t2);
}
