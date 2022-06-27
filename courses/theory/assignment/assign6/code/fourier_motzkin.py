import unittest
from typing import List

import pandas as pd

from tableau import Tableau
from constraint import Rel, Constraint


def elim_equations(table: Tableau) -> Tableau:
    # Challenge : finish the equation elimination step for the
    # fourier_motzkin  algorithm
    #
    # Your code here
    pass


def elim_unbounded_vars(table: Tableau) -> Tableau:
    # Challenge : finish the unbounded variable elimination step for the
    # fourier_motzkin  algorithm
    #
    # Your code here
    pass

def elim_vars(table: Tableau) -> Tableau:
    # Challenge : finish the bounded variable elimination step for the
    # fourier_motzkin  algorithm
    #
    # Your code here


def solve_one_var(table: Tableau) -> float:
    # Challenge : finish the solve the last variable step for the
    # fourier_motzkin  algorithm
    #
    # Your code here
    pass


def fourier_motzkin(la_prop: List[Constraint]) -> dict:
    # Challenge : finish the fourier_motzkin  algorithm by assembling the
    # four steps above
    #
    # Your code here


if __name__ == '__main__':
    case_1 = [Constraint([1, 1], 0.8), Constraint([1, -1], 0.2)]
    case_2 = [Constraint([1, 1], 0.8), Constraint([1, 5], 0.2), Constraint([1, 3], 0, relation=Rel.EQ)]
    fourier_motzkin(case_1)
    fourier_motzkin(case_2)
