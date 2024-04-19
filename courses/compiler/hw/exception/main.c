#include <stdio.h>
#include "estack.h"
#include "excp.h"

void f();

void g();

int main() {
    // init the exception handler stack
    estack_INIT ();

    // Example #1: no throw
    TRY
        {
            printf("example #1:\n");
        }
    CATCH(0)
        {
            printf("caught: 0!\n");
        }
    ENDTRY;

    // Example #2: throw in try
    TRY
        {
            printf("example #2:\n");
            THROW(3);
        }
    CATCH(1)
        {
            printf("Caught: 1\n");
        }
    CATCH(3)
        {
            printf("Caught: 3\n");
        }
    ENDTRY;

    // Example #3: throw in deep function call chain
    TRY
        {
            printf("example #3:\n");
            f();
        }
    CATCH(2)
        {
            printf("Caught: 2\n");
        }
    CATCH(5)
        {
            printf("Caught: 5\n");
        }
    ENDTRY;

    // Example #4: unhandled exception
    THROW(99);

    return 0;
}


void f() {
    g();
}

void g() {
    THROW(2);
}
