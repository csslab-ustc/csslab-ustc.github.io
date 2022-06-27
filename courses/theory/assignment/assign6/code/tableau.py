import unittest

import pandas as pd
from pandas.testing import assert_frame_equal

from constraint import *


class Tableau:
    def __init__(self, constraints):
        assert constraints, "constraints should not empty"

        col_size = len(constraints[0].coefficients)
        row_size = len(constraints)
        self.col_names = [f"x{i}" for i in range(col_size)]
        self.row_names = [f"s{i}" for i in range(row_size)]

        self.data = pd.DataFrame(data=[con.coefficients for con in constraints],
                                 columns=self.col_names, index=self.row_names, dtype="float64")

        self.values = pd.Series(data=[con.value for con in constraints], index=self.row_names, dtype="float64")

    def __str__(self):
        return repr(self.data)

    def pivot(self, row, col):
        # Challenge : finish the pivot function of Tableau
        #
        # the pivot function will changes the tableau's data like:
        #
        #          x0   x1                                           s0   x1
        #     s0  1.0  1.0            pivot s0 and x0           x0  1.0 -1.0
        #     s1  2.0 -1.0  --------------------------------->  s1  2.0 -3.0
        #     s2 -1.0  2.0    s0 = x0+x1;  --> x0 = s0-x1;      s2 -1.0  3.0
        #                     s1 = 2x0-x1 = 2(s0-x1)-x1 = 2s0 – 3x1
        #                     s2 = -x0+2x1 = -(s0-x1)+2x1 = -s0+3x1
        #
        # check the lecture's slides to understand how this happened.
        # Your code here:

        # swap row and column's name
        self.data.rename(columns={col: row}, index={row: col}, inplace=True)


class TestTableau(unittest.TestCase):

    def test_pivot_1(self):
        tab = Tableau([Constraint([1, 1], 2), Constraint([2, -1], 0), Constraint([-1, 2], 1)])
        tab.pivot("s0", "x0")
        assert_frame_equal(tab.data, pd.DataFrame(data=[[1.0, -1.0], [2.0, -3.0], [-1.0, 3.0]],
                                                  index=["x0", "s1", "s2"], columns=["s0", "x1"]))
        tab.pivot("s2", "x1")
        assert_frame_equal(tab.data, pd.DataFrame(data=[[2.0 / 3.0, -1.0 / 3.0], [1.0, -1.0], [1.0 / 3.0, 1.0 / 3.0]],
                                                  index=["x0", "s1", "x1"], columns=["s0", "s2"]))

    def test_pivot_2(self):
        case = [Constraint([-1, 1, 0], 0), Constraint([-1, 0, 1], 0), Constraint([1, -1, -2], 0),
                Constraint([0, 0, 1], 1)]
        tab = Tableau(case)
        tab.pivot("s3", "x2")
        assert_frame_equal(tab.data, pd.DataFrame(data=[[-1, 1, 0], [-1, 0, 1], [1, -1, -2], [0, 0, 1]],
                                                  index=["s0", "s1", "s2", "x2"], columns=["x0", "x1", "s3"],
                                                  dtype="float64"))
        tab.pivot("s2", "x0")
        assert_frame_equal(tab.data, pd.DataFrame(data=[[-1, 0, -2], [-1, -1, -1], [1, 1, 2], [0, 0, 1]],
                                                  index=["s0", "s1", "x0", "x2"], columns=["s2", "x1", "s3"],
                                                  dtype="float64"))
        print(tab.data)


if __name__ == '__main__':
    unittest.main()
