from enum import Enum


class Rel(Enum):
    EQ = "="
    LT = "<"
    LE = "<="


class IllegalConstraintError(Exception):
    def __init__(self, constraint):
        self.constraint = constraint

    def __str__(self):
        return f"Illegal constraint: {self.constraint}"


class Constraint:
    def __init__(self, coefficients, value, relation=Rel.LE):
        self.coefficients = coefficients
        self.value = value
        self.relation = relation

    def __str__(self):
        coefficients_str = ""
        for idx, value in enumerate(self.coefficients):
            if idx == 0:
                coefficients_str += f"{value}*x{idx}"
            elif value > 0:
                coefficients_str += f" + {value}*x{idx}"
            elif value < 0:
                coefficients_str += f" - {abs(value)}*x{idx}"

        return f"{coefficients_str} {self.relation.value} {self.value}"


if __name__ == '__main__':
    la_prop = [Constraint([1, 1], 2), Constraint([2, -1], 0), Constraint([-1, 2], 1)]
    for constraint in la_prop:
        print(constraint)
