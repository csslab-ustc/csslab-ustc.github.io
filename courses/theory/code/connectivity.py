from z3 import *

debug: bool = True

########################################
# Dynamic connectivity.

N = 10

# Step 1: declare new sorts in Z3 using "DeclareSort"
# think "sort" as "structures" in C or "class" in Java.
# here, we use sort to formalize point
point_sort = DeclareSort('point_sort')

# create ten points: p_0 to p_9
points = [Const(f'p_{i}', point_sort)
          for i in range(N)]

# establish known connectivity
know_connectivity = [(4, 3),
           (8, 3),
           (6, 5),
           (9, 4),
           (2, 1)
                     ]

props = []
# the rows
for i in range(N-1):
    if (i+1, i) in know_connectivity:
        # print(f"{points[i]} == {points[i+1]}")
        props.append(points[i] == points[i+1])
    else:
        # print(f"{points[i]} != {points[i+1]}")
        props.append(points[i] != points[i+1])
# the columns
for i in range(N//2):
    if (i+N//2, i) in know_connectivity:
        # print(f"{points[i]} == {points[i+N//2]}")
        props.append(points[i] == points[i+N//2])
    else:
        # print(f"{points[i]} != {points[i+N//2]}")
        props.append(points[i] != points[i+N//2])

# a magic
# we should dynamically adjust the layout:
props.remove(points[8] != points[9])


def check(p, q):
    the_prop = And(And(props), p != q)
    solver = Solver()
    solver.add(the_prop)
    # check connectivity
    res = solver.check()
    if res == sat:
        print('sat')
        model = solver.model()
        print(model)
    else:
        print('unsat')


if __name__ == '__main__':
    check(points[3], points[9])
    check(points[0], points[9])









