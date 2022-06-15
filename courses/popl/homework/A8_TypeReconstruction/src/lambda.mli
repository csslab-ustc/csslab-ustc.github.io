module Type:
sig
  type t
    = Bool
    | Var of string
    | Arrow of t * t
end
(* We assume that the record fields are sorted.
 * And this can be easily achieved by
 * pre-sorting the record fields.
 *)
type t
  = True
  | False
  | If of t * t * t
  | Var of string
  | Abs of string * t
  | App of t * t

val pp: t -> unit
val typeCheck: t -> Type.t
val unit_test: unit -> unit
