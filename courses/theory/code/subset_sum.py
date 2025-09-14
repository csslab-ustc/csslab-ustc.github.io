import time
from set_lib import powerset, print_sets
from typing import Optional, Set

# the subset sum problem
def subset_sum(the_set: Set[int]) -> Optional[Set[int]]:
    all_sets = powerset(the_set)
    for cur_set in all_sets:
        if len(cur_set) !=0 and sum(cur_set) == 0:
            return cur_set
    return None

if __name__ == "__main__":
    sets = powerset({1})
    print_sets(sets)
    sets = powerset({1, 2, 3})
    print_sets(sets)
    sets = powerset({i for i in range(20)})
    print_sets(sets)

    # may be too slow to run... :-(
    # sets = powerset([i for i in range(50)])
    # print_sets(sets)

    # subset sum
    r = subset_sum({2, 3, 8, -5})
    if r is None:
        print("no solution")
    else:
        print(r)




















