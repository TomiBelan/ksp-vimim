#include <stdio.h>
#include <string.h>

int main() {
 char buf[1000];
  gets(buf);
  if (!strcmp(buf, "emacs")) printf("ano\n"); else printf("nie\n");

}
