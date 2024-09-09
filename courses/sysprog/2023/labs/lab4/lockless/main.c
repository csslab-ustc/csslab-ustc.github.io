#include<stdio.h>
#include<pthread.h>
#include "stack.h"

int main()
{
    struct Args args;
    int correct = 0;
    int false = 0;

    for(int i = 0; i < 100; i++){
        Stack *st = Stack_new();
        args.st = st;
        args.data = 1;
        pthread_t tid[10000];
        for(int count = 0; count <10000; count++){
            pthread_create (&tid[count], NULL, (void *(*)(void *))Stack_push2, &args);

        }
        for(int count = 0; count <10000; count++){
            pthread_join(tid[count], NULL);
        }

        if(Stack_size(st) == 10000){
            correct++;
        }else{
            false++;
        }
        Stack_destroy(st);
    }
    printf("correct:%d\n false:%d\n",correct,false);
    return 0;
}