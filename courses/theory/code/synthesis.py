from typing import List
import z3

debug = False

# the first example
# the sketch:
# H ::= V O V
# V ::= x | 0 | 1
# O ::= + | -


def printit(s):
    print(s, end="")

sketch = {
    "H": [lambda model: sketch["V"][model.eval(z3.Int("H_0")).as_long()](model),
          lambda model: sketch["O"][model.eval(z3.Int("H_1")).as_long()](model),
          lambda model: sketch["V"][model.eval(z3.Int("H_2")).as_long()](model)],
    "V": [lambda model: printit("x"),
          lambda model: printit("0"),
          lambda model: printit("1")],
    "O": [lambda model: printit(" + "),
          lambda model: printit(" - ")]
}

def H(x):
    return O(z3.Int("H_1"),
             V(z3.Int('H_0'), x),
             V(z3.Int('H_2'), x))

def O(s_o, x, y):
    return z3.If(s_o==0, x + y, x - y)

def V(s_v, x):
    return z3.If(s_v==0, x,
          z3.If(s_v==1, 0, 1))


# the second example
# the sketch:
# H ::= V O V
# V ::= x | y | True | False
# O ::= and | or

sketch2 = {
    "H": [lambda model: sketch2["V"][model.eval(z3.Int("H_0")).as_long()](model),
          lambda model: sketch2["O"][model.eval(z3.Int("H_1")).as_long()](model),
          lambda model: sketch2["V"][model.eval(z3.Int("H_2")).as_long()](model)],
    "V": [lambda model: printit("x"),
          lambda model: printit("y"),
          lambda model: printit("1"),
          lambda model: printit("0")],
    "O": [lambda model: printit(" & "),
          lambda model: printit(" | ")]
}


def H2(x, y):
    return O2(z3.Int("H_1"),
             V2(z3.Int('H_0'), x, y),
             V2(z3.Int('H_2'), x, y))

def O2(s_o, x, y):
    return z3.If(s_o==0, x & y, x | y)

def V2(s_v, x, y):
    return z3.If(s_v==0, x,
                 z3.If(s_v==1, y,
                    z3.If(s_v==2, z3.BitVecVal(0, 32),
                          z3.BitVecVal(1, 32))))



def print_fun(sketch, start, model, f, args):
    print("the synthesized function:")
    printit(f"def {f}(")
    print(*args, sep=", ", end="):\n")
    printit("    return ")
    rights = sketch[start]
    for f in rights:
        f(model)
    print("")


def solve(sketch, start, spec, f, args):
    solver = z3.Solver()
    solver.add(spec)
    res = solver.check()
    if res == z3.sat:
        if debug:
            print("sat")
        model = solver.model()
        if debug:
            print(model)
        print_fun(sketch, start, model, f, args)
    else:
        print("unsat")


if __name__ == "__main__":
    # example 1
    io_spec = z3.And([H(0) == 1,
                    H(1)==1,
                    H(2)==0])
    if debug:
        print(io_spec)
    solve(sketch, "H", io_spec, "f", ["x"])

    io_spec = z3.And([H(0) == 0,
                    H(1)==2,
                    H(2)==4])
    if debug:
        print(io_spec)
    solve(sketch, "H", io_spec, "f", ["x"])

    logic_spec = z3.And([z3.ForAll(z3.Int("x"), H(z3.Int("x"))== z3.Int("x")+1)])
    if debug:
        print(logic_spec)
    solve(sketch, "H", logic_spec, "f", ["x"])

    # example 2
    zero = z3.BitVecVal(0, 32)
    one = z3.BitVecVal(1, 32)
    io_spec = z3.And([H2(zero, zero) == zero,
                        H2(zero, one)== one,
                        H2(one, zero)== one])
    if debug:
        print(io_spec)
    solve(sketch2, "H", io_spec, "f", ["x", "y"])


