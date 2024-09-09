#ifndef SRC_AST_H
#define SRC_AST_H

#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>

 void
usage ();

 void
waitChild ();

// ssedb command-related data structures and operations
enum Cmd_Kind_t{
    CMD_KIND_BREAK,      // break points
    CMD_KIND_CONT,       // continue
    CMD_KIND_FILE,       // load an ELF file
    CMD_KIND_QUIT,       // quit the dubugger
    CMD_KIND_REGS,       // display registers
    CMD_KIND_RUN,        // run
    CMD_KIND_SI,         // assembly-level single stepping
    CMD_KIND_XI,         // disassemble instructions
    CMD_KIND_XX,         // disassemble data
    // of course, you may want to add more commands
    // by yourself
};

// data structure to represent a command
// feed to the "ssedb". For instance:
//   (ssedb) b 0x08040808
// or:
//   (ssedb) si
// or:
//   (ssedb) r
// and so on.
struct Cmd_t
{
    enum Cmd_Kind_t kind; // which kind the cmd is
    int pid;
    union{
        long addr;           // for "b"
        char *filename;     // for "file"
    }u;
};
typedef struct Cmd_t *Cmd_t;

// Various constructor functions.
Cmd_t
Cmd_new_break (long addr, int pid);

Cmd_t
Cmd_new_cont (int pid);

Cmd_t
Cmd_new_file (char *filename, int pid);

Cmd_t
Cmd_new_quit (int pid);

Cmd_t
Cmd_new_regs (int pid);

Cmd_t
Cmd_new_run (int pid);

Cmd_t
Cmd_new_si (int pid);

Cmd_t
Cmd_new_xi (long addr, int pid);

Cmd_t
Cmd_new_xx (long addr, int pid);

#endif //SRC_AST_H
