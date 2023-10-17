




with ExpectError():
    root = my_sqrt(0)


def my_sqrt_checked(x):
    root = my_sqrt(x)
    assertEquals(root * root, x)
    return root

my_sqrt_checked(2.0) # 1.414213562373095


from Timer import Timer
import random

with Timer() as t:
    for i in range(10000):
        x = 1 + random.random() * 1000000
        assertEquals(my_sqrt(x) * my_sqrt(x), x)
print(t.elapsed_time())





def assertEquals(x, y, rel_tol=1e-8):
    assert math.isclose(x, y, rel_tol)

assertEquals(my_sqrt(2) * my_sqrt(2), 2)  
assertEquals(my_sqrt(3) * my_sqrt(3), 3)
assertEquals(my_sqrt(42.11) * my_sqrt(42.11), 42.11)



x = 2
res = my_sqrt(2) * my_sqrt(2) # res: 1.9999999999999996
import math
math.isclose(x, res, rel_tol=1e-15) # true



my_sqrt_with_log(9)
'''
output:
approx = None
approx = 4.5
approx = 3.25
approx = 3.0096153846153846
approx = 3.000015360039322
approx = 3.0000000000393214
3.0
'''






def my_sqrt_with_log(x):
    """Computes the square root of x, using the Newton–Raphson method"""
    approx = None
    guess = x / 2
    while approx != guess:
        print("approx =", approx)  # <-- New
        approx = guess
        guess = (approx + x / approx) / 2
    return approx



my_sqrt(4) # output: 2.0
my_sqrt(2) # output: 1.414213562373095




def my_sqrt(x):
    """Computes the square root of x, using the Newton-Raphson method"""
    approx = None
    guess = x / 2
    while approx != guess:
        approx = guess
        guess = (approx + x / approx) / 2
    return approx

