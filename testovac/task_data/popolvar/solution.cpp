#include <cstdio>

int main() {
  int m = 0, a = 0;
  while(scanf("%d", &a) == 1) if (a > m) m = a;
  printf("%d\n", m);
}
