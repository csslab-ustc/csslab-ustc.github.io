#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/reg.h>
#include <sys/ptrace.h>
#include <sys/user.h>
#include <sys/wait.h>
#include <libdis.h>
#include <string.h>
#include <inttypes.h>
#include <Zydis/Zydis.h>

#define DEBUG 0
#define TODO do{printf("Supply your code at: file: %s; \
line: %d\n", __FILE__, __LINE__);}while(0)


// pid of child
static int pid = 0;

static int status = 0;

static void
usage ()
{
  printf ("A ptrace-based minimal debugger.\n"
	  "\tUsage: ssedb <file>\n");
  exit (0);
}

static void 
die (const char *s)
{
  fprintf (stderr, "%s\n", s);
  exit (0);
}

static void
waitChild ()
{
  wait (&status);
  // Has the child being stopped?
  if (WIFEXITED (status))
    if (DEBUG)
      printf ("not being traced!\n");
  return;
}

//+++++++++++++++++++++++++++++++++++++++++++++++++++++++//
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
  union{
    long addr;           // for "b"
    char *filename;     // for "file"
  }u;
};
typedef struct Cmd_t *Cmd_t;

// Various constructor functions.
Cmd_t
Cmd_new_break (long addr)
{
  Cmd_t c = malloc (sizeof (*c));
  c->kind = CMD_KIND_BREAK;
  c->u.addr = addr;
  return c;
}

Cmd_t
Cmd_new_cont ()
{
  Cmd_t c = malloc (sizeof (*c));
  c->kind = CMD_KIND_CONT;
  return c;
}

Cmd_t
Cmd_new_file (char *filename)
{
  Cmd_t c = malloc (sizeof (*c));
  c->kind = CMD_KIND_FILE;
  c->u.filename = filename;
  return c;
}

Cmd_t
Cmd_new_quit ()
{
  Cmd_t c = malloc (sizeof (*c));
  c->kind = CMD_KIND_QUIT;
  return c;
}

Cmd_t
Cmd_new_regs ()
{
  Cmd_t c = malloc (sizeof (*c));
  c->kind = CMD_KIND_REGS;
  return c;
}

Cmd_t
Cmd_new_run ()
{
  Cmd_t c = malloc (sizeof (*c));
  c->kind = CMD_KIND_RUN;
  return c;
}

Cmd_t
Cmd_new_si ()
{
  Cmd_t c = malloc (sizeof (*c));
  c->kind = CMD_KIND_SI;
  return c;
}

Cmd_t
Cmd_new_xi (int addr)
{
  Cmd_t c = malloc (sizeof (*c));
  c->kind = CMD_KIND_XI;
  c->u.addr = addr;
  return c;
}

Cmd_t
Cmd_new_xx (int addr)
{
  Cmd_t c = malloc (sizeof (*c));
  c->kind = CMD_KIND_XX;
  c->u.addr = addr;
  return c;
}

// A tedious but simple parsing function, parsing
// user input string into a command data structure.
static Cmd_t 
parseCommand (char *s)
{
  char temp[1024];
  int i = 0;

  if (!s || !*s)
    return 0;

  // first get the command name, store it into "temp"
  while (temp[i++]=*s++)
    if (*s==' ' || *s=='\0')
      break;

  temp[i] = '\0';
  if (DEBUG)
    printf ("temp=[%s]\n", temp);
 
  if (0==strcmp (temp, "b")){
    long addr;
    if (!*(s)){
      printf ("break requires an address\n");
      return 0;
    }
    addr = strtol (s, 0, 0);
    if (DEBUG)
      printf ("addr = %lx\n", addr);
    return Cmd_new_break (addr);
  }
  else if (0==strcmp (temp, "c"))
    return Cmd_new_cont ();
  else if (0==strcmp (temp, "file")){
    if (!*s){
      printf ("file requires a file name\n");
      return 0;
    }
    return Cmd_new_file (s+1);
  }
  else if (0==strcmp (temp, "q"))
    return Cmd_new_quit ();
  else if (0==strcmp (temp, "r"))
    return Cmd_new_run ();
  else if (0==strcmp (temp, "regs"))
    return Cmd_new_regs ();
  else if (0==strcmp (temp, "si"))
    return Cmd_new_si ();
  else if (0==strcmp (temp, "x/i")){
    int addr;
    if (!*(s)){
      printf ("x/i requires an address\n");
      return 0;
    }
    addr = strtol (s, 0, 0);
    if (DEBUG)
      printf ("addr = %x\n", addr);
    return Cmd_new_xi (addr);
  }
    
  else if (0==strcmp (temp, "x/x")){
    int addr;
    if (!*(s)){
      printf ("x/x requires an address\n");
      return 0;
    }
    addr = strtol (s, 0, 0);
    if (DEBUG)
      printf ("addr = %x\n", addr);
    return Cmd_new_xx (addr);
  }
  else;

  printf ("Unknown command: %s\n", temp);
  return 0;
}

// Given a command and execute it.
static void
execCommand (Cmd_t c)
{
  switch (c->kind){
  case CMD_KIND_BREAK:{
    long brk = 0x00000000000000cc;
    long data, old_data;
    struct user_regs_struct uregs;

    data = ptrace(PTRACE_PEEKDATA, pid, c->u.addr, 0);
    old_data = data;
    printf ("init data = %lx\n", data);
    data = (data &0xffffffffffffff00) | brk;    
    printf ("revised data = %lx\n", data);
    ptrace(PTRACE_POKEDATA, pid, c->u.addr, data);
   
    ptrace(PTRACE_CONT, pid, 0, 0);

    waitChild ();
    ptrace(PTRACE_GETREGS, pid, 0, &uregs);
    ptrace(PTRACE_POKEDATA, pid, c->u.addr, old_data);
    uregs.rip = uregs.rip - 1;
    ptrace(PTRACE_SETREGS, pid, 0, &uregs);
    return;
  }
  case CMD_KIND_CONT:{
    ptrace(PTRACE_CONT, pid, 0, 0);
    waitChild ();
    return;
  }
  case CMD_KIND_FILE:{
    kill (pid, SIGKILL);
    pid = fork ();
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
    int c;
    L:
    printf ("ssedb is quiting. Are you sure? (y|n) ");
    c = getchar ();
    if ('y'==c || 'Y'==c){
      kill (pid, SIGKILL);
      exit (0);
    }
    else if ('n'==c || 'N'==c){
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

    ptrace (PTRACE_GETREGS, pid, 0, &regs);
    printf ("eax = %lld\n"
	    "ebx = %lld\n"
	    "ecx = %lld\n"
	    "edx = %lld\n"
	    "esi = %lld\n"
	    "edi = %lld\n"
	    "esp = 0x%p\n"
	    "ebp = 0x%p\n"
	    "eip = 0x%p\n", 
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
    ptrace(PTRACE_DETACH, pid, 0, 0);
    waitChild ();
    return;
  }
  case CMD_KIND_SI:{
    ptrace(PTRACE_SINGLESTEP, pid, 0, 0);
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
      buf.data[i] = ptrace(PTRACE_PEEKDATA, pid, addr, 0);
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
          // Print current instruction pointer.
          printf("%016" PRIX64 "  ", runtime_address);

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
      long data = ptrace(PTRACE_PEEKDATA, pid, addr, 0);
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

static void
loopCommand ()
{
  // buffer to hold user input, hopefully,
  // 1024 seems to be large enough.
  char buf[1024];
 
  while (1){
    printf ("(ssedb) ");
    gets(buf);
    
    if (DEBUG)
      printf ("user input: %s\n", buf);

    Cmd_t c = parseCommand (buf);
    // not a valid command, re-read
    if (!c)
      continue;
    
    // execute a valid command
    execCommand (c);
  }
}


int 
main (int argc, char **argv)
{
  // The debugger should be run as:
  //   $ ./ssedb <file>
  // and this "if" checks this.
  if (argc<2)
    usage ();

  pid = fork ();

  // In the child
  if (0 == pid){
    ptrace (PTRACE_TRACEME, 0, 0, 0);
    execve (argv[1], argv+1, 0);
    return;
  }
  // in the parent
  else{
    // wait the child to stop.
    waitChild ();
    printf ("A minimal ptrace-based dubugger, copyright (C) 2012, by SSE of USTC.\n"
	    "Now debugging: %s (pid: %d)\n", argv[1], pid);
    // now, the debugger is ready to read commands in
    // and handle them, repeatedly.
    loopCommand ();
  }
  return 0;
}
