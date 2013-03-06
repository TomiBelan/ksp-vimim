#include <stdio.h>

long long int fact(long long int N)
{
	if (N==0) return 1;
	else return N*fact(N-1);
}

int main(){
	long long int N;
	scanf("%lld", &N);
	printf("%lld\n", fact(N));
}
