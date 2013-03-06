#include <stdio.h>
int N;
long long int a[1000];
int diff;

int main()
{
    scanf("%d %d", &N, &diff);
		for (int i=0; i<N; i++) scanf("%lld ", &a[i]);
		for (int i=0; i<(N-1); i++) for (int j=i; j<N; j++) if (a[i]-a[j] == diff)
		{
				printf("\\n\n");
				return 0;
		}
		printf("%clld\n", '%');
		return 0;
}
