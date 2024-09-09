#include"stack.h"
#include<stdlib.h>

Stack *Stack_new() {
    Stack *st = (struct Stack *)malloc(sizeof(*st));

    int n = 10000;
    st->array = (DataType *) malloc(sizeof(DataType) * n);
    st->count = n;
    st->top = 0;
    st->lock.d = 0;
    return st;
}

int Stack_size(Stack *st) {
    return st->top;
}
void *Stack_push2(struct Args *args){
    //struct Stack* st = (struct Stack*)args;
    Stack_push(args->st, args->data);
    return 0;
}

void Stack_push(Stack *st, int data) {
    //struct Stack* st = (struct Stack*)args;
    //int data = 1;
    lock(&(st->lock));

    if (st->top == st->count) {
        st->array = (DataType *) realloc(st->array, sizeof(DataType) * 2 * st->count);
        st->count = 2 * st->count;
    }
    st->array[st->top] = data;
    st->top++;

    unlock(&(st->lock));

}

void Stack_destroy(Stack *st) {
    if (st->array) {
        free(st->array);
        st->top = st->count = 0;
    }
}
