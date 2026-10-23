from typing import Callable, List

from hypothesis import given, settings, Verbosity
from hypothesis import strategies as st

## Part I: some basic testing for integer functions

# we are given a target function of addition to be tested, 
# which comprises a deliberate bug:
def myadd(x: int, y: int)-> int:
    match x:
        case 1234567890: return y     # a bug!
        case _: return x + y

# we write properties that the addition function should satisfy.
# the first property specifies that addition function
# satisfies the law of communatativity:
def add_prop_comm(f: Callable[[int, int], int], x: int, y: int):
    assert f(x, y) == f(y, x)

# the second property specifies that addition function 
# has a right identify element of "zero":
def add_prop_left_identify(f: Callable[[int, int], int], x: int, y: int):
    assert f(0, x) == x

# the third property specifies that addition function 
# has a right identify element of "zero":
def add_prop_right_identify(f: Callable[[int, int], int], x: int, y: int):
    assert f(x, 0) == x

# the fourth property specifies that addition function 
# gives an inverse element -x, for each x:
def add_prop_inverse(f: Callable[[int, int], int], x: int, y: int):
    assert f(x, -x) == 0

# we write generators to generate random numbers, 
# which are further leveraged to test the aforementioned properties:
@given(st.integers(), st.integers())
@settings(max_examples=10000)
def test_add(x: int, y: int):
    add_prop_comm(myadd, x, y)
    add_prop_left_identify(myadd, x, y)
    add_prop_right_identify(myadd, x, y)
    add_prop_inverse(myadd, x, y)


# another target function to be tested, 
# the division function is special in that it is partial, 
# that is, it does not defined on the input values: (x, 0)
def mydiv(x: int, y: int)->int:
    if y == 0:
        raise RuntimeError()
    return x//y

# the first property specifies the legal range for the quotient:
def div_prop_range(f: Callable[[int, int], int], x: int, y: int):
    result = f(x, y)
    assert result * y <= x < (result + 1) * y if y > 0 else \
           (result + 1) * y < x <= result * y

# the second property specifies the quotient is always 0, when the dividen is 0:
def div_prop_zero(f: Callable[[int, int], int], x: int, y: int):
    assert f(0, y) == 0

nonzeros = st.integers().filter(lambda n: n!=0)
@given(st.integers(), nonzeros)
@settings(max_examples=10000)
def test_div(x: int, y: int):
    div_prop_range(mydiv, x, y)
    div_prop_zero(mydiv, x, y)


## Part II: testing list 

# we are given a (buggy) function of list reverse, which should be tested:
def list_rev(l: List[int]) -> List[int]:
    # match l:
    #     case []: 
    #         return []
    #     case [head, *tail]: 
    #         t = list_rev(tail)
    #         t.append(head)
    #         return t
    # raise RuntimeError()
    return l


# the first property specifies the reverse function is inversable:
def list_rev_prop_inverse(f: Callable[[List[int]], List[int]], l: List[int]):
    assert f(f(l)) == l

# the second property specifies the reverse function should return the same
# set of elements:
def list_rev_prop_same_set(f: Callable[[List[int]], List[int]], l: List[int]):
    result = f(l)
    assert set(l) == set(result)

# the third property specifies the reverse function should return elements
# in a specified order:
def list_rev_prop_order(f: Callable[[List[int]], List[int]], l: List[int]):
    n = len(l)
    result = f(l)
    assert all(l[i] == result[n-1-i] for i in range(0, n))

@given(st.lists(st.integers()))
@settings(max_examples=10000)
def test_list_rev(l: List[int]):
    list_rev_prop_inverse(list_rev, l)
    list_rev_prop_same_set(list_rev, l)
    list_rev_prop_order(list_rev, l)


# we are given a (buggy) function of list sorting, which should be tested:
def list_sort(l: List[int]) -> List[int]:
    # l1 = l.copy()
    # l1.sort()
    # return l1
    return l

# the first property specifies the sorting function should be idempotent:
def list_sort_prop_idempotence(f: Callable[[List[int]], List[int]], l: List[int]):
    assert f(f(l)) == f(l)

# the second property specifies the sorting function should return the same
# set of elements:
def list_sort_prop_same_set(f: Callable[[List[int]], List[int]], l: List[int]):
    result = list_sort(l)
    assert set(result) == set(l)

# the third property specifies the sorting function should return
# elements in an ascending order:
def list_sort_prop_order(f: Callable[[List[int]], List[int]], l: List[int]):
    result = list_sort(l)
    assert all(result[i]<=result[i+1] for i in range(0, len(l)-1))

# generators
@given(st.lists(st.integers()))
@settings(max_examples=100)
def test_list_sort(l):
    list_sort_prop_idempotence(list_sort, l)
    list_sort_prop_same_set(list_sort, l)
    list_sort_prop_order(list_sort, l)


## Part III: complex testing scenarios that may defeat normal PBTs

def nest_add(x: int, y: int) -> int:
    if x == 123456789:
        if y == 987654321:
            return 0
    return x+y

def add_prop(f, x, y):
    assert nest_add(x, y) == x+y

@given(st.integers(), st.integers())
@settings(max_examples=10000)
# @settings(backend="crosshair", max_examples=10000, verbosity=Verbosity.verbose)
def test_nest_add(x, y):
    add_prop(nest_add, x, y)



if __name__ == "__main__":
    test_add()
    test_div()
    test_list_rev()
    test_list_sort()
    test_nest_add()

