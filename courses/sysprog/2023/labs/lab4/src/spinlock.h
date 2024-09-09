#ifndef SPINLOCK
#define SPINLOCK
#include "cas.h"

int onlock(struct lock i);
int unlock(struct lock i);

#endif