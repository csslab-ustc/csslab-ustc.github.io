#ifndef CAS_H
#define CAS_H

unsigned long
atomic_cmp_set(volatile unsigned long *ptr, unsigned long old, unsigned long new);

#endif