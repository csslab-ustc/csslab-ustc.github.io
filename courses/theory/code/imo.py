import threading
import time
from math import floor
from typing import List, Tuple

from z3 import *

DEBUG: bool = True

########################################
# Some IMO problems.

all_problems = []

"""
1959, p1.
# 求证: 对于任意正整数n, 分数(21n+4)/(14n+3)不可约。
"""
def imo_1959_p1():
    ctx = Context()
    solver = Solver(ctx=ctx)
    n = Int('n', ctx=ctx)
    s = Int('s', ctx=ctx)
    t = Int('t', ctx=ctx)
    """
      (21n+4)      s
      --------- = ----  
      (14n+3)      t
    """

    solver.add(n>=1, s>=1, t>=1)
    solver.add((21*n+4)*t==(14*n+3)*s, s<(21*n+4), s>t, 2*s < 3*t)
    result = solver.check()
    if result == sat:
        print(solver.model())
    else:
        print('1959, p1: unsat')

all_problems.append(imo_1959_p1)


"""
1960, p2.
求所有可被11整除的三位数, 使得所除之商正好等于该三位数十进制的三位数字
平方的和。
"""
def imo_1960_p2():
    ctx = Context()
    solver = Solver(ctx=ctx)
    # abc
    a, b, c = Ints('a b c', ctx=ctx)
    t = Int('t', ctx=ctx)
    solver.add(a>=1, b>=0, c>=0)
    solver.add((a*100+b*10+c)==t*11, 
               t==a*a+b*b+c*c)
    loop = True
    num_of_solutions = 0
    while loop:
      res = solver.check()
      if res == sat:
          num_of_solutions += 1
          print(solver.model(), end=", ")
          a_value, b_value, c_value = \
            solver.model()[a], solver.model()[b], solver.model()[c]
          print(f"abc={a_value}{b_value}{c_value}")
          prop = And([a==a_value, b==b_value, c==c_value])
          solver.add(Not(prop))
      else:
          loop = False
          if num_of_solutions == 0:
            print('1960, p2: unsat')

all_problems.append(imo_1960_p2)

"""
1962, p1.
求满足下列条件的最小自然数n:
其十进制形式尾数为6, 如把末尾的6移到最前面后,
得到数是原数的4倍。
"""
def imo_1962_p1():
    # calculate the value of a list of digit
    # the most significant bit is at the rightmost
    # e.g., [1, 2, 3]  ==> 321
    def get_value(the_digits: List[Any]) -> Any:
      the_value = 0
      for i in range(len(the_digits)):
        the_value += the_digits[i] * pow(10, i)
      # print(the_value)
      return the_value
    
    def try_num(num_digits: int) -> Tuple[Any, List[Any], Any]:
      ctx = Context()
      solver = Solver(ctx=ctx)
      original_digits = [Int(f"x_{i}", ctx=ctx) for i in range(num_digits)]
      # print(f"{original_digits}")
      original_value = get_value(original_digits)
      # print(original_value)
      
      # move the element
      new_digits = [original_digits[i] for i in range(1, len(original_digits))]
      new_digits.append(original_digits[0])
      # print(new_digits)
      new_value = get_value(new_digits)

      for d in original_digits:
        solver.add(d>=0, d<=9)
      solver.add(original_digits[num_digits - 1] != 0)
      solver.add(original_digits[0] == 6)
      solver.add(new_value == original_value*4)
      res = solver.check()
      if res == sat:
        # print("sat: ")
        # print(solver.model())
        return res, original_digits, solver.model()
      else:
        # print("1962: unsat")
        return res, [], None
    
    # we try from smaller to larger one, so that we can
    # find the smallest one
    for num_digits in range(2, 20):
      res, digits, model = try_num(num_digits)
      if res == sat:
        digits.reverse()
        print("the smallest: ", end="")
        for d in digits:
          print(model[d], end="")
        print("")
        break

all_problems.append(imo_1962_p1)


"""
1977, p5.
设正整数a, b满足a^2+b^2除以a+b的商是q，余数是r， 
求出使得q^2+r=1977的所有可能的a、b.
"""
def imo_1977_p5():
    ctx = Context()
    solver = Solver(ctx=ctx)
    a, b = Ints('a b', ctx=ctx)
    q, r = Ints('q r', ctx=ctx)
    solver.add(a>=1, b>=1, q>0, r>=0, r<(a+b))
    solver.add(a*a+b*b==(a+b)*q+r)
    solver.add(q*q+r==1977)
    num_of_solutions = 0
    loop = True
    while loop:
        res = solver.check()
        if res == sat:
            num_of_solutions += 1
            model = solver.model()
            print(model)
            solver.add(Not(And(a==solver.model()[a],
                           b==solver.model()[b])))
        else:
            loop = False
            if num_of_solutions == 0:
                print('1977, p5: unsat')

all_problems.append(imo_1977_p5)

"""
1981, p3.
m, n 都属于{1, 2, ..., 1981}，且满足(m^2-mn-n^2)^2 = 1,
求m^2+n^2的最大值。
"""
def imo_1981_p3():
    ctx = Context()
    opt = Optimize(ctx=ctx)
    N = 1981
    m, n = Ints('m n', ctx=ctx)
    opt.add(m>=1, m<=N)
    opt.add(n>=1, n<=N)
    opt.add(Or(m*m-m*n-n*n==1, m*m-m*n-n*n==-1))
    opt.maximize(m*m+n*n)
    res = opt.check()
    if res == sat:
        model = opt.model()
        m_value = model[m].as_long()
        n_value = model[n].as_long()
        max_value = m_value*m_value+n_value*n_value
        print(f"{model}, max value = {max_value}")
    else:
        print('1981, p3: unsat')

all_problems.append(imo_1981_p3)


"""
1982, p4.
n是正整数，假设x^3-3xy^2+y^3=n有一组整数解x，y，
则此方程至少有三组整数解。
并证明：当n=2981时，它没有整数解。
"""
def imo_1982_p4():
    ctx = Context()
    solver = Solver(ctx=ctx)
    N = 2891
    x, y, n = Ints('x y n', ctx=ctx)
    solver.add(n==8)
    solver.add(x*x*x - 3*x*y*y+y*y*y==n)
    num_of_solutions = 0
    while True:
        res = solver.check()
        if res == sat:
            model = solver.model()
            print(model)

            # solver.add(n == model[n])
            solver.add(x > (model[x]))
            num_of_solutions += 1
            if num_of_solutions >= 3:
                break
        else:
            print('1982, p4: unsat')

all_problems.append(imo_1982_p4)


"""
1986, p1.
给定正整数d， 
证明: 2d-1、5d-1、13d-1不可能都是平方数.
"""
def imo_1986_p1():
    ctx = Context()
    solver = Solver(ctx=ctx)
    d, x, y, z = Ints('d x y z', ctx=ctx)

    solver.add(d>=1, x>=1, y>=1, z>=1)
    # solver.add(d<=10000)
    solver.add(2*d-1==x*x, 5*d-1==y*y, 13*d-1==z*z)
    res = solver.check()
    if res == sat:
        print(solver.model())
    else:
        print('1986, p1: unsat')

# all_problems.append(imo_1986_p1)

"""
1988, p6.
设正整数a, b满足ab+1可以整除a^2+b^2, 
证明: (a^2+b^2)/(ab+1) 一定是某个整数的平方.
"""
def imo_1988_p6():
    ctx = Context()
    solver = Solver(ctx=ctx)
    a, b = Ints('a b', ctx=ctx)
    k, t = Ints('k t', ctx=ctx)

    solver.add(a>=1, b>=1)
    solver.add(k>=1, t>=1, t<k)
    solver.add(a*a+b*b==(a*b+1)*k)
    solver.add(ForAll([t], k!=t*t))
    res = solver.check()
    if res == sat:
        print(solver.model())
    else:
        print('1988, p6: unsat')

all_problems.append(imo_1988_p6)

"""
1992, p1.
设正整数a, b, c满足1<a<b<c,
且（a-1）(b-1)(c-1)是abc-1的因子。 
求a, b, c.
"""
def imo_1992_p1():
    ctx = Context()
    solver = Solver(ctx=ctx)
    a, b, c = Ints('a b c', ctx=ctx)
    t = Int('t', ctx=ctx)

    solver.add(a>1, b>a, c>b)
    solver.add(a*b*c-1==(a-1)*(b-1)*(c-1)*t)
    num_of_solutions = 0
    loop = True
    while loop:
        res = solver.check()
        if res == sat:
            num_of_solutions += 1
            print(solver.model())
            solver.add(Not(And([a==solver.model()[a],
                               b==solver.model()[b],
                               c==solver.model()[c]])))
        else:
            loop = False
            if num_of_solutions == 0:
                print('1988, p6: unsat')

all_problems.append(imo_1992_p1)

"""
1994, p4.
确定使得(n^3+1)/(n*m-1)是整数的所有正整数m、n.
"""
def imo_1994_p4():
    ctx = Context()
    solver = Solver(ctx=ctx)
    m, n, t = Ints('m n t', ctx=ctx)

    solver.add(m>=1, n>=1)
    solver.add(n*n*n+1==(n*m-1)*t)
    num_of_solutions = 0
    loop = True
    while loop:
        res = solver.check()
        if res == sat:
            num_of_solutions += 1
            print(solver.model())
            solver.add(Not(And([m==solver.model()[m],
                               n==solver.model()[n]])))
        else:
            loop = False
            if num_of_solutions == 0:
                print('1994, p4: unsat')

# all_problems.append(imo_1994_p4)

"""
1996, p4.
正整数a, b使得15a+16b和16a-15b都是完全平方数,
求这两个平方数中较小数的最小值.
"""
def imo_1996_p4():
    ctx = Context()
    solver = Solver(ctx=ctx)
    a, b, s, t = Ints('a b s t', ctx=ctx)

    solver.add(a>=1, b>=1, s>=1, t>=1)
    solver.add(t <= 2)
    solver.add(15*a+16*b==s*s, 16*a-15*b==t*t)
    res = solver.check()
    if res == sat:
        print(solver.model())
    else:
        print('1996, p4: unsat')

# all_problems.append(imo_1996_p4)


"""
2001, p6.
已知正整数a > b > c > d，满足
ac+bd = (a+b-c+d)(-a+b+c+d).
证明：ab+cd是合数.
"""
def imo_2001_p6():
    ctx = Context()
    solver = Solver(ctx=ctx)
    a, b, c, d, s, t = Ints('a b c d s t', ctx=ctx)

    solver.add(a>=1, b>=1, c>=1, d>=1, s>=1, t>=1)
    solver.add(a*c + b*d == (a+b-c+d)*(-a+b+c+d))
    solver.add((a * b + c*d) == s*t)
    res = solver.check()
    if res == sat:
        print(solver.model())
    else:
        print('2001, p6: unsat')

all_problems.append(imo_2001_p6)


"""
2007, p5.
给定正整数a, b，证明：
如果 （4ab-1）/(4a^2-1)^2是整数，则有a=b.
"""
def imo_2007_p5():
    ctx = Context()
    solver = Solver(ctx=ctx)
    a, b, t = Ints('a b t', ctx=ctx)

    solver.add(a>=1, b>=1, t>=1)
    solver.add(t*(4*a*b-1)==(4*a*a-1)*(4*a*a-1))
    solver.add(a != b)
    res = solver.check()
    if res == sat:
        print(solver.model())
    else:
        print('2007, p5: unsat')

# all_problems.append(imo_2007_p5)

###
# end of problems


should_be_sequential = True
sem = threading.Semaphore(1)

def wrap(f):
    if should_be_sequential:
        sem.acquire()
    print(f"\nsolving {f.__name__} starting ...")
    f()
    print(f"solving {f.__name__} finished")
    if should_be_sequential:
        sem.release()

if __name__ == '__main__':
    for problem in all_problems:
        print(problem.__name__, end=", ")

    start = time.time()
    all_threads = []
    for problem in all_problems:
        thread = threading.Thread(target=wrap, args=(problem, ))
        all_threads.append(thread)
        thread.start()
    # wait for all threads
    for thread in all_threads:
        thread.join()
    end = time.time()
    duration = end-start
    print(f"\nSummary: solved {len(all_problems)} problems in {duration} seconds")










