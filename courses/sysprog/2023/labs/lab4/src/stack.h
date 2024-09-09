#ifndef STACK
#define STACK

#include"spinlock.h"
typedef int DataType;
typedef struct Stack
{
    DataType *array;
    int count;
    int top;
    struct lock t;
}Stack;
void stackInit(Stack *st);
int stackSize(Stack *st);
//void print(Stack *st);
void* stackInsert(void* parameters);
void stackDestory(Stack *st);

#endif