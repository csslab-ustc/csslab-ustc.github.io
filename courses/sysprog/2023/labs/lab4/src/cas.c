#include "cas.h"
//static __inline__
unsigned long
atomic_cmp_set(volatile long *ptr, unsigned long old,
               unsigned long set)
{
    unsigned long prev;

    __asm__ volatile(
    "LOCK\n"
    "cmpxchgq %2,%1"
    : "=a"(prev), "+m"(*(volatile long *)(ptr))
    : "r"(set), "0"(old)
    : "memory");
    //printf("prev=%ld\n", prev);
    return prev;
}