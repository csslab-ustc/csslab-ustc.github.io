"""
Knapsack problem

The knapsack problem is a typical optimization problem that has been
studied for hundred of years.
The problem is: given a set of items, each
of which has a weight and a value, determine a set of items such that the
total weight is less than a given limit C but with the maximum value.

This problem is NPC, and for more background information of the
knapsack problem, please refer to:
https://en.wikipedia.org/wiki/Knapsack_problem

More formal problem description: given items, with specific weight:
   W = {w_1, ..., w_n}
and value:
   V = {v_1, ..., v_n}
For a given knapsack of maximum capacity C, how to choose a subset of
items to maximize
   max(v_i + ... + v_k)
without exceeding the capacity:
   w_i + ... + w_k <= C   

Here is a concrete example:
   W = {4, 6,  2, 2, 5, 1}
   V = {8, 10, 6, 3, 7, 2}
and C = 12.
The expected result is: we should select the first, second, and third items, 
and the total value is:
   8 + 10 + 6 = 24

In this code, we will implement a simplified version of
the knapsack problem, in which we only require the total weight
of items is than the given limit C, but which does not necessarily
maximize the value.
To this end, the problem can be solved by SAT.
"""

import time
from typing import List, Tuple

from z3 import *

debug: bool = False

# return the constraint and the flags
def generate_constraints(weights: List[int], capacity: int) -> Tuple[BoolRef, List[BoolRef]]:
    size = len(weights)
    flags: List[BoolRef] = [Bool(f"x_{i}") for i in range(size)]
    constraints: List[BoolRef] = [(If(flags[i], weights[i], 0)) for i in range(size)]
    non_empty: BoolRef = Or(flags)
    return And(sum(constraints) <= capacity, non_empty), flags


def _01_knapsack_sat(weights: List[int], values: List[int], capacity: int):
    # step #1: generate the constraints
    constraints, flags = generate_constraints(weights, capacity)
    if debug:
        print(f"constraints: {constraints}")

    # step #2: solve the constraints
    solver = Solver()
    solver.add(constraints)

    start = time.time()
    result = solver.check()
    end = time.time()
    print(f"01_knapsack_sat solved {len(weights)} items in {(end - start):.6f}s")

    if result == sat:
        model = solver.model()
        # print the items
        print(f"the weight: {weights} with capacity: {capacity}")
        for i in range(len(weights)):
            if model.eval(flags[i]):
                print(f"index: [{i}] with weight: {weights[i]}")
            else:
                pass
    else:
        print("no solution")


def generate_large_test(capacity: int, max_numbers: int) -> List[int]:
    weights: List[int] = [(capacity + 1) for _ in range(max_numbers)]
    weights[max_numbers - 1] = capacity
    return weights


if __name__ == '__main__':
    # test case 1
    W = [4, 6,  2, 2, 5, 1]
    V = [8, 10, 6, 3, 7, 2]
    C = 12
    _01_knapsack_sat(W, V, C)

    # another test case
    W = [23, 26, 20, 18, 32, 27, 29, 26, 30, 27]
    V = [505, 352, 458, 220, 354, 414, 498, 545, 473, 543]
    C = 67
    _01_knapsack_sat(W, V, C)

    # a large test case:
    #
    C = 10000
    max_number = 100
    W = generate_large_test(C, max_number)
    V = W
    _01_knapsack_sat(W, V, C)


