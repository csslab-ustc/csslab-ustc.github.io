(* 
    Finish 5 Todo in let.ml
    run `dune exec main` to check your code 
*)
open Format
exception Todo
exception TypeError of string

module Type =
struct
    type t
    = Bool
    | Var of string
    | Arrow of t * t

    let rec pp t =
        match t with
        | Bool -> printf "Bool"
        | Var x -> print_string x
        | Arrow (t1, t2) ->
            (printf "("
        ; pp t1
        ; printf "->"
        ; pp t2
        ; printf ")")

    let rec subst ((x: string), (ty1: t), (ty2: t)) =
    (* [ Var(x) |-> ty1 ]ty2 *)
        match ty2 with
        | Bool -> Bool
        | Var y ->
            if x = y 
            then ty1
            else ty2
        | Arrow (s1, s2) ->
            Arrow (subst (x, ty1, s1), subst(x, ty1, s2))


    let rec occurs (x, tyT) =
    (* Is x appears in tyT freely? *)
        match tyT with
            | Bool -> false
            | Var(s) -> (s = x)
            | Arrow (tyT1, tyT2) -> 
                (occurs (x, tyT1) || occurs (x, tyT2))
             
end (* structure Type *)


module Constraint =
struct

    type t = (Type.t * Type.t) list

    let subst x tyT constr =
    (*  Replace variables in the constraint set *)
    (* [x |-> ty] (s1, s2) *)
        List.map
            (fun (tyS1, tyS2) -> 
                (Type.subst (x, tyT, tyS1), Type.subst (x, tyT, tyS2)))
            constr

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
            1. According to constraint set, solve (C) return sigma. 
                C is a list of (S: Type.t, T: Type.t), 
                corresponding to C = {S1=T1, S2=T2, ...} in textbook. 

            2. unify(C) return a list of (X: Type.t, T: Type.t) ,
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
        in substall c'
   


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


let counter = ref 0

let freshTypeVar () =
(* Return a new type variable *)
    let n = !counter in
        let _ = counter := (n+1) in
            ("X_" ^ string_of_int n)

(* 
    [Task 2] 
        According to Fig 22.1 in Textbook, finish 2 Todo in check (env, t).

    [Tips]
        1. To finish this task, you can also refer to assignment 4: Type. 
        2. check (env, t) return the type of term T under gamma and its constraints. 
*)
let rec check ((env: string -> Type.t), t): Type.t * Constraint.t = 
    match t with   
        | True -> (Type.Bool, [])

        | False -> (Type.Bool, [])

        | Var x -> 
            (env x, [])

        | Abs (x, t) ->
            (* Task 2.1 *)
            raise Todo

        | If (t1, t2, t3) ->
            let (ty1, c1) = check (env, t1) in 
            let (ty2, c2) = check (env, t2) in
            let (ty3, c3) = check (env, t3) in
            let newc = [(ty1, Type.Bool); (ty2, ty3)] in
            let c' = List.concat [c1; c2; c3; newc] in
                (ty2, c')

        | App (t1, t2) ->
            (* Task 2.1 *)
            raise Todo

let typeCheck t: Type.t = 
    let (ty, c) = check ((fun _ -> raise (TypeError "var not found")), t) in
    let _ = printf "\nConstraints: " in
    let _ = Constraint.pp c in 
    let _ = printf "\nraw type: " in
    let _ = Type.pp ty in 
    let sigma = Constraint.solve (c) in 
    let ty = sigma ty in 
    let _ = printf "\npretty type: " in
    let _ = Type.pp ty in  
    ty

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

(* unit test *)

let unit_test () =
    let _ = printf "\n\x1B[32m ============== Lambda: unit test =============\x1B[0m\n" in
    let t = App (Abs ("x", Var "x"), True) in
    let _ = (pp t; printf "\n") in
    let _ = typeCheck t in
    ()

