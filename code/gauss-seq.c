#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include <sys/time.h>

void prt1a(char *t1, double *v, int n,char *t2);
void wtime(double *t) {
    static int sec = -1;
    struct timeval tv;
    gettimeofday(&tv, (void *)0);
    if (sec < 0) sec = tv.tv_sec;
    *t = (tv.tv_sec - sec) + 1.0e-6*tv.tv_usec;
}

int N;
double *A;
#define A(i,j) A[(i)*(N+1)+(j)]
double *X;

int main(int argc,char **argv) {
    double time0, time1;
    int i, j, k;
    int max_iter = 0;

    if (argc > 1) N = atoi(argv[1]);
    if (argc > 2) max_iter = atoi(argv[2]);

    A = (double *)malloc(N*(N+1)*sizeof(double));
    X = (double *)malloc(N*sizeof(double));

    for(i=0;i<N;i++)
        for(j=0;j<=N;j++)
            A(i,j) = (i==j || j==N)?1.0:0.0;

    wtime(&time0);

    int it = (max_iter>0 && max_iter<N)?max_iter:N-1;
    for (i=0;i<it;i++)
        for (k=i+1;k<N;k++)
            for (j=i+1;j<=N;j++)
                A(k,j) -= A(k,i)*A(i,j)/A(i,i);

    X[N-1] = A(N-1,N)/A(N-1,N-1);
    for (j=N-2;j>=0;j--) {
        for (k=0;k<=j;k++)
            A(k,N) -= A(k,j+1)*X[j+1];
        X[j] = A(j,N)/A(j,j);
    }

    wtime(&time1);
    printf("Time=%g\n",time1-time0);
    prt1a("X=(",X,N>9?9:N,"...)\n");

    free(A); free(X);
    return 0;
}

void prt1a(char *t1,double *v,int n,char *t2){
    int j;
    printf("%s",t1);
    for(j=0;j<n;j++)
        printf("%.4g%s",v[j],j%10==9?"\n":", ");
    printf("%s",t2);
}
