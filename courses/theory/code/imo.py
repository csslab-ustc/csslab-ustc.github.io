from z3 import *
import sys

debug: bool = True

########################################
# Some IMO problems.

"""
1959, p1.
# 求证, 对于任意正整数n, 分数(21n+4)/(14n+3)不可约。
"""
def imo_1959():
    n = Int('n')
    s = Int('s')
    t = Int('t')
    """
      (21n+4)      s
      --------- = ----  
      (14n+3)      t
    """
    solver = Solver()
    solver.add(n>=1, s>=1, t>=1, n<100)
    solver.add((21*n+4)*t==(14*n+3)*s, s<(21*n+4), s>t)
    res = solver.check()
    if res == sat:
        print(solver.model())
    else:
        print('1959: unsat')
        
"""
1960, p2.
求所有可被11整除的三位数, 使得所除之商正好等于其十进制三位数字
平凡的和。
"""
def imo_1960():
    # abc
    a, b, c = Ints('a b c')
    t = Int('t')
    solver = Solver()
    solver.add(a>=1, b>=0, c>=0)
    solver.add((a*100+b*10+c)==t*11, 
               t==a*a+b*b+c*c)
    loop = True
    num_of_solutions = 0
    while(loop):
      res = solver.check()
      if res == sat:
          num_of_solutions += 1
          print(solver.model())
          a_value, b_value, c_value = \
            solver.model()[a], solver.model()[b], solver.model()[c]
          print(f"{a_value}{b_value}{c_value}")
          prop = And([a==a_value, b==b_value, c==c_value])
          solver.add(Not(prop))
      else:
          loop = False
          if num_of_solutions == 0:
            print('1960: unsat')

"""
1962, p1.
求满足下列条件的最小自然数n, 其十进制尾数为6, 如把末尾的6移到最前面后,
得到数是原数的4倍。
"""
def imo_1962():
    # abc
    def get_value(l: list):
      the_value = 0
      for i in range(len(l)):
        the_value += l[i] * pow(10, i)
      # print(the_value)
      return the_value
    
    def num(n: int) -> int:
      the_digits = [Int(f"x_{i}") for i in range(n)]
      # print(the_digits)
      old_value = get_value(the_digits)
      
      # move the element
      new_digits = [the_digits[i] for i in range(1, len(the_digits))]
      new_digits.append(the_digits[0])
      # print(new_digits)
      new_value = get_value(new_digits)
      solver = Solver()
      for d in the_digits:
        solver.add(d>=0, d<=9)
      solver.add(the_digits[n-1] != 0)
      solver.add(the_digits[0] != 0)
      solver.add(new_value == old_value*4)
      res = solver.check()
      if res == sat:
        print("sat: ")
        # print(solver.model())
        return res, the_digits, solver.model()
      else:
        # print("1962: unsat")
        return res, None, None
    
    found_smallest = False
    for n in range(2, 20):
      res, digits, model = num(n)
      if res == sat:
        digits.reverse()
        if not found_smallest:
          print("the smallest: ")
          found_smallest = True
        for d in digits:
          print(model[d], end="")
        print("")
        # break
        

"""
1981, p3.
m, n 都属于{1, 2, ..., 1981}，且满足(m^2-mn-n^2)^2 = 1,
求m^2+n^2的最大值。
"""
def imo_1981():
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

"""
1988, p6.
设正整数a, b满足ab+1可以整除a^2+b^2, 
证明 (a^2+b^2)/(ab+1) 是某个整数的平方.
"""
def imo_1988():
    a, b = Ints('a b')
    k = Int('k')
    t = Int('t')
    solver = Solver()
    solver.add(a>=1, b>=1)
    solver.add(k>=1)
    solver.add(t>=1)
    solver.add(a*a+b*b==(a*b+1)*k)
    solver.add(ForAll([t], k != t*t))
    res = solver.check()
    if res == sat:
        print(solver.model())
    else:
        print('1988: unsat')




"""
$ python3 imo.py <year>
"""
if __name__ == '__main__':
    year = int(sys.argv[1])
    match year:
      case 1959: imo_1959()
      case 1960: imo_1960()
      case 1962: imo_1962()
      case 1981: imo_1981()
      case 1988: imo_1988()
      case _: print("illegal year")









