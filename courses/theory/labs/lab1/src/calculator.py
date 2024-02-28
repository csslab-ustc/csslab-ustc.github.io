import unittest
from dataclasses import dataclass


@dataclass
class Expr:
    pass

@dataclass
class Num(Expr):
    value: [int| float]
    
    def __str__(self) -> str:
        return str(self.value)

@dataclass
class Add(Expr):
    left: Expr
    right: Expr

    def __str__(self):
        return f"{self.left} + {self.right}"

@dataclass
class Minus(Expr):
    left: Expr
    right: Expr

    def __str__(self):
        return f"{self.left} - {self.right}"

@dataclass
class Multi(Expr):
    left: Expr
    right: Expr

    def __str__(self):
        return f"{self.left} * {self.right}"

# Exercise 2: fill in the missing data structures of `Div` and `Par`. 
# You also need to implement the `__str__()` method in these classes 
# to print the necessary information. Make sure your src pass
# the unit tests 1&2.
@dataclass
class Div(Expr):
    # @begin
    left: Expr
    right: Expr

    def __str__(self):
        return f"{self.left} / {self.right}"
    # @end

@dataclass
class Par(Expr):
    # @begin
    inclusion: Expr

    def __str__(self):
        return f"({self.inclusion})"
    # @end



# Exercise 3: finish the interpreter by filling in the missing
# src in the `eval_value()` function.
# Don't forget to test your src using unit tests 3&4.
def eval_value(e: Expr) -> [int| float]:
    match e:
        case Num(value):
            return value
        case Add(left, right):
            return eval_value(left) + eval_value(right)
    # @begin
        case Minus(left, right):
            return eval_value(left) - eval_value(right)
        case Multi(left, right):
            return eval_value(left) * eval_value(right)
        case Div(left, right):
            try:
                result =  eval_value(left) / eval_value(right)
            except ZeroDivisionError:
                print(f"Find Division by zero error: {e}")
                exit(1)
            return result
        case Par(inclusion):
            return eval_value(inclusion)
    # @end

# 3 * 4 + 10 / 2
test_case_1 = Add(
    Multi(
        Num(3), Num(4)
    ), Div(
        Num(10), Num(2)
    )
)

# (12 + 217) * 3 - 621
test_case_2 = Minus(
    Multi(
        Par(
            Add(Num(12), Num(217))
        ), Num(3)
    ), Num(621)
)

class TestCalculator(unittest.TestCase):

    def test_print_1(self):
        self.assertEqual(str(test_case_1), "3 * 4 + 10 / 2")

    def test_print_2(self):
        self.assertEqual(str(test_case_2), "(12 + 217) * 3 - 621")

    def test_eval_1(self):
        self.assertEqual(eval_value(test_case_1), 17)

    def test_eval_2(self):
        self.assertEqual(eval_value(test_case_2), 66)


if __name__ == '__main__':
    unittest.main()
