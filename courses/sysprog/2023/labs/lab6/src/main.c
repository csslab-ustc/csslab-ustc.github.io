#include <stdio.h>
#include <unistd.h>
#include <sys/ptrace.h>
#include "ast.h"
#include "cmdFuncs.h"

int
main (int argc, char **argv){
    // The debugger should be run as:
    //   $ ./ssedb <file>
    // and this "if" checks this.
    if (argc<2)
        usage ();

    int pid = fork ();

    // In the child
    if (0 == pid){
        ptrace (PTRACE_TRACEME, 0, 0, 0);
        execve (argv[1], argv+1, 0);
        return 0;
    }
    // In the parent
    else{
        // wait the child to stop.
        waitChild ();
        printf ("A minimal ptrace-based dubugger, copyright (C) 2012, by SSE of USTC.\n"
                "Now debugging: %s (pid: %d)\n", argv[1], pid);
        // now, the debugger is ready to read commands in
        // and handle them, repeatedly.
        loopCommand (pid);
    }
    return 0;
}