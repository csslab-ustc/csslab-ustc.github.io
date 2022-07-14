all:
	gcc -g -o touchstone server.c
	gcc -fno-stack-protector -z execstack -g -o filesv ./sql_lite3/sqlite3.o -l pthread -l dl ./sql_lite3/sqlhelper.c filesv.c token.c parse.c http-tree.c handle.c
	gcc -fno-stack-protector -z execstack -g -o banksv ./sql_lite3/sqlite3.o -l pthread -l dl ./sql_lite3/sqlhelper.c banksv.c  token.c parse.c http-tree.c handle.c
	gcc -fno-stack-protector -z execstack -g -o httpd  httpd.c token.c parse.c http-tree.c 


clean:
	rm -rf touchstone filesv banksv httpd 
