from dataclasses import dataclass
from typing import List

import z3

try_Q = False

from z3 import *

## some non-linear examples:

@dataclass
class NonLinear:
    name: str
    constraint: List[BoolRef]

x, y = Real("x"), Real("y")
p, q = Int("p"), Int("q")
s, t = Int("s"), Int("t")

all_constraints = [
    NonLinear("circle",
              [x**2 + y**2 == 1.0]),
    NonLinear("ellipse",
              [x**2/4 + y**2/2 == 1.0]),
    NonLinear("parabola",
              [y**2 == 4*x]),
    NonLinear("hyperbola",
              [x**2/4 - y**2/2 == 1.0]),
    NonLinear("elliptic-1",
              [y**2 == x**3 - x]),
    NonLinear("elliptic-2",
              [y**2 == x**2 - x + 1]),
    NonLinear("elliptic-3",
              [y**2 == x**3 - 3*x + 2]),
    NonLinear("format-power-2",
              [x**2+y**2 == 1, x>0, y>0]),
    NonLinear("format-power-3",
              [x**3+y**3 == 1, x>0, y>0]),
    NonLinear("Galois",
              [x**5 - x + 1== 0]),
]

# 我们切换到有理数论域Q
if try_Q:
    all_constraints.append(NonLinear("format-power-2-Q",
              [x**2+y**2 == 1, p>0, q>0, s>0, t>0, x*q==p, y*s==t]))
    all_constraints.append(NonLinear("format-power-3-Q",
              [x**3+y**3 == 1, p>0, q>0, s>0, t>0, x*q==p, y*s==t]))

def doit():
    for c in all_constraints:
        solver = Solver()
        solver.add(c.constraint)
        res = solver.check()
        if res == sat:
            print(f"{c.name}: {c.constraint[0]}\n\tsolution: {solver.model()}")
        else:
            print(f"no solution: {c.name}")

if __name__ == "__main__":
    doit()



