from z3 import *

debug: bool = True

########################################
# This is the example we discussed in the lecture.

"""
# We can encode and reason using predicates,
# in three steps:
# 1) declare sorts;
# 2) encode the predicates as propositions; and
# 3) kick Z3 to check the propositions.
"""

# Step 1: declare new sorts in Z3 using "DeclareSort"
# think "sort" as "structures" in C or "class" in Java
StudentSort = DeclareSort('student_sort')

# represent predicates using boolean-valued functions in Z3
is_a_student = Function('is_a_student', StudentSort, BoolSort())
should_learn_formal_method = Function('should_learn_formal_method', StudentSort, BoolSort())

# propositions
x = Const('x', StudentSort)
# 所有学生都应该学形式化方法，
P = ForAll(x, Implies(is_a_student(x), should_learn_formal_method(x)))
# 张三是学生，
zhang_san = Const('zhang_san', StudentSort)
Q = is_a_student(zhang_san)
# 张三应该学形式化方法。
R = should_learn_formal_method(zhang_san)

# let Z3 prove that this proposition is valid
prove(Implies(And(P, Q), R))

# another (spurious) deduction:
"""
所有学生都应该学形式化方法，
李四不是学生，
所以李四不用学形式化方法。
"""
P = ForAll(x, Implies(is_a_student(x), should_learn_formal_method(x)))
li_si = Const('li_si', StudentSort)
target_prop = Implies(And(P, Not(is_a_student(li_si))),
                      Not(should_learn_formal_method(li_si)))
# does Z3 accept this?
prove(target_prop)


####
# deduction system

"""
------------------(r0)
   is_even 0
   
   is_even x
------------------(r1)
   is_even (x+2)
"""
x = Int('x')
is_even = Function('is_even', IntSort(), BoolSort())
# We encode the two deduction rules:
r0 = is_even(0)
r1 = ForAll([x], Implies(is_even(x), is_even(x+2)))
deduction_rules = And([r0, r1])

# and then do automatic reasoning with the deduction rules:
prove(Implies(deduction_rules, is_even(2)))
# warning: may be slow...
prove(Implies(deduction_rules, is_even(50)))
















