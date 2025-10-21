import functools
import threading
import time
from typing import Callable
from ctypes import *
import matplotlib.pyplot as plt
from z3 import *

### it seems that cupy does not support the lastest Python (i.e., 3.15)
### so that we have to write it from scratch
# from cupy import cp

# so_file = "/tmp/gpu.so"
# c_functions = CDLL(so_file)
# inc_ptr = c_functions.ptr

the_target = "cpu"
indent = []

def trace(func: Callable) -> Callable:
    @functools.wraps(func)
    def traced(*args):
        global indent
        for x in indent:
            print("\t", end="")
        indent.append(0)
        print(f"{args[0]} starting:")
        start = time.time()
        func(*args)
        end = time.time()
        indent.pop(0)
        for x in indent:
            print("\t", end="")
        print(f"{args[0]} finished in: {end - start} seconds")
        return

    return traced


def judge(name: str, xs, ys, predicate):
    xs_result = []
    ys_result = []
    # on single-core CPUs
    if the_target == "cpu":
        for x in xs:
            for y in ys:
                if predicate(x, y):
                    xs_result.append(x)
                    ys_result.append(y)
    # on multi-core CPUs
    elif the_target == "threaded":
        all_threads = []
        for x in xs:
            class DrawThread(threading.Thread):
                def __init__(self, _x):
                    super().__init__()
                    self.x = _x
                    self.xs = []
                    self.ys = []

                def run(self):
                    for y in ys:
                        if predicate(self.x, y):
                            self.xs.append(x)
                            self.ys.append(y)

            thread = DrawThread(x)
            all_threads.append(thread)
            thread.start()
        for t in all_threads:
            t.join()
            for x in t.xs:
                xs_result.append(x)
            for x in t.ys:
                ys_result.append(x)
    # on GPUs
    elif the_target == "gpu":
        xs_size = len(xs)
        ys_size = len(ys)
        xs_argtype = c_float * xs_size
        ys_argtype = c_float * ys_size
        inc_ptr.argtypes = (c_char_p, c_int, c_int, xs_argtype, ys_argtype, c_float,)
        restype = POINTER(c_int)
        inc_ptr.restype = restype
        ret = inc_ptr(bytes(name, "utf-8"), xs_size, ys_size, xs_argtype(*xs), ys_argtype(*ys), 1e-2)
        for i in range(0, xs_size):
            for j in range(0, ys_size):
                if ret[i * ys_size + j] == 1:
                    xs_result.append(xs[i])
                    ys_result.append(ys[j])
    else:
        print("unsupported arch")
    return xs_result, ys_result


@trace
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
    # x-axis and y-axis
    plt.plot(xs, [0 for x in xs], label="x-axis", linestyle="--")
    plt.plot([0 for x in ys], ys, label="y-axis", linestyle="--")
    xs_result, ys_result = judge(name, xs, ys, predicate)
    plt.scatter(xs_result, ys_result, label=name, s=3)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.savefig(name + "_" + the_target)
    plt.close()


def float_eq(f_1, f_2):
    if abs(f_1 - f_2) < 1e-2:
        return True
    return False


@trace
def draw_all(name: str):
    draw("line",
         -10,
         10,
         -10,
         10,
         1e-2,
         lambda x, y: float_eq(2 * x + 3 - y, 0))
    draw("line",
         -10,
         10,
         -10,
         10,
         1e-2,
         lambda x, y: float_eq(2 * x + 3 - y, 0))
    ### some conic sections
    # 圆
    draw("circle",
         -10,
         10,
         -10,
         10,
         1e-2,
         lambda x, y: float_eq(math.pow(x, 2) + math.pow(y, 2) - 5, 0))
    # 椭圆
    draw("ellipse",
         -10,
         10,
         -10,
         10,
         1e-2,
         lambda x, y: float_eq(math.pow(x, 2) / 4 + math.pow(y, 2) / 2 - 5, 0))
    # 抛物线
    draw("parabola",
         -10,
         10,
         -10,
         10,
         1e-2,
         lambda x, y: float_eq(x * 4 - math.pow(y, 2), 0))
    # 双曲线
    draw("hyperbola",
         -10,
         10,
         -10,
         10,
         1e-2,
         lambda x, y: float_eq(math.pow(x, 2) / 4 - math.pow(y, 2) / 2 - 1, 0))

    '''
    # 椭圆曲线
    Elliptic curves (general form):
    y^2 = x^3 + ax + b
    here we draw some elliptic curves for different combination of the
    coefficients a and b:
    '''
    for a in range(-2, 3, 1):
        for b in range(-2, 3, 1):
            draw(f"elliptic_curve_y^2=x^3+{a}x+{b}",
                 -10,
                 10,
                 -10,
                 10,
                 1e-2,
                 lambda x, y: float_eq(
                     math.pow(x, 3) + a * x + b - math.pow(y, 2), 0))
    '''
    费马曲线
    General form:
    x^n + y^n = 1
    where x, y \\in \\mathbb{Q}.
    '''
    for a in range(2, 10):
        draw(f"format_x^{a}+y^{a}=1",
             -10,
             10,
             -10,
             10,
             1e-2,
             lambda x, y: float_eq(math.pow(x, a) + math.pow(y, a) - 1,
                                   0))


if __name__ == "__main__":
    draw_all("all")

    # try constraint solving with Z3
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
