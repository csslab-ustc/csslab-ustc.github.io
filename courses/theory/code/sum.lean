-- To prove properties of natural numbers using induction.

-- to define a cursive function "sum" on "Nat" type
def sum(n: Nat): Nat :=
  match n with
  | 0 => 0
  | Nat.succ n' => n + (sum n')

-- a theorem stating a property of "sum", along with its induction proof
theorem t2:
  2 * (sum n) = n*(n+1)
  := by
  induction n with
  | zero => rw[sum]
  | succ n' ih =>
  rw[sum]
  rw[Nat.left_distrib]
  rw[ih]
  grind
