-- addition
def add x y := Int.add x y

theorem add_comm(x y: Int):
    add x y = add y x
    := by
    unfold add
    grind

theorem add_left_zero:
    add 0 x = x
    := by unfold add; grind

theorem add_right_zero:
    add x 0 = x
    := by unfold add; grind

theorem add_x_minus_x:
    add x (-x) = 0
    := by unfold add; grind

-- list reverse
def rev(l: List Int) := l.reverse

theorem rev_prop_inverse:
    rev (rev (l)) = l
    := by
    unfold rev
    grind

def is_order (l: List Int) (l': List Int) (n: Nat) :=
    ∀ (i: Nat), (i<n) → (l[i]? = l'[n-1-i]?)

theorem rev_prop_in_order:
    is_order l (rev l) l.length
    := by
    unfold is_order
    unfold rev
    intro i h
    rw [List.getElem?_reverse]
    grind
    grind

-- list sort
-- specifically, we use merge sort
def leInt (a: Int) (b: Int) := decide (a<=b)

def sort(l: List Int) := l.mergeSort leInt

def is_sorted (l: List Int) :=
    List.Pairwise (fun a b => (decide (a ≤ b))) l

theorem sort_prop_idempotent:
    sort (sort l) = sort (l)
    := by
    unfold sort
    apply List.mergeSort_of_pairwise
    exact List.pairwise_mergeSort
        (le := leInt)
        (by
            intro a b c hab hbc
            simp only [leInt, decide_eq_true_eq]
                at hab hbc ⊢
            omega)
        (by
            intro a b
            simp [leInt, decide_eq_true_eq]
            omega)
        l

theorem sort_prop_is_sorted:
    is_sorted (sort l)
    := by
    unfold is_sorted sort
    apply List.pairwise_mergeSort
    intro a b c hab hbc
    simp only [decide_eq_true_eq] at hab hbc ⊢
    omega
    intro a b
    grind


-- nested function that requires dedicated inputs
def nest_add (x: Int) (y: Int) :=
    if x=12345
    then if y=67890
         then 0
         else x+y
    else x+y

theorem t_is_always_1:
    nest_add x y = x+y
    := by
    unfold nest_add
    simp
    intros h1 h2
    subst x y
    simp
    sorry
