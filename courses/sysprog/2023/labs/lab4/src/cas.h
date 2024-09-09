#ifndef CAS
#define CAS
static struct lock{
    volatile long d;
}lock;
//static __inline__
unsigned long
atomic_cmp_set(volatile long *ptr, unsigned long old, unsigned long set);

#endif