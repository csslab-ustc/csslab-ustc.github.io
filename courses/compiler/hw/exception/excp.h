#ifndef EXCP_H
#define EXCP_H

#define TRY estack_push ();                     \
  if(0==setjmp(global_stack->buf)){


#define CATCH(x) }else if(x==global_stack->value){      \
  estack_pop();

#define ENDTRY }else{                           \
  int value = global_stack->value;              \
  char *file = global_stack->file;              \
  int line = global_stack->line;                \
  estack_pop();                                 \
  global_stack->value = value;                  \
  global_stack->file = file;                    \
  global_stack->line = line;                    \
  longjmp(global_stack->buf, 1);                \
  }

#define THROW(x) do{                            \
    global_stack->value = x;                    \
    global_stack->file = __FILE__;              \
    global_stack->line = __LINE__;              \
    longjmp(global_stack->buf, 1);              \
  }while(0)

#endif

