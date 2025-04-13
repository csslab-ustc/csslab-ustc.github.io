from z3 import *
import sys

debug: bool = True

########################################
# Some IMO problems.

# for any positive integer n
def imo_1959_p1():
    pass

"""
1981, p3.
m, n 都属于{1, 2, ..., 1981}，且满足(m^2-mn-n^2)^2 = 1,
求m^2+n^2的最大值。
"""
def imo_1981_p3():
    N = 1981
    m, n = Ints('m n')
    opt = Optimize()
    opt.add(m>=1, m<=N)
    opt.add(n>=1, n<=N)
    opt.add(m*m-m*n-n*n==1)
    opt.maximize(m*m+n*n)
    res = opt.check()
    if res == sat:
        print(opt.model())
    else:
        print('unsat')





if __name__ == '__main__':
    imo_1981_p3()










