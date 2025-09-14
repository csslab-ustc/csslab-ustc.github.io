import time
from typing import List, Set


DEBUG = False


# return: the powerset, and the number of sets in the power set.
def powerset0(the_set: Set[int]) -> List[Set[int]]:
    if len(the_set) <= 0:
        empty_set: Set[int] = set()
        return [empty_set]
    element = the_set.pop()
    the_partial_powerset = powerset0(the_set)
    # to avoid infinite recursion
    temp_sets = the_partial_powerset.copy()
    for each_set in temp_sets:
        new_each_set = each_set.union({element})
        the_partial_powerset.append(new_each_set)
    return the_partial_powerset


def powerset(the_set: Set[int]) -> List[Set[int]]:
    num_elements: int = len(the_set)
    start = time.perf_counter()
    the_powerset = powerset0(the_set)
    end = time.perf_counter()
    delta = (end - start)*1000
    print(f"power set for a set with {num_elements} elements, used: {delta}毫秒")
    return the_powerset

def print_sets(all_sets: List[Set[int]]) -> None:
    if not DEBUG:
        return
    print("[", end="")
    for s in all_sets:
        print(s, end=",\n")
    print("]")
    print(f"power set numbers: {len(all_sets)}")

if __name__ == "__main__":
    '''
    some sample code
    '''
    # create some sets
    set1: Set[int] = {1, 2, 3}
    set2: Set[int] = {2, 3, 4}
    print(set1)
    print(set2)

    # set operations
    set3: Set[int] = set1.union(set2)
    print(set3)

    set4 = set1.intersection(set2)
    print(set4)

    ''' power set '''
    the_power_set: List[Set[int]] = powerset({1})
    print_sets(the_power_set)
    the_power_set = powerset({1, 2, 3})
    print_sets(the_power_set)

    # caution: may be too slow to run... :-(
    for num in range(1, 50):
        the_power_set = powerset({i for i in range(num)})
        print_sets(the_power_set)















