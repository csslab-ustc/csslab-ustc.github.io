#include "spinlock.h"
#include "cas.h"

void lock(struct lock *i){
    while(atomic_cmp_set(&(i->d), 0,  1)){
        // spin;
    }
    //return;
}
void unlock(struct lock *i){
    i->d = 0;
}