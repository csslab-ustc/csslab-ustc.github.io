-- An Introdution Proposition Proof, In Lean

/-
  Part I: Lean set-up
  1. Install VScode, if you have not already done that;
  2. Install "lean 4" extension, from the "Extension" tab in VScode;
  3. Create a new file "prop.lean", and then open it in VScode, which
    will trigger the installation of the Lean toolchain.
-/


/-
  Part II: Proof with Natural Deduction
-/

variable (P Q R: Prop)

---- #1: rules for var
-- varAxiom (exact)
theorem var_axiom (x: P) : P
  := by
  exact x


---- #2: rules for →
-- →Intro (intro)
theorem to_intro:
  P → P
  := by
  intro hp
  exact hp -- var (exact)

-- →Elim (exact)
theorem to_elim:
  (P → Q) → P → Q
  := by
  intro h1
  intro h2
  exact (h1 h2)
  -- we can only use "apply"
  -- apply h1
  -- exact h2

---- #3: rules for ∧
-- ∧ Intro (constructor)
theorem and_intro:
  P -> Q -> P ∧ Q
  := by
  intros h1 h2
  constructor
  -- we have two sub-goals
  exact h1
  exact h2


-- ∧Elim (cases)
theorem and_elim:
  (P ∧ Q) → P
  := by
  intro h1
  cases h1 with
  | intro x y => exact x
  -- we can only use "let"
  -- let ⟨l, r⟩ := h1
  -- exact l


---- #4: rules for ∨
-- ∨ Intro (constructor, left, right)
theorem or_intro:
  P -> P ∨ Q
  := by
  intros h
  constructor
  exact h

-- ∨ Elim (cases)
theorem or_elim:
  (P ∨ Q) → (P→ R) → (Q → R) → R
  := by
  intro h1 h2 h3
  cases h1 with
  | inl x => apply (h2 x)
  | inr x => apply (h3 x)

---- #5: rules for ⊤
-- ⊤ Intro (constructor)
theorem true_intro:
  True
  := by
  constructor

---- #6: rules for ⊥
-- ⊥ Elim (exfalso, cases)
theorem false_elim:
  False -> P
  := by
  intro h
  exfalso
  exact h


---- #7: rules for ¬
-- ¬  Elim (unfold, exfalso)
theorem not_unfold:
  ¬ P ∧ P → Q
  := by
  intro h
  cases h with
  | intro x y =>
  unfold Not at x
  exfalso
  apply (x y)


/-
  Part III: Curry-Howard Isomorphism
-/
#print var_axiom
theorem var_axiom2 (x: P) : P
  :=
  x

#print to_intro
theorem to_intro2:
  P → P
  :=
  fun x => x

#print to_elim
theorem to_elim2:
  (P → Q) → P → Q
  :=
  fun h1 h2 => h1 h2

#print and_intro
theorem and_intro2:
  P -> Q -> P ∧ Q
  :=
  fun h1 h2 => ⟨h1, h2⟩

#print and_elim
theorem and_elim2:
  (P ∧ Q) → P
  :=
  fun x => x.left

#print or_intro
theorem or_intro2:
  P -> P ∨ Q
  :=
  fun x => Or.inl x

#print or_elim
theorem or_elim2:
  (P ∨ Q) → (P→ R) →  (Q → R) → R
  :=
  fun (h1) (h2) (h3) =>
    match h1 with
  | Or.inl l => (h2 l)
  | Or.inr r => (h3 r)

#print true_intro
theorem true_intro2:
  True
  :=
  True.intro

#print false_elim
theorem false_elim2:
  False -> P
  :=
  fun x => False.elim x

#print not_unfold
theorem not_unfold2:
  ¬ P ∧ P → Q
  :=
  fun x =>
  match x with
  | And.intro y z =>
    nomatch y z

/-
  Part IV: Proof Automation
-/
-- Most proofs can be carried out with the "tauto" tactic,
-- which stands for "tautology".
-- For example:

theorem or_elim3:
  (P ∨ Q) → (P→ R) →  (Q → R) → R
  := by
  grind

-- we leave the proof of other propositions as exercises.


/-
  Part V: Predicate Logic
-/
---- #1: rules for ∀
-- ∀ Intro (intro)
theorem forall_intro{A: α → Prop} (ha: ∀ a, A a):
  ∀(x: α), (A x)
  := by
  intro x
  apply ha

-- ∀ Elim (apply)
theorem forall_elim{A: α → Prop} (ha: ∀ x, A x):
  A a
  := by
  apply ha

---- #2: rules for ∃
-- ∃ Intro (constructor)
theorem exists_intro_{A: α → Prop} (ha: A a):
  ∃(x: α), (A x)
  := by
  constructor
  exact ha

-- ∃ Elim (apply)
theorem exists_elim_ {A: α → Prop}
  (h1: (∃(x: α), A x))
  (h2: (∀(y: α), A y → R)):
  R
  := by
  let ⟨ x, h ⟩ := h1
  apply h2 x h
