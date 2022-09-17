### Sample Code

```c
// ---------------------list.h---------------------
typedef struct list_t *list_t;
typedef void *poly_t;

list list_new();
list list_insert(list_t l, poly_t data);		// head-insert method

/*
int list_sum(list_t l);					
int list_mul(list_t l);	
*/

// abstract 
int list_fold(list_t l, poly_t acc, 
              poly_t (*f)(poly_t, poly_t));

list_t list_map(list_t l, 
              poly_t (*f)(poly_t));

void list_print(list_t l,
               void (*f)(poly_t));


// ---------------------list.c---------------------
#include <malloc.h>
#include "list.h"
#include <stdio.h>

/*
struct list_t{
    int data;
    struct list_t *next;
}
*/

struct list_t{
    void *data;
    struct list_t *next;
}

list_t list_new(){
    struct list_t *l = malloc(sizeof(*l));
    l->data = NULL;
    l->next = NULL;
    return l;
}

list_t list_insert(list_t l, poly_t data){		// head-insert method
	list_t tmp = malloc(sizeof(*tmp));
	tmp->data = data;
    tmp->next = l->next;
    l->next = tmp;
    return l;
}

/*
int list_sum(list_t l){
    int sum = 0;
    list_t tmp = l->next;
    while(tmp){
        sum += tmp->data;
        tmp = tmp->next;
    }
    
    return sum;
}

int list_mul(list_t l){
    int product = 1;
    list_t tmp = l->next;
    while(tmp){
        product *= tmp->data;
        tmp = tmp->next;
    }
    
    return product;
}
*/

int list_fold(list_t l, poly_t acc, 
              poly_t (*f)(poly_t, poly_t)){
    list_t tmp = l->next;
    while(tmp){
        acc = f(acc, tmp->data);
        tmp = tmp->next;
    }
    
    return acc;
}

list_t list_map(list_t l, poly_t (*f)(poly_t)){
    list_t new_list = list_new();
    list_t tail = new_list;
    list_t tmp = l->next;
    while(tmp){
        list_t p = list_new();
        p->data = f(tmp->data);
        tail->next = p;
        
        tmp = tmp->next;
        tail = p;
    }
    
    return new_list;
}


void list_print(list_t l, void (*f)(poly_t)){
    list_t tmp = l->next;
    printf("[");
    while(tmp){
        f(tmp->data);
        printf(", ");
        tmp = tmp->next;
    }
    printf("]");
}


// double-list.h, double-list.c, string-list.h, string-list.c


// ---------------------boxint.h---------------------
typedef int *boxint_t;
boxint_t_new(int i);
void boxint_print(boxint_t);

// ---------------------boxint.c---------------------
#include "boxint.h"
#include <stdio.h>
#include <malloc.h>

boxint_t boxint_t_new(int i){
    int *p = malloc(sizeof(*p));
    *p = i;
    
    return p;
}
void boxint_print(boxint_t p){
    printf("%d", *p);
}

// ---------------------main.c---------------------
#include <stdio.h>
#include "boxint.h"
#include "list.h"

/*
int add(int x, int y){
    return x + y;
}

int mul(int x, int y){
    return x * y;
}

int triple(int x){
    return x*x*x;
}

void print_int(int *p){
    printf("%d.\n", *p);
}
*/

int main(){
    list_t l = list_new();
    
    l = list_insert(l, boxint_new(1));
    l = list_insert(l, boxint_new(2));
    l = list_insert(l, boxint_new(3));
    l = list_insert(l, boxint_new(4));
    
    list_print(l, boxint_print);
    
    /*
    printf("fold_sum = %d.\n", list_fold(l, 0, add));
    printf("fold_mul = %d.\n", list_fold(l, 1, mul));
    
    printf("%d.\n", (list_fold(list_map(l, triple), 0, add)));
    */
    
    return 0;
}

```



