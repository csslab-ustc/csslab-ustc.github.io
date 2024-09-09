//
// Created by hushuang on 10/26/21.
//
#include<stdio.h>
#include<pthread.h>
#include "stack.h"

int main()
{
    Stack st;

    int count;
    int correct;
    int false;

    for(int i = 0; i < 100; i++){
        stackInit(&st);
        pthread_t tid[10000];
        for(count = 0; count <10000; count++){
            pthread_create (&tid[count], NULL, stackInsert, &st);

        }
        for(count = 0; count <10000; count++){
            pthread_join(tid[count], NULL);
        }

        if(stackSize(&st) == 10000){
            correct++;
        }else{
            false++;
        }
        stackDestory(&st);
    }
    printf("correct:%d\n false:%d\n",correct,false);
    return 0;
}