### Sample Code

#### OOP : Object oriented programming

```c
// ---------------------complex.h---------------------
typedef struct complex_t *complex_t;

// complex class
struct complex_t {
    // data
    double real;
    double virt;
   
    // method
    complex_t (*add)(complex_t, complex_t);
    void (*print)(complex_t);
    double (*distance)(complex_t);
}

complex_t complex_new(double real, double virt);


// ---------------------complex.c---------------------
#include "complex.h"
#include <stdio.h>
#include <math.h>

complex_t add(complex_t c1, complex_t c2);
void print(complex_t c);
double distance(complex_t c);

// object construtor
complex_t complex_new(double real, double virt){
    complex_t temp = malloc(sizeof(*temp));
    
    // init data
    temp->real = real;
    temp->virt = virt;
    
    // init method
    temp->add = add;
    temp->print = print;
    temp->distance = distance;
}

complex_t add(complex_t c1, complex_t c2){
    complex_t temp = malloc(sizeof(*temp));
    temp->real = c1->real + c2->real;
    temp->virt = c1->virt + c2->virt;
    
    return temp;
}

void print(complex_t c){
    printf("%lf + %lf i", c->real, c->virt);
    
    return ;
}

double distance(complex_t c){
    double value = sqrt(c->real*c->real + c->virt*c->virt);
    
    return value;
}


// ---------------------main.c---------------------
#include <stdio.h>
#include "complex.h"

#define CALL(obj, f) obj->f(obj)

int main(){
    complex_t c = complex_new(3.0, 4.0);
    d = CALL(c, distance)
    printf("distance : %lf\n", d);
    
    return 0;
}
```

#### virtual table version

```c
// ---------------------complex.h---------------------
typedef struct complex_t *complex_t;

// create virtual table to save more memory space
typedef struct complex_vtable *complex_vtable;
struct complex_vtable{
    // method
    complex_t (*add)(complex_t, complex_t);
    void (*print)(complex_t);
    double (*distance)(complex_t);
}

// complex class
struct complex_t {
    // data
    double real;
    double virt;
   
    // vptr
    complex_vtable vptr;
}

complex_t complex_new(double real, double virt);


// ---------------------complex.c---------------------
#include "complex.h"
#include <stdio.h>
#include <math.h>

complex_t add(complex_t c1, complex_t c2);
void print(complex_t c);
double distance(complex_t c);

// object construtor
complex_t complex_new(double real, double virt){
    complex_t temp = malloc(sizeof(*temp));
    
    // init data
    temp->real = real;
    temp->virt = virt;
    
    temp->vptr = &vtable;
}

// init the vtable;
struct complex_vtable vtable = {
    .add = add,
    .print = print,
    .distance = distance
};

complex_t add(complex_t c1, complex_t c2){
    complex_t temp = malloc(sizeof(*temp));
    temp->real = c1->real + c2->real;
    temp->virt = c1->virt + c2->virt;
    
    return temp;
}

void print(complex_t c){
    printf("%lf + %lf i", c->real, c->virt);
    
    return ;
}

double distance(complex_t c){
    double value = sqrt(c->real*c->real + c->virt*c->virt);
    
    return value;
}


// ---------------------main.c---------------------
#include <stdio.h>
#include "complex.h"

#define CALL(obj, f) obj->vptr->f(obj)

int main(){
    complex_t c = complex_new(3.0, 4.0);
    d = CALL(c, distance)
    printf("distance : %lf\n", d);
    
    return 0;
}
```

#### Inheritance

```c
// ---------------------complex_color.h---------------------
typedef struct complex_color_vtable *complex_color_vtable;
struct complex_color_vtable{
    // method
    complex_color_t (*add)(complex_color_t, complex_color_t);
    void (*print)(complex_color_t);
    double (*distance)(complex_color_t);
}

// complex_color_t 继承自上述 complex_t类
typedef struct complex_color_t *comple_color_t;
struct complex_color_t {
    complex_color_vtable vptr;
    
    double real;
    double virt;
    char *color;
}

// ---------------------complex_color.c---------------------
#include "complex_color.h"
#include <stdio.h>

struct complex_color_vtable vtable = {
    .add = add,
    .print = print,
    .distance = distance
};

// object construtor
complex_color_t complex_color_new(double real, double virt, char *color){
    complex_color_t temp = malloc(sizeof(*temp));
    
    // init data
    temp->real = real;
    temp->virt = virt;
    temp->color = color;
    
    temp->vptr = &vtable;
}


complex_color_t add(complex_color_t c1, complex_color_t c2){
    complex_color_t temp = malloc(sizeof(*temp));
    temp->real = c1->real + c2->real;
    temp->virt = c1->virt + c2->virt;
    
    return temp;
}

void print(complex_color_t c){
    printf("%lf + %lf i, color: %s", c->real, c->virt, c->color);
    
    return ;
}

// ---------------------main.c---------------------
#include "complex_color.h"
#include <stdio.h>

#define CALL(obj, f) obj->vptr->f(obj)

int main(){
    complex_color_t c = complex_new(3.0, 4.0, "blue");
    d = CALL(c, distance)
    printf("distance : %lf\n", d);
    
    CALL(c, print);
    
    complex_t c2 = (complex_t)c;
    CALL(c2, pirnt);
    
    return 0;
}
```

#### Reflection & Interface

```c
// ---------------------complex.h---------------------
typedef struct complex_t *complex_t;

struct pair_t {
    char *name;
    void (*f)();
}

// create virtual table to save more memory space
typedef struct complex_vtable *complex_vtable;
struct complex_vtable{
    int num;
    // method
    struct pair_t add;
    struct pair_t print;
    struct pair_t distance;
}

// complex class
struct complex_t {
    // data
    double real;
    double virt;
   
    // vptr
    complex_vtable vptr;
}

complex_t complex_new(double real, double virt);


// ---------------------complex.c---------------------
#include "complex.h"
#include <stdio.h>
#include <math.h>

complex_t add(complex_t c1, complex_t c2);
void print(complex_t c);
double distance(complex_t c);

// object construtor
complex_t complex_new(double real, double virt){
    complex_t temp = malloc(sizeof(*temp));
    
    // init data
    temp->real = real;
    temp->virt = virt;
    
    temp->vptr = &vtable;
}

// init the vtable;
struct complex_vtable vtable = {
    .num = 3,
    .add = {
        .name = "add",
        .f = add
    },
    .print = {
        .name = "print", 
        .f = .print
    },
    .distance = {
        .name = "distance",
        .f = .distance
    }
};

complex_t add(complex_t c1, complex_t c2){
    complex_t temp = malloc(sizeof(*temp));
    temp->real = c1->real + c2->real;
    temp->virt = c1->virt + c2->virt;
    
    return temp;
}

void print(complex_t c){
    printf("%lf + %lf i", c->real, c->virt);
    
    return ;
}

double distance(complex_t c){
    double value = sqrt(c->real*c->real + c->virt*c->virt);
    
    return value;
}


// ---------------------main.c---------------------
#include <stdio.h>
#include "complex.h"

#define CALL(obj, f) obj->vptr->f(obj)

int main(){
    complex_t c = complex_new(3.0, 4.0);
	int func_num = c->vptr->num;
    
    // there is a bug.
    int *p = (int *)c->vptr;
    p++;
    struct pair_t *q = (struct pair_t *)p;
    
    for(int i=0; i<num; i++){
		printf("%s()\n", q->name);
        q++;
    }
    
    return 0;
}
```



