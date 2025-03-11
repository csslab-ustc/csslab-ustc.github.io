"""
The subset sum problem, via the SAT approach.
"""

# to dump detailed information
debug = False

from typing import List, Dict, Tuple
from z3 import *

def generate_constraints(target_set: List[int], target: int) \
        -> Tuple[z3.BoolRef, Dict[int, BoolRef]]:
    set_len: int = len(target_set)
    index2bool: Dict[int, BoolRef] = {}
    bools: List[BoolRef] = [Bool(f"x_{i}") for i in range(set_len)]
    for idx in range(set_len):
        index2bool[idx] = Bool(f"x_{idx}")
    constraints = [If(bools[i], target_set[i], 0) for i in range(set_len)]
    prop_sum = sum(constraints) == target
    prop_nonempty = Or(bools)
    return And(prop_sum, prop_nonempty), index2bool


def subset_sum(target_set: List[int], target_num: int):
    solver = Solver()
    constraints, the_map = generate_constraints(target_set, target_num)
    if debug:
        print("the constraints are:")
        print(constraints)
    solver.add(constraints)
    if solver.check() == sat:
        model: ModelRef = solver.model()
        # output the solution (i.e., the subset):
        print("subset = {", end="")
        for i in range(len(target_set)):
            if model.eval(the_map[i]):
                print(f"{target_set[i]}, ", end="")
        print("}")
    else:
        print(f"the set {target_set} has no subset with sum of {target_num}")


if __name__ == '__main__':
    # the target set
    the_set = [2, 3, 8, -5]
    # look for a subset of the "the_set" whose sum is the "target_num"
    subset_sum(the_set, 0)






