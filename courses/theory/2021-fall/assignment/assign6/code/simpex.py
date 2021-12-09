import unittest
from enum import Enum, auto

import pandas as pd
from pandas.testing import assert_series_equal

from constraint import Constraint, IllegalConstraintError
from tableau import Tableau

VERBOSE = True


class Status(Enum):
    UNSAT = auto()
    SAT = auto()
    UNDECIDED = auto()


def simplex(constraints):
    result = {}
    print("===>Solving Constraints:")
    if not constraints:
        return result

    basic_var_amount = len(constraints[0].coefficients)
    for constraint in constraints:
        if len(constraint.coefficients) != basic_var_amount:
            raise IllegalConstraintError(constraint)
        print(constraint)

    tab = Tableau(constraints)

    # Challenge : finish the simplex algorithm following the skeleton of the algorithm:
    # simplex(){
    #     tab = constructTableau();
    #     while(True){
    #         for(each additional var si){
    #             if(si violates its constraint){
    #                 if(there is a suitable xj){
    #                     pivot(si, xj);
    #                     update additional var
    #                 }
    #                 else return UNSAT;
    #             }
    #         }
    #         if (each additional var satisfies its constraint)
    #             return SAT;
    #     }
    # }
    # Your code here



class TestSimplex(unittest.TestCase):

    def test_simplex_sat(self):
        case = [Constraint([1, 1], 2), Constraint([2, -1], 0), Constraint([-1, 2], 1)]
        result = simplex(case)
        assert_series_equal(pd.Series(result), pd.Series({"x0": 1.0, "x1": 1.0}))

    def test_simplex_unsat(self):
        case = [Constraint([-1, 1, 0], 0), Constraint([-1, 0, 1], 0), Constraint([1, -1, -2], 0),
                Constraint([0, 0, 1], 1)]
        result = simplex(case)
        self.assertEqual(result, "no solution")


if __name__ == '__main__':
    unittest.main()


