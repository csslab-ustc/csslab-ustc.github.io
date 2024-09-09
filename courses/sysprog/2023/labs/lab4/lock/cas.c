#include "cas.h"
unsigned long
atomic_cmp_set(volatile unsigned long *ptr, unsigned long old,
               unsigned long new)
{
    unsigned long prev;
    __asm__ volatile(
    "LOCK cmpxchgq %2,%1"
    : "=a"(prev), "+m"(*(volatile long *)(ptr))
    : "r"(new), "0"(old)
    : "memory");
    return prev;
}