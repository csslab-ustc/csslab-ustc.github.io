#include "spinlock.h"
//#include "cas.h"
int onlock(struct lock i){
    while(1){
        i.d = atomic_cmp_set(&lock.d, 0,  1);
        if(i.d == 0)
            return 1;
    }
}
int unlock(struct lock i){
    while(1){
        i.d = atomic_cmp_set(&lock.d, 1,  0);
        if(i.d == 1)
            return 1;
    }
}