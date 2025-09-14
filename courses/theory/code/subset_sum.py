from typing import Optional, Set
from set_lib import powerset


# the subset sum problem
def subset_sum(the_set: Set[int]) -> Optional[Set[int]]:
    the_power_set = powerset(the_set)
    for each_set in the_power_set:
        if len(each_set) !=0 and sum(each_set) == 0:
            return each_set
    return None

def print_solution(solution: Optional[Set[int]]) -> None:
    if solution is None:
        print("no solution")
    else:
        print(f"found a solution: {solution}")

if __name__ == "__main__":
    r = subset_sum({2, 3, 8, -5})
    print_solution(r)

    # a challenging problem
    the_set = {i for i in range(1, 20)}
    the_set.add(-1)
    r = subset_sum(the_set)
    print_solution(r)





















