(* 
    Finish 6 Todo in let.ml
    run `dune exec main` to check your code 
*)

open Format
exception Todo
exception TypeError of string

module Type =
struct
    type t
         (* T *)
        = Bool
        | Var of string
        | Arrow of t * t
        | Pair of t * t
   
    type scheme
        (* ∀ X1...Xn. T *)
        = Forall of string list * t

    let rec exists (x, l) =
        match l with
        | [] -> false
        | y::ys ->
            if x = y
            then true
            else exists (x, ys)

    let fvs (t) =
    (* FV(t) *)
        let rec doit (t, l) =
                (match t with
                | Bool -> l
                | Var x ->
                    if exists (x, l)
                    then l
                    else x::l
                | Arrow (t1, t2) ->
                    doit (t2, doit (t1, l))
                | Pair (t1, t2) ->
                    doit (t2, doit (t1, l)))
        in  doit (t, [])

    let rec subtract set1 set2 =
    (* set1 - set2 *)
        match set1 with
            | [] -> []
            | y::ys ->
                if exists(y, set2)
                then subtract ys set2
                else y::(subtract ys set2)

    let generalize (t, bind_in_gamma): scheme =
    (* T  --->  ∀ X1...Xn. T *)
        let vars = fvs t in
        let var' = (subtract vars bind_in_gamma) in (* FV(t1) - FV(gamma) *)
        Forall (var', t)

    let rec pp t =
        match t with
        | Bool -> printf "Bool"
        | Var x -> print_string x
        | Arrow (t1, t2) ->
            (printf "("
        ; pp t1
        ; printf " -> "
        ; pp t2
        ; printf ")")
        | Pair (t1, t2) ->
            (printf "("
        ; pp t1
        ; printf " * "
        ; pp t2
        ; printf ")")

    let rec occurs (x, t) =
        match t with
        | Bool -> false
        | Var y -> 
            if x = y 
            then true 
            else false
        | Arrow (t1, t2) ->
            (occurs (x, t1) || occurs (x, t2))
        | Pair (t1, t2) ->
            (occurs (x, t1) || occurs (x, t2))

    let rec subst (x, t1, t2) =
    (*  Replace type variables *)
    (* [x |-> t1] t2 *)
        match t2 with
        | Bool -> Bool
        | Var y ->
            if x = y 
            then t1
            else t2
        | Arrow (s1, s2) ->
            Arrow (subst (x, t1, s1), subst(x, t1, s2))
        | Pair (s1, s2) ->
            Pair (subst (x, t1, s1), subst (x, t1, s2))

end (* structure Type *)

module Constraint =
struct

type t = (Type.t * Type.t) list

    let subst (x, ty, constr) =
    (*  Replace variables in the constraint set *)
    (* [x |-> ty] (s1, s2) *)
        List.map (fun (s1, s2) -> (Type.subst(x, ty, s1), Type.subst (x, ty, s2))) constr

    let substall constr ty =
    (* sigma = [X |-> Bool, Y |-> Z, ...] *)
            List.fold_left
                (fun tyS (x, ty2) -> Type.subst (x, ty2, tyS))
                ty
                (List.rev constr)

    (*  
        [Task 1] 
            According to Fig 22.2 in Textbook, finish 3 Todo in solve (C)

        [Tips]
        
            According to constraint set, solve (C) return sigma. 
            C is a list of (S: Type.t, T: Type.t), 
            corresponding to C = {S1=T1, S2=T2, ...} in textbook. 

            unify(C) return a list of (X: Type.t, T: Type.t) ,
            corresponding to sigma = [X |-> Bool, Y |-> Z, ...] in textbook 
    *)
    let solve (c) = 
        let rec unify c = 
            match c with
                | [] -> []
                | (Type.Bool, Type.Bool) :: rest -> 
                    unify rest

                | (Type.Var(x), tyt) :: rest -> 
                    (* Task 1.1 *)
                    raise Todo

                | (tys, Type.Var(x)) :: rest -> 
                    (* Task 1.2 *)
                    raise Todo
                
                | (Type.Arrow(s1, s2), Type.Arrow(t1, t2)) :: rest ->
                    (* Task 1.3 *)
                    raise Todo

                | (_, _) :: _ ->
                    raise (TypeError "Unsolvable constraints")

        in 
        let c' = unify c 
        in substall c'  (* sigma *)

    let pp t = List.iter (fun (x, y) -> 
                                (Type.pp x
                                ; printf " = "
                                ; Type.pp y
                                ; printf "; "))
                            t

end (* strucure Constraint *)

type t
  = True
  | False
  | If of t * t * t
  | Var of string
  | Abs of string * t
  | App of t * t
  | Let of string * t * t
  | Pair of t * t


let counter = ref 0

let freshTypeVar () =
(* Return a new type variable *)
    let n = !counter in
        let _ = counter := (n+1) in
            ("X_" ^ string_of_int n)

let instantiate (Type.Forall (vars, t)) =
    (* ∀ X1...Xn.T  --->  [Xi |-> Yi]T *)
    let rec doit (vars, t) =
        match vars with
            | [] -> t
            | x :: xs ->
                let fresh = freshTypeVar()
                in  doit (xs, Type.subst (x, (Type.Var fresh), t))
    in  doit (vars, t)

type opt
(* Two forms of type in gamma *)
  = Left of Type.t          (* T *)
  | Right of Type.scheme    (* ∀ X1...Xn. T *)

let subst_gamma sigma gamma =
(* 
    Make the same substitution (sigma) for the type variable in the gamma 

    for instance, [Y |-> Z]
    T   --->  [Y |-> Z]T
    ∀ X1...Xn. T  --->  ∀ X1...Xn. [Xi |-> Yi]T
 *)
    let doit (x, optt) =
        match optt with
        | Left ty ->
            (x, Left (sigma ty))
        | Right (Type.Forall (vars, ty)) ->
            (x, Right (Type.Forall (vars, sigma ty)))
    in List.map doit gamma 

let rec find_bind gamma =
(* Return a list of bound variables in gamma *)
    match gamma with
    | [] -> []
    | pair :: rs -> 
        match pair with 
        | (_, Left (Var x)) -> x :: (find_bind rs)
        | (_, _) -> (find_bind rs)

let rec find_in_gamma ((x: string), (gamma: (string * opt) list)) = 
(* Return the type of x in context *)
    match gamma with
        | [] -> raise (TypeError "var not found")
        | (y, tyx)::sl ->
            if x = y
            then tyx
            else find_in_gamma (x, sl)

(* 
    [Task 2] 
        According to Fig 22.1 and p333-p334 in Textbook, finish 3 Todo in check (env, t)

    [Tips]
        check (env, t) return the type of term T under gamma and its constraints 
*)            
let check t : Type.t * Constraint.t = 
    let rec doit t gamma =
    (*  gamma is a list of (x: string, T: opt) ,
        corresponding to Γ = {Y: T1, Z: ∀X1...Xn.T2, ...} in textbook *)
        (match t with 
            | True -> (Type.Bool, [])
            | False -> (Type.Bool, []) 
            | Var x -> 
                let find = find_in_gamma(x, gamma) in 
                let ret = match find with
                    | Left ty -> ty
                    | Right forall -> instantiate forall
                in 
                (ret, [])

            | Let (x, t1, t2)->
                (* Task 2.1 *)
                raise Todo

            | Pair (t1, t2)->
                let (ty1, c1) = doit t1 gamma in
                let (ty2, c2) = doit t2 gamma in
                let c' = List.concat [c1; c2] in
                    ((Type.Pair (ty1, ty2)), c')

            | Abs (x, t) ->
                (* Task 2.2 *)
                raise Todo

            | If (t1, t2, t3) ->
                let (ty1, c1) = doit t1 gamma in 
                let (ty2, c2) = doit t2 gamma in
                let (ty3, c3) = doit t3 gamma in
                let newc = [(ty1, Type.Bool); (ty2, ty3)] in
                let c' = List.concat [c1; c2; c3; newc] in
                    (ty2, c')

            | App (t1, t2) ->
                (* Task 2.3 *)
                raise Todo
                    
            )
        in doit t []


let rec pp t =
    match t with
      | True -> printf "true"
      | False -> printf "false"
      | If (e1, e2, e3) ->
        (printf "if "
       ; pp e1
       ; printf " then "
       ; pp e2
       ; printf " else "
       ; pp e3)
      | Var x -> print_string x
      | Abs (x, t) ->
        (printf "λ "
       ; print_string x
       ; printf "."
       ; pp t)
      | App (t1, t2) ->
        (printf "("
       ; pp t1
       ; printf ") ("
       ; pp t2
       ; printf ")")
      | Let (x, t1, t2) ->
        (printf "let "
       ; print_string x
       ; printf " = "
       ; pp t1
       ; printf " in "
       ; pp t2
       )
      | Pair (t1, t2) ->
        (printf "("
       ; pp t1
       ; printf ", "
       ; pp t2
       ; printf ")")

let typeCheck t = 
    let (ty, c) = check (t) in
    let _ = printf "\nthe term: " in
    let _ = pp t in
    let _ = printf "\nConstraints: " in
    let _ = Constraint.pp c in
    let _ = printf "\nraw type: " in
    let _ = Type.pp ty in
    let sigma = Constraint.solve (c) in
    let ty = sigma ty in
    let _ = printf "\npretty type: " in
    let _ = Type.pp ty in
    ty

(* unit test *)
let unit_test () =
let _ = printf "\n\x1B[32m =============== Let: unit test ===============\x1B[0m\n" in


let t = App (Abs ("x", Var "x")
           , True)
in
let _ = pp t; printf "\n" in
let _ = typeCheck t in
let _ = printf "\n\x1B[32m ---------------------------------------------\x1B[0m\n"  in


let t1 = Let ("f", Abs("x", Var "x"), App (Var "f", Var "f")) in
let _ = pp t1; printf "\n" in
let _ = typeCheck t1 in
let _ = printf "\n\x1B[32m ---------------------------------------------\x1B[0m\n"  in

let t2 = Let ("f0", Abs("x0", Pair (Var "x0", 
                                    Var "x0"))
            , Let ("f1", Abs ("x1", App (Var "f0", App (Var "f0", Var ("x1")))),
                   App (Var "f1", Abs ("z", Var "z"))))
in
let _ = pp t2; printf "\n" in
let _ = typeCheck t2 in 
let _ = printf "\n\x1B[32m ---------------------------------------------\x1B[0m\n"  in

let t3 = Let ("f", Abs("x", Let ("g", Abs ("y", Pair (Var "x", Var "y")), Var "g")), Var "f")
in
let _ = pp t3; printf "\n" in
let _ = typeCheck t3 in
let _ = printf "\n\x1B[32m ---------------------------------------------\x1B[0m\n"  in

let t4 = Abs("x", Abs ("y", Pair (Var "x", Var "y")))
in
let _ = pp t4; printf "\n" in
let _ = typeCheck t4 in
let _ = printf "\n\x1B[32m ---------------------------------------------\x1B[0m\n"  in

(* let t5 = Abs ("f", App (Var "f", Var "f"))
in
let _ = pp t5; printf "\n" in
let _ = typeCheck t5 in
let _ = printf "\n\x1B[32m ---------------------------------------------\x1B[0m\n"  in *)
()