(* You can run this code online:
  https://coq.vercel.app/scratchpad.html
*)

(* To import a standard library of arithemtic *)
Require Import Arith.

(* to define a cursive function "sum" *)
Fixpoint sum(n: nat): nat :=
  match n with
  | 0 => 0
  | S(m) => n + sum(m)
  end.

(* a lemma stating a fact that is used in the following theorem *)
Lemma sum_lemma : forall n : nat,
  2 * sum (S n) = 2 * (S n) + 2 * sum n.
Proof.
  intros n.
  simpl.
  ring. (* to prove addition and multiplication facts, automatically *)
Qed.

(* a theorem and its induction proof *)
Theorem f:
  forall n: nat,
  2 * sum(n) = n*(n+1).
Proof.
induction n.
(* goal 1: the base step *)
simpl.
auto.
(* goal 2: the induction step *)
rewrite ->  sum_lemma.
rewrite -> IHn.
ring.
Qed.


