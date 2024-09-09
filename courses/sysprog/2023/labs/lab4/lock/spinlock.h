#ifndef SPINLOCK_H
#define SPINLOCK_H

struct lock{
    volatile unsigned long d;
};

void lock(struct lock *i);
void unlock(struct lock *i);

#endif