#include <stdlib.h>
#include "estack.h"

estack global_stack = 0;

static estack estack_alloc() {
    estack t = malloc(sizeof(*t));
    t->next = 0;
    t->value = -1;;
    t->line = -1;
    return t;
}

void estack_init() {
    estack t = estack_alloc();
    global_stack = t;
    return;
}

void estack_push() {
    estack t = estack_alloc();
    t->next = global_stack;
    global_stack = t;
    return;
}

void estack_pop() {
    global_stack = global_stack->next;
    return;
}
