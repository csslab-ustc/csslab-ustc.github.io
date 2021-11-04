import z3

# Find Solution Set That Can Make Logical Expression P/\Q be True
P, Q = z3.Bools('P Q')
F = z3.And(P, Q)
solver = z3.Solver()
solver.add(F)
print(solver.check())
print(solver.model())
