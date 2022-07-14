#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <time.h>
#include "sql-lite3/dbutil.h"
#include "parse.h"
#include "handle.h"

#ifndef DEBUG
#define DEBUG 0
#endif

static char *fileOk = 
  "HTTP/1.1 200 OK\r\n\r\n";
static char *fileNotExist =
  "<html><b>404</b>: File does not exist!</html>";
static char *noPermission = 
  "<html><b>401</b>: Access denied: no permission!</html>";
// lookup the HTTP body to find key
static char *lookup (char *key);


void handleHead (char *uri, int fd)
{
  // to do 
  return;
}

static char *getTime()
{
  time_t now;
  char *t;
  
  time(&now);
  t = ctime(&now);
  return t;
}

void handleGet (char *uri, int fd)
{
  char *path;
  char *info;
  
  assert (uri);
  if (DEBUG)
    printf("uri=[%s]\n", uri);
  if (strcmp (uri, "/")==0)
    uri = "/index.html";
  path = malloc (strlen (uri)+3);
  strcpy (path, "./");
  strcpy (path+2, uri);
  if (DEBUG)
    printf ("path=[%s]\n", path);
  
  if (access(path, F_OK)!=0){
    fprintf (stderr, "file: %s not found\n"
	     , path);
    info = "HTTP/1.1 404 File Not Found\r\n\r\n";
    write (fd, info, strlen(info));
    write (fd, fileNotExist, strlen (fileNotExist));
    return;
  }
  if (access(path, R_OK)!=0){
    fprintf (stderr, "file: %s no perm\n"
	     , path);
    info = "HTTP/1.1 401 No Permission\r\n\r\n";
    write (fd, info, strlen(info));
    write (fd, noPermission, strlen (noPermission));
    return;
  }
  fprintf (stderr, "file: %s OK\n"
	   , path);
  info = "HTTP/1.1 200 OK\r\n\r\n";
  write (fd, info, strlen(info));
  
  char c;
  int file = open (path, O_RDONLY);
  while (read (file, &c, 1)){
    write (fd, &c, 1);
  }
  close (file);
  return;
}

////////////////////////////////////////////
// handle various POST-related requests.
// post login
void handlePostLogin (int fd
		      , char *name
		      , char *passwd
		      , int checkPasswd)
{
  int t = 0;
  if (checkPasswd)
    t = Db_checkUserPasswd(name, passwd);
  else t = 1;
  char c[1024];
  // not a valid user.
  if (!t){
    sprintf(c,
	    "<html>"
	    "<head>"
	    "<title>login failed</title>"
	    "</head>"
	    "<body>Sorry, %s. Login fail.."
	    "<p>Please login again."
	    "<p><form name='logoutform' method='POST' ><table><tr><td> <input type='submit' name='submit_exit' value='Exit'></td></tr></table></form>"
	    "</body></html>"
	    , name);
    char *info = fileOk;
    write(fd, info, strlen(info));
    write(fd, c, strlen(c));
    close(fd);
    return;
  }
  // login success!
  char *logintime = getTime ();
  int balance = Db_readBalance (name);
  sprintf(c,
	  "<html>"
	  "<head>"
	  "<title>Welcome</title>"
	  "</head>"
	  "<body>Welcome you: <b>%s</b> to the SSE bank."
	  "<p>"
	  "Current time is: %s."
	  "<p>"
	  "Your current balance is: <b>%d</b>."
	  "<p>"
	  "<form name='transferform' method='POST'>"
	  "<table>"
	  "<tr>"
	  "<td>&nbsp;</td>"
	  "<td> <input type='hidden' name='transfer_from' value='%s'>"
	  "</td>"
	  "</tr>"
	  "<tr>"
	  "<td>Transfer to:</td>"
	  "<td> <input type='text' name='transfer_to' size='20' autocomplete='no'>"
	  "</td>"
	  "</tr>"
	  "<tr>"
	  "<td>Money:</td>"
	  "<td> <input type='text' name='transfer_money' size='20' autocomplete='no'>"
	  "</td>"
	  "</tr>"
	  "<tr>"
	  "<td>&nbsp;</td>"
	  "<td> <input type='submit' name='submit_transfer' value='Transfer'>"
	  "</td>"
	  "</tr>"
	  "</table>"
	  "</form>"
	  "<p>"
	  "<form name='logoutform' method='POST'>"
	  "<table>"
	  "<tr>"
	  "<td> <input type='submit' name='submit_logout' value='Logout'>"
	  "</td>"
	  "</tr>"
	  "</table>"
	  "</form>"
	  "</body></html>"
	  , name
	  , logintime
	  , balance
	  , name);
  //printf("login = %s\n",c);
  char *info = fileOk;
  write(fd, info, strlen(info));
  write(fd, c, strlen(c));
  close (fd);
  return;  
}

// POST: register
void handlePostRegister (int fd
			 , char *name
			 , char *passwd)
{
  int t = Db_checkUser(name);
  char c[1024];

  // user exists
  if(t){
    sprintf(c,
	    "<html>"
	    "<head>"
	    "<title>register failed</title>"
	    "</head>"
	    "<body>Sorry, %s has registered!"
	    "<p>Please register again."
	    "<p><form name='exitform' method='POST'><table><tr><td> <input type='submit' name='submit_exit' value='Exit'>"
	    "</td>"
	    "</tr>"
	    "</table>"
	    "</form></body></html>"
	    , name);
    char *info = fileOk;
    write(fd, info, strlen(info));
    write(fd, c, strlen(c));
    close (fd);
    return;
  }
  //
  char *logintime = getTime();
  Db_registerUser(name, passwd);
  sprintf(c
	  , "<html>"
	  "<head>"
	  "<title>register succeed</title>"
	  "</head>"
	  "<body>Welcome, <b>%s</b>, you register succeed."
	  "<p>The current time is: %s."
	  "<p><form name='logoutform' method='POST'>"
	  "<table><tr><td> <input type='submit' name='submit_logout'"
	  "value='Logout'></td></tr></table></form></body></html>"
	  , name
	  , logintime);
  char *info = fileOk;
  write(fd, info, strlen(info));
  write(fd, c, strlen(c));
  close(fd);
  return;
}

void handlePostTransfer (int fd
			 , char *from
			 , char *to
			 , int money)
{
  int fromBalance = Db_readBalance (from);
  int newFromBalance = fromBalance - money;
  int toBalance = Db_readBalance (to);
  int newToBalance = toBalance + money;
  Db_writeBalance (from, newFromBalance);
  Db_writeBalance (to, newToBalance);
  handlePostLogin (fd, from, 0, 0);
  return;
}

void handlePostLogout (int fd)
{
  char *info = "HTTP/1.1 303 SeeOther\r\n"
    "Location: ./index.html\r\n\r\n";
  
  write (fd, info, strlen (info));
  close (fd);
  return;
}

// POST

//////////////////////////////////////////////
// data structure and values holding body info
struct kv{
  char *key;
  char *value;
};
static struct kv temp[16];
static char *kv_lookup(char *key)
{
  int i = 0;
  while (i<16 && temp[i].key){
    if (strcmp(temp[i].key, key)==0)
      return temp[i].value;
    // a dirty hack
    if (temp[i].key[0]=='s'
	&& key[0]=='s')
      return temp[i].value;
    i++;
  }
  return 0;
}

static void kv_print ()
{
  int i=0;
  while (i<16 && temp[i].key){
    fprintf (stderr, "kv[%d]=%s, %s\n"
	     , i
	     , temp[i].key
	     , temp[i].value);
    i++;
  }
  return;
}

// read values from the body.
static void getValues (Http_t tree)
{
  assert (tree);
  char *body = tree->body;
  assert (body);
  int len = strlen(body);

  char *start = body;
  int num = 0;
  while(start<body+len){
    char *end = strchr(start, '=');
    *end = '\0';
    temp[num].key = start;
    start = end+1;
    end = strchr(start, '&');
    if(end == 0){
      temp[num].value = start;
      break;
    }
    *end = '\0';
    temp[num].value = start;
    start = end+1;
    num++;
  }
  return;
}

void handlePost(Http_t tree, int fd)
{
  getValues (tree);
  kv_print();
  char *name = 0; 
  char *passwd = 0;
  char *type = kv_lookup ("submit");

  Db_init(0);
 
  if (strcmp (type, "Exit")==0
      || strcmp (type, "Logout")==0){
    handlePostLogout(fd);
  }
  else if (strcmp (type, "Login")==0){
    name = kv_lookup ("login_username");
    passwd = kv_lookup ("login_password");
    assert(name);
    assert(passwd);
    handlePostLogin (fd, name, passwd, 1);
  }
  else if (strcmp (type, "Register")==0){
    name = kv_lookup ("login_username");
    passwd = kv_lookup ("login_password");
    assert(name);
    assert(passwd);
    handlePostRegister (fd, name, passwd);
  }
  else if (strcmp (type, "Transfer")==0){
    char *from = kv_lookup ("transfer_from");
    char *to = kv_lookup ("transfer_to");
    char *money = kv_lookup ("transfer_money");
    assert (from);
    assert (to);
    assert(money);
    int m = atoi (money);
    handlePostTransfer (fd, from, to, m);
  }
  else {
    fprintf (stderr, "%s\n", "server bug");
    close(fd);
  }
  return;
}

void Handle_main (int fd, Http_t tree)
{
  assert (tree);
  if (tree->kind != HTTP_KIND_REQUEST){
    fprintf (stderr, "%s\n", "server bug");
    close (fd);
    exit (0);
  }
  
  ReqLine_t reqline = tree->reqLine;
  
  assert (reqline);
  switch (reqline->kind){
  case REQ_KIND_GET:
    handleGet(reqline->uri, fd);
    break;
  case REQ_KIND_HEAD:
    handleHead(reqline->uri, fd);
    break;
  case REQ_KIND_POST:
    handlePost(tree, fd);
    break;
  default:
    fprintf (stderr, "%s\n", "server bug");
    close (fd);
    exit (0);
    break;
  }  
  return;
}
