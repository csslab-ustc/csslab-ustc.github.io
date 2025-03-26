from multiprocessing.util import ForkAwareLocal

from z3 import *
from z3 import ForAll
from z3.z3util import Iff

debug: bool = True

########################################
# This is the example we discussed in the lecture.


########################################
# part I: the encoding of deduction.


"""
# We can encode and reason using predicates,
# in three steps:
# 1) declare sorts;
# 2) encode the predicates as propositions; and
# 3) kick Z3 to check the propositions.
"""

# Step 1: declare new sorts in Z3 using "DeclareSort"
# think "sort" as "structures" in C or "class" in Java
person_sort = DeclareSort('person_sort')

# represent predicates using boolean-valued functions in Z3
is_student = Function('is_student', person_sort, BoolSort())
learn_logic = Function('learn_logic', person_sort, BoolSort())

# propositions
x = Const('x', person_sort)
# 所有学生都应该学逻辑：
# \forall x. S(x) -> L(x)
P = ForAll(x, Implies(is_student(x), learn_logic(x)))
# 张三是学生，
# S(zhang_san)
zhang_san = Const('zhang_san', person_sort)
Q = is_student(zhang_san)
# 张三应该学逻辑。
R = learn_logic(zhang_san)
target_proposition = Implies(And(P, Q), R)

# let Z3 prove that this proposition is valid
prove(target_proposition)

# another (spurious) deduction:
"""
所有学生都应该学逻辑，
李四不是学生，
李四不用学逻辑。
"""
P = ForAll(x, Implies(is_student(x),
                      learn_logic(x)))
li_si = Const('li_si', person_sort)
target_proposition = Implies(And(P, Not(is_student(li_si))),
                      Not(learn_logic(li_si)))
# does Z3 accept this?
prove(target_proposition)



########################################
# part II: dependent type theory

"""
the following code models:
template <int N>
class Vector{
    int data[N];
};
int main(int argc, char *argv[]){
    Vector<10> v1;
    Vector<20> v2;
    v1 = v2;
}
"""
vector_sort = DeclareSort('vector_sort')
vector_n_template = Function('vector_n_sort', IntSort(), vector_sort)
# equals = Function('equals', vector_sort, vector_sort, BoolSort())
m, n = Const('m', IntSort()), Const('n', IntSort())
#  m = n -> vector[m] = vector[n]
rules = ForAll([m, n],
               Implies(m == n,
                       vector_n_template(m) == vector_n_template(n)))

k = Const('k', IntSort())
print("prove vectors: 0, 0")
prove(Implies(rules, vector_n_template(0) == vector_n_template(0)))
print("prove vectors: 0, 1")
prove(Implies(rules, vector_n_template(0) == vector_n_template(1)))
print("prove vectors: 0, k-k")
prove(Implies(rules, vector_n_template(0) == vector_n_template(k*k-k*k)))
print("prove vectors: 0, k*k-k*k")
prove(Implies(rules, vector_n_template(0) == vector_n_template(k*k-k*k)))
print("prove vectors: 0, k*k*k-k*k*k-1")
prove(Implies(rules, vector_n_template(0) == vector_n_template(k*k*k-k*k*k-1)))



########################################
# part III: deduction for axiomatic systems:

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

# then do automatic reasoning with the deduction rules:
print("prove even: 2")
prove(Implies(deduction_rules, is_even(2)))
print("prove even: 50")
prove(Implies(deduction_rules, is_even(50)))
# warning: may be slow...
print("prove even: 100")
prove(Implies(deduction_rules, is_even(100)))











