import time
from typing import List, Tuple, Optional


# return: the powerset, and the number of sets in the power set.
def powerset0(the_set: List[int], high: int) -> Tuple[List[List[int]], int]:
    if high < 0:
        return [[]], 1
    all_sets, nums = powerset0(the_set, high-1)
    for i in range(nums):
        new_set = all_sets[i].copy()
        new_set.append(the_set[high])
        all_sets.append(new_set)
    return all_sets, nums*2


def powerset(the_set: List[int]) -> List[List[int]]:
    start = time.perf_counter()
    all_sets, _ = powerset0(the_set, len(the_set) - 1)
    end = time.perf_counter()
    delta = (end - start)*1000
    print(f"finished in: {delta}毫秒")
    return all_sets

def print_sets(all_sets: List[List[int]]) -> None:
    print("[", end="")
    for s in all_sets:
        print(s, end=",\n")
    print("]")


# the subset sum problem
def subset_sum(the_set: List[int]) -> Optional[List[int]]:
    all_sets = powerset(the_set)
    for cur_set in all_sets:
        if len(cur_set) !=0 and sum(cur_set) == 0:
            return cur_set
    return None

if __name__ == "__main__":
    sets = powerset([1])
    print_sets(sets)
    sets = powerset([1, 2, 3])
    print_sets(sets)
    sets = powerset([i for i in range(20)])
    print_sets(sets)

    # may be too slow to run...
    # sets = powerset([i for i in range(50)])
    # print_sets(sets)

    # subset sum
    r = subset_sum([2, 3, 8, -5])
    if r is None:
        print("no solution")
    else:
        print(r)




















