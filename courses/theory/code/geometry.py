from typing import Callable, List

DEBUG = True

'''
我们研究线性及非线性约束的几何解释。
'''

import numpy as np
import matplotlib.pyplot as plt

'''
绘制二维图形。
我们采用暴力穷举法绘制图像，而不用解析形式，是因为一般情况下，（非线性）约束
不满足函数形式。例如，椭圆的约束
x^2    y^2
--- + ----- = 1
a^2    b^2
对同一个变量x的值，可能有两个（对称的）y值与之对应。
'''
def draw_pic_2d(from_: int,
                to_: int,
                stride: float,
                relation: Callable[[float, float], bool],
                name: str):
    if DEBUG:
        print(name)
    xs = []
    i = from_
    while i <= to_:
        xs.append(i)
        i += stride
    print(xs)
    ys = xs.copy()
    if DEBUG:
        print(xs)
        print(ys)
    result_xs: List[float] = []
    result_ys: List[float] = []
    x_axis = [0 for i in range(len(xs))]
    plt.plot(xs, x_axis, linestyle='--', label="x_axis")
    plt.plot(x_axis, xs, linestyle='--', label="y_axis")
    for x in xs:
        xq: float = (x / 4.0) ** 2
        for y in ys:
            yq: float = (y / 3.0) ** 2
            sumqq: float = xq + yq - 1.0
            # print(xq, xqq, yq, yqq, delta, delta2)
            # sys.exit(0)
            if sumqq.__abs__() <= 1e-6:
                result_xs.append(x)
                result_ys.append(y)
    if DEBUG:
        print(result_xs)
        print(result_ys)
    plt.scatter(result_xs, result_ys, label=name)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.show()
    # plt.savefig(name)
    # plt.close()

#
# def float_eq(f1: Decimal, f2: Decimal, threshold: Decimal) -> bool:
#     if Decimal.__abs__(f1-f2) <= threshold:
#         return True
#     return False


if __name__ == "__main__":
    # draw_pic_2d(-10,
    #             10,
    #             1e-2,
    #             lambda x, y: float_eq(Decimal..(x),
    #                                   y,
    #                                   1e-3),
    #             "sin")
    # draw_pic_2d(-10,
    #             10,
    #             1e-2,
    #             lambda x, y: float_eq(math.cos(x),
    #                                   y,
    #                                   1e-3),
    #             "cos")
    draw_pic_2d(-10,
                10,
                10*0.001,
                lambda x, y: True,
                "ellipse")













