from nagini_contracts.contracts import *
from typing import List

# basic pre- and post-conditions
def inc(x: int)-> int:
    Requires(x >= 0)
    Ensures(Result() >= 1)

    return x + 1


# branching
def abs(x: int) -> int:
    Requires(True)
    Ensures(Result() >= 0)

    if x >= 0:
        return x
    else:
        return 0-x

def abs_strong(x: int) -> int:
    Requires(True)
    Ensures(Result() == (x if x>=0 else 0-x))

    if x >= 0:
        return x
    else:
        return 0-x

# loops
# def loop_fun(x: int) -> int:
#     Requires(True)
#     Ensures(Result() == 5)

#     while x < 5:
#         x = x + 1
#     return x

def loop_fun2(x: int) -> int:
    Requires(x<=5)
    Ensures(Result() == 5)

    while x < 5:
        Invariant(x<=5)
        x = x + 1
    return x


# function
def callee(size: int) -> List[int]:
    Requires(size > 0)
    Ensures(list_pred(ResultT(List[int])))
    Ensures(len(Result()) > 0)
    Ensures(Forall(ResultT(List[int]), lambda x: x >= 0))

    l: List[int] = [0]
    i: int = 1
    while i<size:
        Invariant(list_pred(l))
        Invariant(len(l) > 0)
        Invariant(i >= 1)
        Invariant(Forall(l, lambda x: x >= 0))

        l.append(i)
        i += 1
    return l

def caller(n: int)-> int:
    Requires(n >= 1)
    Ensures(Result() >= 0)

    l = callee(n)
    return l[0]

# specification-oriented programming
def mysum(n: int)->int:
    Requires(n >= 0)
    Ensures(Result() *2 == n*(n+1))

    s: int = 0
    i: int = 1
    while i<=n:
        Invariant(i<=(n+1))
        Invariant(s*2 == (i-1)*(i))
        s += i
        i += 1
    return s


@Pure
def mysum_spec2(n: int)->int:
    if(n<=0):
        return 0
    else:
        return n+mysum_spec2(n-1)


@Pure
def mysum_spec(n: int)->int:
    match n:
        case 0: return 0
        case _: return n+mysum_spec(n-1)

# specification-oriented programming
def mysum2(n: int)->int:
    Requires(n >= 0)
    Ensures(Result() == mysum_spec(n))

    s: int = 0
    i: int = 1
    while i<=n:
        Invariant(i>=1 and i<=(n+1))
        Invariant(s == mysum_spec(i-1))

        s += i
        i += 1
    return s

@Pure
def fib_spec(n: int)->int:
    if(n<=1):
        return 1
    else:
        return fib_spec(n-2) + fib_spec(n-1)

def test_fib_spec(n: int)->None:
    Requires(n >= 2)
    Ensures(
        fib_spec(n) == fib_spec(n-2) + fib_spec(n-1)
    )
    return 

def fib(n: int)->int:
    Requires(n>=0)
    Ensures(Result() == fib_spec(n))

    if n<=1:
        return 1

    first: int = 1
    second: int = 1
    i: int = 2

    while i<=n:
        Invariant(i>=2 and i<=(n+1))
        Invariant(first == fib_spec(i-2))
        Invariant(second == fib_spec(i-1))

        temp: int = first
        first = second
        second += temp
        i += 1

    return second

