#include <stdio.h>
#define arch_has_hw_pte_young() false
#ifndef arch_has_hw_pte_young
#define DEFINED 0
#else
#define DEFINED 1
#endif
int main() { printf("%d\n", DEFINED); return 0; }
