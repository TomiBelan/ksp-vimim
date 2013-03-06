#include <stdio.h>

int main(){
	char s[500] ;
	fgets(s,400,stdin);
	int i=0;
	while (s[i]!='\n') i++;
	while (i>0)
	{
		i--;
		printf("%c", s[i]);
	}
	printf("\n");
}
