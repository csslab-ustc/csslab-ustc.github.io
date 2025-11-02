from z3 import *

x, y = Ints('x y')
x, y = BitVecs('x y', 8)
# x = BitVecVal(3, 8)
# y = BitVecVal(125, 8)
solver = Solver()
solver.add(x >=0, y >=0, (x+y)/2<0)
result = solver.check()
model = solver.model()
print(model)
print((model.eval((x+y)/2)))
print((-1)/2)

a, b = Bools('a b')
solve(Xor(a, b))

'''
[c_3, c2, c1, c0]
[a2, a1, a0]
[b2, b1, b0]

[d2, d1, d0]
'''

def print_bits(model, bits):
    binary_bits = []
    for bit in bits:
        if model[bit]:
            print("1", end="")
            binary_bits.append(1)
        else:
            print("0", end="")
            binary_bits.append(0)
    print("")
    # get the value
    value = 0
    for index in range(len(binary_bits)-1):
        value += binary_bits[index] * pow(2, index)
    if binary_bits[len(binary_bits)-1] == 1:
        value -= pow(2, len(binary_bits)-1)
    print(value)

N = 8

carry_bits = [Bool(f"c_{i}") for i in range(N+1)]
a_bits = [Bool(f"a_{i}") for i in range(N)]
b_bits = [Bool(f"b_{i}") for i in range(N)]
d_bits = [Bool(f"d_{i}") for i in range(N)]

print(carry_bits, a_bits, b_bits)

solver = Solver()
cons = [Not(carry_bits[0])]
for index in range(N):
    cons_0_d = d_bits[index] == Xor(Xor(a_bits[index], b_bits[index]), carry_bits[index])
    cons_0_c = carry_bits[index+1] == Or(And(a_bits[index], b_bits[index]),
                               And(Xor(a_bits[index], b_bits[index]),
                                   carry_bits[index]))
    # global cons
    cons.append(cons_0_d)
    cons.append(cons_0_c)

print(cons)
solver.add(cons)

## extra constraints:
solver.add(Not(a_bits[N-1]),
            Not(b_bits[N-1]),
           (d_bits[N-1]))

result = solver.check()
model = solver.model()
print(model)
print_bits(model, a_bits)
print_bits(model, b_bits)
print_bits(model, d_bits)


import ctypes

c1 = ctypes.c_int8(67)
c2 = ctypes.c_int8(65)
print(ctypes.c_int8(c1.value + c2.value))
