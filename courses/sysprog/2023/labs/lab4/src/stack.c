#include"stack.h"
#include<stdio.h>
#include<stdlib.h>
void stackInit(Stack *st)
{
    int n = 10000;
    st->array = (DataType *)malloc(sizeof(DataType)*n);
    st->count = n;
    st->top = 0;
    st->t.d = 0;
}
int stackSize(Stack *st)
{
    //printf("%d", st->top);
    //printf("\n");
    return st->top;
}
void print(Stack *st)
{
    int count = st->top;
    st->top = 0;
    for (st->top=0; st->top < count; st->top++)
    {
        printf("%d ", st->array[st->top]);
    }
    st->top = count;
    printf("\n");
}
void* stackInsert(void* parameters)
{
    struct Stack* st = (struct Stack*)parameters;

    if(onlock(st->t) == 1){
        int x = 1;
        if (st->top == st->count)
        {
            st->array = (DataType *)realloc(st->array, sizeof(DataType) * 2 * st->count);
            st->count = 2 * st->count;
        }
        st->array[st->top] = x;
        st->top++;

        }

    unlock(st->t);
    return 0;
}

void stackDestory(Stack *st)
{
    if (st->array)
    {
        free(st->array);
        st->top = st->count = 0;
    }
}
