#ifndef STACK_H
#define STACK_H

#include"spinlock.h"

typedef int DataType;
typedef struct Stack
{
    DataType *array;
    int count;
    int top;
    struct lock lock;
}Stack;
struct Args{
    Stack *st;
    int data;
};

Stack *Stack_new();
int Stack_size(Stack *st);
void *Stack_push2(struct Args *args);
void Stack_push(Stack *st, int data);
void Stack_destroy(Stack *st);

#endif