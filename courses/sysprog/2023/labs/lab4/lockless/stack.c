#include"stack.h"
#include"cas.h"
#include<stdlib.h>

Stack *Stack_new() {
    Stack *st = (struct Stack *)malloc(sizeof(*st));
    int n = 10000;
    st->array = (DataType *) malloc(sizeof(DataType) * n);
    st->count = n;
    st->top = 0;
    return st;
}

unsigned long Stack_size(Stack *st) {
    return st->top;
}
void *Stack_push2(struct Args *args){
    Stack_push(args->st, args->data);
    return ((void *)0);
}

void Stack_push(Stack *st, int data) {

    while(1){
        unsigned long old_top = st->top;
        unsigned long new_top = old_top + 1;

        if(atomic_cmp_set(&(st->top), old_top,  new_top) == old_top){
            if (st->top == st->count) {
                st->array = (DataType *) realloc(st->array, sizeof(DataType) * 2 * st->count);
                st->count = 2 * st->count;
            }
            st->array[st->top] = data;
            return;
        }

    }

}

void Stack_destroy(Stack *st) {
    if (st->array) {
        free(st->array);
        st->top = st->count = 0;
    }
}
