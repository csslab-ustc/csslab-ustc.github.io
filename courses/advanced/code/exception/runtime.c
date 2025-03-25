#include <stdio.h>
#include <stdlib.h>

struct ExnFrame_t{
    struct ExnFrame_t *link;
    void *handler;
};

struct ExnFrame_t exn_frames[1024];
static int top = -1;

void exn_frame_push(void *handler){
    top++;
    exn_frames[top].handler = handler;
}

void *exn_frame_pop(){
    void *handler = exn_frames[top].handler;
    top--;
    return handler;
}

void print(long n){
    printf("%ld\n", n);
}

void cleanup(char *s){
    printf("stack cleanup for %s\n", s);
}

// throw a key word in C++...
void *throw0(){
    return exn_frames[top].handler;
}

void topHandler(){
    printf("unhandled exception, exiting...\n");
    exit(1);
}

