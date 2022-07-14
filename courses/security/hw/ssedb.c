#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/reg.h>
#include <sys/ptrace.h>
#include <sys/user.h>
#include <sys/wait.h>

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
    int addr;           // for "b"
    char *filename;     // for "file"
  }u;
};
typedef struct Cmd_t *Cmd_t;

// Various constructor functions.
Cmd_t
Cmd_new_break (int addr)
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
    int addr;
    if (!*(s)){
      printf ("break requires an address\n");
      return 0;
    }
    addr = strtol (s, 0, 0);
    if (DEBUG)
      printf ("addr = %x\n", addr);
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
    int brk = 0x000000cc;
    int data;

    data = ptrace(PTRACE_PEEKDATA, pid, c->u.addr, 0);
    printf ("init data = %x\n", data);
    data = (data &0xffffff00) | brk;    
    printf ("revised data = %x\n", data);
    ptrace(PTRACE_POKEDATA, pid, c->u.addr, data);
    ptrace(PTRACE_CONT, pid, 0, 0);
    waitChild ();
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
    printf ("eax = %ld\n"
	    "ebx = %ld\n"
	    "ecx = %ld\n"
	    "edx = %ld\n"
	    "esi = %ld\n"
	    "edi = %ld\n"
	    "esp = 0x%p\n"
	    "ebp = 0x%p\n"
	    "eip = 0x%p\n", 
	    regs.eax, 
	    regs.ebx, 
	    regs.ecx, 
	    regs.edx,
	    regs.esi, 
	    regs.edi, 
	    (char *)regs.esp, 
	    (char *)regs.ebp,
	    (char *)regs.eip);
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
    TODO;
    return;
  }
  case CMD_KIND_XX:{
    // By default, we disassemble 40 bytes
    int i;
    int addr = c->u.addr;
    
    for (i=0; i<10; i++){
      int data = ptrace(PTRACE_PEEKDATA, pid, addr, 0);
      printf ("%x: %x\n", addr, data);
      addr += 4;
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
