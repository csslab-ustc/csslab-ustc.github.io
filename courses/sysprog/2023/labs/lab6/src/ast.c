#include "ast.h"

 void
usage (){
    printf ("A ptrace-based minimal debugger.\n"
            "\tUsage: ssedb <file>\n");
    exit (0);
}

 void
waitChild (){
    // wait the child to stop.
    wait (NULL);
    return;
}

// Various constructor functions.
Cmd_t
Cmd_new_break (long addr, int pid)
{
    Cmd_t c = malloc (sizeof (*c));
    c->kind = CMD_KIND_BREAK;
    c->u.addr = addr;
    c->pid = pid;
    return c;
}

Cmd_t
Cmd_new_cont (int pid)
{
    Cmd_t c = malloc (sizeof (*c));
    c->kind = CMD_KIND_CONT;
    c->pid = pid;
    return c;
}

Cmd_t
Cmd_new_file (char *filename, int pid)
{
    Cmd_t c = malloc (sizeof (*c));
    c->kind = CMD_KIND_FILE;
    c->u.filename = filename;
    c->pid = pid;
    return c;
}

Cmd_t
Cmd_new_quit (int pid)
{
    Cmd_t c = malloc (sizeof (*c));
    c->kind = CMD_KIND_QUIT;
    c->pid = pid;
    return c;
}

Cmd_t
Cmd_new_regs (int pid)
{
    Cmd_t c = malloc (sizeof (*c));
    c->kind = CMD_KIND_REGS;
    c->pid = pid;
    return c;
}

Cmd_t
Cmd_new_run (int pid)
{
    Cmd_t c = malloc (sizeof (*c));
    c->kind = CMD_KIND_RUN;
    c->pid = pid;
    return c;
}

Cmd_t
Cmd_new_si (int pid)
{
    Cmd_t c = malloc (sizeof (*c));
    c->kind = CMD_KIND_SI;
    c->pid = pid;
    return c;
}

Cmd_t
Cmd_new_xi (long addr, int pid)
{
    Cmd_t c = malloc (sizeof (*c));
    c->kind = CMD_KIND_XI;
    c->u.addr = addr;
    c->pid = pid;
    return c;
}

Cmd_t
Cmd_new_xx (long addr, int pid)
{
    Cmd_t c = malloc (sizeof (*c));
    c->kind = CMD_KIND_XX;
    c->u.addr = addr;
    c->pid = pid;
    return c;
}

