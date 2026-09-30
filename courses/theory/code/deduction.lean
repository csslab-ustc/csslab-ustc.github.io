-- ########################################
-- This is the example we discussed in the lecture, in Lean.


-- ########################################
-- part I: the encoding of deduction.


/-
We can encode and reason using predicates, in three steps:
   1) declare sorts;
   2) encode the predicates as propositions (boolean-valued functions); and
   3) kick Z3 to check the propositions.
-/

-- Step #1: declare new sorts in Lean using "axiom"
-- think "sort" as "structures" in C or "class" in Python/C++/Java
axiom person_sort: Type

-- Step #2: declare predicates
axiom is_student: person_sort -> Prop
axiom learn_logic: person_sort -> Prop

-- propositions
axiom x: person_sort

-- 所有学生都应该学逻辑：
-- # \forall x. S(x) -> L(x)
def P := ∀ x: person_sort, is_student x → learn_logic x

-- 张三是学生，
-- # S(zhang_san)
axiom zhang_san: person_sort

def Q := is_student zhang_san
-- # 张三应该学逻辑。
def R := learn_logic zhang_san
def target_proposition := P ∧ Q → R

-- # prove this proposition is valid in Lean
theorem t1:
  target_proposition
  := by
  intro h
  cases h with
  | intro l r =>
  apply l
  unfold Q at r
  exact r


/- another (spurious) deduction:
所有学生都应该学逻辑，
李四不是学生，
李四不用学逻辑。
--/
axiom li_si: person_sort
theorem t2:
  P ∧ ¬(is_student li_si ) → ¬(learn_logic li_si)
-- can we prove this in Lean?
  := by
  intros h1 h2
  cases h1 with
  | intro l r => unfold P at l; unfold Not at r; apply r; sorry


-- ########################################
-- part II: dependent type theory

/-
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
-/
axiom vector_sort: Type
axiom vector_n_template: Nat → vector_sort
axiom vector_equals: vector_sort -> vector_sort -> Prop
axiom m: Nat
axiom n: Nat
--  m = n -> vector[m] = vector[n]
def P_rules := forall (m: Nat) (n: Nat),
              m == n →
              vector_equals (vector_n_template m) (vector_n_template n)


axiom k: Nat
#print "prove vectors: 0, 0"
theorem v_0_0:
  P_rules → vector_equals (vector_n_template 0) (vector_n_template 0)
  := by
  intro h
  apply h
  simp

#print "prove vectors: 0, 1"
theorem v_0_1:
  P_rules → vector_equals (vector_n_template 0) (vector_n_template 1)
  := by
  intro h
  apply h
  simp
  sorry

#print "prove vectors: 0, k-k"
theorem v_k_k:
  P_rules →
  vector_equals (vector_n_template 0) (vector_n_template (k-k))
  := by
  intro h
  apply h
  simp

#print "prove vectors: 0, k*k-k*k"
theorem v_k2_k2:
  P_rules →
  vector_equals (vector_n_template 0) (vector_n_template (k*k-k*k))
  := by
  intro h
  apply h
  simp -- notice the non-linear

#print "prove vectors: 0, k*k*k-k*k*k"
theorem v_k3_k3:
  P_rules →
  vector_equals (vector_n_template (k*k+ 2*k+1)) (vector_n_template ((k+1)*(k+1)))
  := by
  intro h
  apply h
  grind -- non-trival non-linear


--########################################
--# part III: deduction with axiomatic systems:

/-
------------------(r_0)
   is_even 0


   is_even x
------------------(r_ss)
   is_even (x+2)
-/
--# We encode the two deduction rules:
inductive is_even: Nat-> Prop where
  | r_0: is_even 0
  | r_ss: ∀ x: Nat, is_even x → is_even (x+2)


-- then we can reason with these deduction rules:
#print "prove even: 0"
theorem even_0:
  is_even 0
  := by
  exact is_even.r_0

#print "prove even: 2"
theorem even_2:
  is_even 2
  := by
  apply is_even.r_ss
  exact is_even.r_0

#print "prove even: 50"
theorem even_50:
  is_even 50
  := by
  repeat apply is_even.r_ss
  exact is_even.r_0

--# warning: may be slow...
#print "prove even: 100000"
theorem even_100000:
  is_even 100000
  := by
  repeat apply is_even.r_ss
  exact is_even.r_0
