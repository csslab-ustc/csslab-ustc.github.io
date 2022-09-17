topic 1：连续控制流 continuation， CPS style

```c
// tradition_version
int main(){
    printf("%d.\n", add(3, 4));
}

add(int x, int y){
    return x + y;
}

// continuation_version
int main(){
    f(int x){
        printf("%d.\n", x);
    }
    add(3, 4, f);
}

add(int x, int y, cont){
    cont(x + y);
}
```

CPS sample code

```c
// ******************CPS_sample_one
double square(double r){
    return r * r;
}

double area(double r){
    return 3.14 * square(r);
}

int main(){
    printf("%lf.\n", area(1.0));
}

// CPS_version_one
double square(double r, void (*cont)(double)){
    cont(r*r);
}

double area(double r, void (*cont)(double)){
    void f(double l){
        cont(3.14 * l);
    }
    square(r, f);
}

int main(){
    void f(double x){
        printf("%lf.\n", x);
    }
    area(1.0, f);
    
    return 0;
}

// ******************CPS_sample_two
int add(int x, int y){
	printf("%d.\n", x+y);
}

int main(){
    int m = add(3, 4);
    int n = add(5, 6)；
    printf("%d.\n", m+n);
    
    return 0;
}

// CPS_version_two
int add(int x, int y, void (*cont)(int)){
	cont(x+y);
}

int main(){
    void f(int x){
        void g(int y){
            printf("%d.\n", x+y);
            exit(0);
        }
        add(5, 6, g);
    }
    
    add(3, 4, f);
}

// ******************CPS_sample_three
int fac(int n){
    if(n == 0){
        return 1;
    }else{
        return n*fac(n-1);
    }
}

int main(){
    printf("%d.\n", fac(5));
}

// CPS_version_three
int fac(int n, void (*cont)(int)){
    if(n == 0){
		cont(1);
    }else{
        void f(int x){
            cont(n*x);
        }
        fac(n-1, f);
    }
}

int main(){
    void f(int x){
        printf("%d.\n", x)
    }
    fac(5, f);
    
    return 0;
}
```

topic 2：信号处理 signal process

```c
// ********************
void f(){
    asm(".byte \xff");
}

int main(){
    int i = 0;
    f();
    
    return 0;
}

// ********************one-shoot:OS will flush the callback function after being called once.
#include <signal.h>
#include <stdio.h>
#include <unistd.h>

void callback(int sig){
    printf("caught a signal: %d.\n", sig);
    //signal(SIGINT, callback);
}

int main(){
    int i = 0;
    signal(SIGINT, callback);
    
    return 0;
}
```

