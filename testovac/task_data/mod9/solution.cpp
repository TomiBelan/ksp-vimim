#include <stdio.h>

int main() {
  int s=0;
  while (!feof(stdin)) {
    int d=-1;
    scanf("%1d", &d);
    if (d==-1) break;
    s=(s+d)%9;
  }
  if (s) printf("False\n"); else printf("True\n");

}
