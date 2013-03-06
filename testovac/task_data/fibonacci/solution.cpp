#include <stdio.h>

int main(){
		int N;
    scanf("%d/n", &N);
		long long int a = 1;
		long long int b = 1;
		long long int c = 1;
		N--;
		while (N--)
		{
			c = a;
			a = a + b;
			b = c;
		}
		printf("%lld\n", b);
}
