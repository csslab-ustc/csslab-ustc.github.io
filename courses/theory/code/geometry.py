from typing import Callable

import matplotlib.pyplot as plt
from z3 import *


def draw(name: str,
         x_min: int,
         x_max: int,
         y_min: int,
         y_max: int,
         stride: float,
         predicate: Callable[[float, float], bool]):
    xs = []
    r = x_min
    while r <= x_max:
        xs.append(r)
        r += stride
    ys = []
    r = y_min
    while r <= y_max:
        ys.append(r)
        r += stride
    x_result = []
    y_result = []
    # x-axis and y-axis
    plt.plot(xs, [0 for x in xs], label="x-axis", linestyle="--")
    plt.plot([0 for x in ys], ys, label="y-axis", linestyle="--")
    for x in xs:
        for y in ys:
            if predicate(x, y):
                x_result.append(x)
                y_result.append(y)
    plt.scatter(x_result, y_result, label=name, s=3)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.savefig(name)
    plt.close()


def float_eq(f_1, f_2):
    if abs(f_1 - f_2) < 1e-2:
        return True
    return False


if __name__ == "__main__":
    draw("line",
         -10,
         10,
         -10,
         10,
         1e-2,
         lambda x, y: float_eq(2 * x + 3 - y, 0))
    draw("sin",
         -10,
         10,
         -2,
         2,
         1e-2,
         lambda x, y: float_eq(math.sin(x) - y, 0))
    draw("cos",
         -10,
         10,
         -2,
         2,
         1e-2,
         lambda x, y: float_eq(math.cos(x) - y, 0))
    draw("exp",
         -10,
         10,
         -10,
         10,
         1e-2,
         lambda x, y: float_eq(math.exp(x) - y, 0))
    draw("sigmoid",
         -10,
         10,
         -2,
         2,
         1e-2,
         lambda x, y: float_eq(1 / (1 + math.exp(-x)) - y, 0))
    draw("circle",
         -10,
         10,
         -10,
         10,
         1e-2,
         lambda x, y: float_eq(math.pow(x, 2) + math.pow(y, 2) - 5, 0))
    draw("ellipse",
         -10,
         10,
         -10,
         10,
         1e-2,
         lambda x, y: float_eq(math.pow(x, 2) / 4 + math.pow(y, 2) / 2 - 5, 0))
    '''
    Elliptic curves (general form):
    y^2 = x^3 + ax + b
    here we draw some elliptic curves for different combination of the
    coefficients a and b:
    '''
    for a in range(-2, 3, 1):
      for b in range(-2, 3, 1):
        draw(f"elliptic_curve_a={a}_b={b}",
          -10,
          10,
          -10,
          10,
          1e-2,
          lambda x, y: float_eq(math.pow(x, 3) + a*x + b -math.pow(y, 2), 0))
    draw(f"format",
          -10,
          10,
          -10,
          10,
          1e-3,
          lambda x, y: float_eq(math.pow(x, 3) + math.pow(y, 3) - 1, 0))

    #     # try constraint solving with Z3
    #     solver = Solver()
    #     x, y = Reals('x y')
    #     solver.add(x**3+a*x +b -y**2==0)
    #     res = solver.check()
    #     if res == sat:
    #       print(f"y^2=x^3+{a}x+{b}", solver.model())
    #     else:
    #       print("unsat")


    # we can try another way to draw figures
    # by leveraging a solver:
    # solver = Solver()
    # x, y = Reals('x y')
    # solver.add(x ** 3 + y ** 3 - 1 == 0)
    # num_of_solutions = 0
    # xs = []
    # ys = []
    # while num_of_solutions < 1000:
    #     res = solver.check()
    #     if res == sat:
    #         num_of_solutions += 1
    #         # print(f"=x^3+y^3==1", solver.model())
    #         x_value = solver.model()[x]
    #         y_value = solver.model()[y]
    #         x_str: str = x_value.as_decimal(10)
    #         x_f = float(x_str.strip('?'))
    #         xs.append(x_f)
    #         y_str: str = y_value.as_decimal(10)
    #         y_f = float(y_str.strip('?'))
    #         ys.append(y_f)
    #         solver.add(Not((x == x_value)))
    #     else:
    #         print("unsat")
    #         break
    # # print(xs)
    # # print(ys)
    # plt.scatter(xs,
    #             ys,
    #             label="sat", s=3)
    # plt.xlabel("x")
    # plt.ylabel("y")
    # plt.legend()
    # plt.savefig("sat")
    # plt.close()




