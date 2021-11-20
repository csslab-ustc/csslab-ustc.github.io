import unittest

from z3 import *

from counter import counter


class Todo(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

    def __repr__(self):
        return self.__str__()


##################################
# The abstract syntax for the Tac (three address code) language:
"""
S ::= x=y | x=y+z | x=y-z | x=y*z | x=y/z
F ::= f(x1, ..., xn){S;* return x;}
"""


# statement
class Stmt:
    def __repr__(self):
        return self.__str__()


class StmtAssignVar(Stmt):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        raise Todo("Exercise 6: finish the __str__ method in data structure StmtAssignVar")


class StmtAssignAdd(Stmt):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        raise Todo("Exercise 6: finish the __str__ method in data structure StmtAssignAdd")


class StmtAssignSub(Stmt):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        raise Todo("Exercise 6: finish the __str__ method in data structure StmtAssignSub")


class StmtAssignMul(Stmt):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        raise Todo("Exercise 6: finish the __str__ method in data structure StmtAssignMul")


class StmtAssignDiv(Stmt):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        raise Todo("Exercise 6: finish the __str__ method in data structure StmtAssignDiv")


# function:
class Function:
    def __init__(self, name, args, stmts, ret):
        self.name = name
        self.args = args
        self.stmts = stmts
        self.ret = ret

    def __str__(self):
        raise Todo("Exercise 6: finish the __str__ method in data structure Function")


###############################################
# SSA conversion:

# take a function 'f', convert it to SSA
def to_ssa_func(func: Function) -> Function:
    raise Todo("Exercise 7: do SSA conversion on tac function ")

    def to_ssa_stmt(stmt):
        raise Todo("Exercise 7: do SSA conversion on tac statements ")


###############################################
# Generate Z3 constraints:
def gen_cons_stmt(stmt):
    raise Todo("Exercise 8: generate constraints form TAC statements ")


def gen_cons_func(func):
    raise Todo("Exercise 8: generate constraints form TAC function ")


###############################################
# Tests

test_case = Function('f',
                     ['s1', 's2', 't1', 't2'],
                     [StmtAssignAdd('a', 's1', 't1'),
                      StmtAssignAdd('b', 's2', 't2'),
                      StmtAssignMul('c', 'a', 'b'),
                      StmtAssignMul('b', 'c', 's1'),
                      StmtAssignVar('z', 'b')],
                     'z')


class TestTac(unittest.TestCase):
    ssa = to_ssa_func(test_case)
    cons = gen_cons_func(ssa)

    def test_print(self):
        res = ("f(s1,s2,t1,t2){\n\ta = s1 + t1;\n\tb = s2 + t2;\n\tc = a * b;\n\t"
               "b = c * s1;\n\tz = b;\n\treturn z;\n}\n")

        # f(s1, s2, t1, t2){
        #   a = s1 + t1;
        #   b = s2 + t2;
        #   c = a * b;
        #   b = c * s1;
        #   z = b;
        #   return z;
        # }
        print(test_case)
        self.assertEqual(str(test_case), res)

    def test_to_ssa(self):
        res = ("f(s1,s2,t1,t2){\n\t_tac_f_0 = s1 + t1;\n\t_tac_f_1 = s2 + t2;\n\t_tac_f_2 = _tac_f_0 * _tac_f_1;\n\t"
               "_tac_f_3 = _tac_f_2 * s1;\n\t_tac_f_4 = _tac_f_3;\n\treturn _tac_f_4;\n}\n")

        # f(s1, s2, t1, t2){
        #   _tac_f_0 = s1 + t1;
        #   _tac_f_1 = s2 + t2;
        #   _tac_f_2 = _tac_f_0 * _tac_f_1;
        #   _tac_f_3 = _tac_f_2 * s1;
        #   _tac_f_4 = _tac_f_3;
        #   return _tac_f_4;
        # }

        print(self.ssa)
        self.assertEqual(str(self.ssa), res)

    def test_gen_cons(self):
        res = ("[_tac_f_0 == f_add(s1, t1),"
               " _tac_f_1 == f_add(s2, t2),"
               " _tac_f_2 == f_mul(_tac_f_0, _tac_f_1),"
               " _tac_f_3 == f_mul(_tac_f_2, s1),"
               " _tac_f_4 == _tac_f_3]")
        print(self.cons)
        self.assertEqual(str(self.cons), res)


if __name__ == '__main__':
    unittest.main()
