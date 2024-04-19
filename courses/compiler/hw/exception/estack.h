#ifndef ESTACK_H
#define ESTACK_H

#include <setjmp.h>
#include <stdlib.h>

typedef struct estack *estack;
struct estack {
    estack next;
    int value;
    char *file;
    int line;
    jmp_buf buf;
};

extern estack global_stack;

#define estack_INIT() do{\
  estack_init();         \
  if (0==setjmp(global_stack->buf))             \
    ;                                           \
  else{                                                                 \
    printf ("Uncaught exception: in file: \"%s\", at line: %d with value %d. Exiting...\n"\
            , global_stack->file, global_stack->line, global_stack->value); \
    exit(1);                                           \
  }                                                    \
  }while(0)

void estack_init();

void estack_push();

void estack_pop();

#endif

