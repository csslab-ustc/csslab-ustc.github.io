#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/ptrace.h>
#include <inttypes.h>
#include <Zydis/Zydis.h>
#include <unistd.h>
#include <sys/user.h>

#include "cmdFuncs.h"
#include "ast.h"

// A tedious but simple parsing function, parsing
// user input string into a command data structure.
 Cmd_t
parseCommand (char *s, int pid){
    char temp[1024];
    int i = 0;

    if (!s || !*s)
        return 0;

    // first get the command name, store it into "temp"
    while ((temp[i++]=*s++))
        if (*s==' ' || *s=='\0')
            break;

    temp[i] = '\0';

    if (0==strcmp (temp, "b")){
        long addr;
        if (!*(s)){
            printf ("break requires an address\n");
            return 0;
        }
        addr = strtol (s, 0, 0);
        return Cmd_new_break (addr, pid);
    }
    else if (0==strcmp (temp, "c"))
        return Cmd_new_cont (pid);
    else if (0==strcmp (temp, "file")){
        if (!*s){
            printf ("file requires a file name\n");
            return 0;
        }
        return Cmd_new_file (s+1, pid);
    }
    else if (0==strcmp (temp, "q"))
        return Cmd_new_quit (pid);
    else if (0==strcmp (temp, "r"))
        return Cmd_new_run (pid);
    else if (0==strcmp (temp, "regs"))
        return Cmd_new_regs (pid);
    else if (0==strcmp (temp, "si"))
        return Cmd_new_si (pid);
    else if (0==strcmp (temp, "x/i")){
        long addr;
        if (!*(s)){
            printf ("x/i requires an address\n");
            return 0;
        }
        addr = strtol (s, 0, 0);
        return Cmd_new_xi (addr, pid);
    }

    else if (0==strcmp (temp, "x/x")){
        long addr;
        if (!*(s)){
            printf ("x/x requires an address\n");
            return 0;
        }
        addr = strtol (s, 0, 0);
        return Cmd_new_xx (addr, pid);
    }
    else;

    printf ("Unknown command: %s\n", temp);
    return 0;
}

// Given a command and execute it.
 void
execCommand (Cmd_t c){
    switch (c->kind){
        case CMD_KIND_BREAK:{
            long brk = 0x00000000000000cc;
            long data, old_data;
            struct user_regs_struct uregs;

            data = ptrace(PTRACE_PEEKDATA, c->pid, c->u.addr, 0);
            old_data = data;
            printf ("init data = %lx\n", data);
            data = (data & 0xffffffffffffff00) | brk;
            printf ("revised data = %lx\n", data);
            ptrace(PTRACE_POKEDATA, c->pid, c->u.addr, data);

            ptrace(PTRACE_CONT, c->pid, 0, 0);

            waitChild ();
            ptrace(PTRACE_GETREGS, c->pid, 0, &uregs);
            ptrace(PTRACE_POKEDATA, c->pid, c->u.addr, old_data);
            uregs.rip = uregs.rip - 1;
            ptrace(PTRACE_SETREGS, c->pid, 0, &uregs);
            return;
        }
        case CMD_KIND_CONT:{
            ptrace(PTRACE_CONT, c->pid, 0, 0);
            waitChild ();
            return;
        }
        case CMD_KIND_FILE:{
            kill (c->pid, SIGKILL);
            int pid = fork ();
            if (0==pid){
                ptrace (PTRACE_TRACEME, 0, 0, 0);
                execve (c->u.filename, &c->u.filename, 0);
            }
            else{
                waitChild ();
                printf ("loading: %s (pid: %d)\n", c->u.filename, pid);
                return;
            }
            return;
        }
        case CMD_KIND_QUIT:{
            int ch;
            L:
            printf ("ssedb is quiting. Are you sure? (y|n) ");
            ch = getchar ();
            if ('y'==ch || 'Y'==ch){
                kill (c->pid, SIGKILL);
                exit (0);
            }
            else if ('n'==ch || 'N'==ch){
                getchar ();
                return;
            }
            else {
                printf("\n");
                goto L;
            }
            return;
        }
        case CMD_KIND_REGS:{
            struct user_regs_struct regs;

            ptrace (PTRACE_GETREGS, c->pid, 0, &regs);
            printf ("rax = %lld\n"
                    "rbx = %lld\n"
                    "rcx = %lld\n"
                    "rdx = %lld\n"
                    "rsi = %lld\n"
                    "rdi = %lld\n"
                    "rsp = 0x%p\n"
                    "rbp = 0x%p\n"
                    "rip = 0x%p\n",
                    regs.rax,
                    regs.rbx,
                    regs.rcx,
                    regs.rdx,
                    regs.rsi,
                    regs.rdi,
                    (char *)regs.rsp,
                    (char *)regs.rbp,
                    (char *)regs.rip);
            return;
        }
        case CMD_KIND_RUN:{
            ptrace(PTRACE_DETACH, c->pid, 0, 0);
            waitChild ();
            return;
        }
        case CMD_KIND_SI:{
            ptrace(PTRACE_SINGLESTEP, c->pid, 0, 0);
            return;
        }
        case CMD_KIND_XI:{

            int i;
            long addr = c->u.addr;


            union{
                long data[10];           // for "b"
                ZyanU8 data_char[80];     // for "file"
            }buf;


            for (i=0; i<10; i++){
                buf.data[i] = ptrace(PTRACE_PEEKDATA, c->pid, addr, 0);
                printf ("%lx: %lx\n", addr, buf.data[i]);
                for(int j = 0; j<8; j++){
                    printf ("char:%x\n", buf.data_char[i*8+j]);
                }
                addr += 8;
            }
            ZydisDecoder decoder;
            ZydisDecoderInit(&decoder, ZYDIS_MACHINE_MODE_LONG_64, ZYDIS_ADDRESS_WIDTH_64);

            // Initialize formatter. Only required when you actually plan to do instruction
            // formatting ("disassembling"), like we do here
            ZydisFormatter formatter;
            ZydisFormatterInit(&formatter, ZYDIS_FORMATTER_STYLE_INTEL);

            // Loop over the instructions in our buffer.
            // The runtime-address (instruction pointer) is chosen arbitrary here in order to better
            // visualize relative addressing
            ZyanU64 runtime_address = 0x007FFFFFFF400000;
            ZyanUSize offset = 0;
            const ZyanUSize length = sizeof(buf.data_char);
            ZydisDecodedInstruction instruction;
            while (ZYAN_SUCCESS(ZydisDecoderDecodeBuffer(&decoder, buf.data_char + offset, length - offset,
                                                         &instruction)))
            {
                // todo : Print current instruction pointer.
                printf(" %016 " PRIX64 "  ", runtime_address);

                // Format & print the binary instruction structure to human readable format
                char buffer[256];
                ZydisFormatterFormatInstruction(&formatter, &instruction, buffer, sizeof(buffer),
                                                runtime_address);
                puts(buffer);

                offset += instruction.length;
                runtime_address += instruction.length;
            }

            return;

        }
        case CMD_KIND_XX:{
            // By default, we disassemble 40 bytes
            int i;
            long addr = c->u.addr;

            for (i=0; i<10; i++){
                long data = ptrace(PTRACE_PEEKDATA, c->pid, addr, 0);
                printf ("%lx: %lx\n", addr, data);
                addr += 8;
            }
            return;
        }
        default:
            printf ("Unknown command: ssedb bug!\n");
            return;
    }
}

 void
loopCommand (int pid){
    // buffer to hold user input, hopefully,
    // 1024 seems to be large enough.
    char buf[1024];

    while (1){
        printf ("(ssedb) ");
        gets(buf);

        Cmd_t c = parseCommand (buf, pid);
        // not a valid command, re-read
        if (!c)
            continue;

        // execute a valid command
        execCommand (c);
    }
}