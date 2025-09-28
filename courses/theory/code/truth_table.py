from dataclasses import dataclass
from typing import Optional, List, Set, Any

DEBUG = True

'''
The definitions of propositions.
'''
@dataclass
class Prop:

    @dataclass
    class T:
        pass

    @dataclass
    class TrueLiteral(T):
        pass

    @dataclass
    class FalseLiteral(T):
        pass

    @dataclass
    class Var(T):
        x: str

    @dataclass
    class And(T):
        props: List[Any]

    @dataclass
    class Or(T):
        props: List[Any]

    @dataclass
    class Implies(T):
        antecedent: Any
        consequent: Any

    @dataclass
    class Not(T):
        theProp: Any

    def print(self: T):
        match self:
            case Prop.TrueLiteral():
                print("T", end="")
                return
            case Prop.FalseLiteral():
                print("F", end="")
                return
            case Prop.Var(x):
                print(f"{x}", end="")
                return
            case Prop.And(ps):
                print("/\\[", end="")
                for i in range(len(ps) - 1):
                    Prop.print(ps[i])
                    print(", ", end="")
                Prop.print(ps[len(ps) - 1])
                print("]")
                return
            case Prop.Or(ps):
                print("\\/[", end="")
                for i in range(len(ps)-1):
                    Prop.print(ps[i])
                    print(", ", end="")
                Prop.print(ps[len(ps)-1])
                print("]")
                return
            case Prop.Implies(a, c):
                Prop.print(a)
                print("->", end="")
                Prop.print(c)
                print("")
                return
            case Prop.Not(a):
                print("!", end="")
                Prop.print(a)
                print("")
                return
        raise ValueError


'''
a functional symbol table
'''
@dataclass
class Table:

    @dataclass
    class T:
        pass

    @dataclass
    class Empty(T):
        pass

    @dataclass
    class Cons(T):
        var: str
        value: Prop.T
        tail: Any

    def insert(self: T, x: str, p: Prop.T) -> T:
        # sanity check
        if not Table.lookup(self, x) is None:
            print("error: duplicated \n")
        return Table.Cons(x, p, self)

    def lookup(self: T, x: str) -> Optional[Prop.T]:
        match self:
            case Table.Empty():
                return None
            case Table.Cons(y, q, tail):
                if x == y:
                    return q
                return Table.lookup(tail, x)
        return None

    def print(self: T):
        print("[", end="")
        def print0(t):
            match t:
                case Table.Empty():
                   return
                case Table.Cons(y, q, tail):
                   print(f"{y} -> ", end="")
                   Prop.print(q)
                   match tail:
                        case Table.Empty():
                            pass
                        case Table.Cons():
                            print(", ", end="")
                   print0(tail)
        print0(self)
        print("]", end=" ")


# take as input a proposition, calculates and returns the
# set of variables in it.
def collectVars(p: Prop.T):
    theSet = set()
    def collect0(p: Prop.T):
        match p:
            case Prop.TrueLiteral(), Prop.FalseLiteral():
                return
            case Prop.Var(x):
                theSet.add(x)
                return
            case Prop.And(props):
                for q in props:
                    collect0(q)
                return
            case Prop.Or(props):
                for q in props:
                    collect0(q)
                return
            case Prop.Implies(a, c):
                collect0(a)
                collect0(c)
                return
            case Prop.Not(p):
                collect0(p)
                return
        raise ValueError
    collect0(p)
    return theSet


def evaluate(p: Prop.T, table: Table.T):
    match p:
        case Prop.TrueLiteral(), Prop.FalseLiteral():
            return p
        case Prop.Var(x):
            return Table.lookup(table, x)
        case Prop.And(props):
            results = [evaluate(q, table) for q in props]
            for r in results:
                match r:
                    case Prop.FalseLiteral():
                        return r
            return Prop.TrueLiteral()
        case Prop.Or(props):
            results = [evaluate(q, table) for q in props]
            for r in results:
                match r:
                    case Prop.TrueLiteral():
                        return r
            return Prop.FalseLiteral()
        case Prop.Implies(a, c):
            ra = evaluate(a, table)
            rc = evaluate(c, table)
            match ra:
                case Prop.TrueLiteral():
                    return rc
            return Prop.TrueLiteral()
        case Prop.Not(p):
            rp = evaluate(p, table)
            match rp:
                case Prop.TrueLiteral():
                    return Prop.FalseLiteral()
            return Prop.TrueLiteral()
    raise ValueError

def dispatch(theSet: Set[str], p: Prop.T, table: Table.T):
        if len(theSet) == 0:
            if DEBUG:
                Table.print(table)
            r = evaluate(p, table)
            Prop.print(r)
            print("")
            return
        var = theSet.pop()
        oldSet = theSet.copy()
        table1 = Table.insert(table, var, Prop.TrueLiteral())
        dispatch(theSet, p, table1)
        table2 = Table.insert(table, var, Prop.FalseLiteral())
        dispatch(oldSet, p, table2)

def prove(p: Prop.T):
    varSet0 = collectVars(p)
    dispatch(varSet0, p, Table.Empty())

if __name__ == "__main__":
    # x /\ y
    prop: Prop.T = Prop.And([Prop.Var("x"), Prop.Var("y")])
    Prop.print(prop)
    prove(prop)

    # x \/ y
    prop: Prop.T = Prop.Or([Prop.Var("x"), Prop.Var("y")])
    Prop.print(prop)
    prove(prop)

    # !x
    prop: Prop.T = Prop.Not(Prop.Var("x"))
    Prop.print(prop)
    prove(prop)

    # x -> x
    prop: Prop.T = Prop.Implies(Prop.Var("x"), Prop.Var("x"))
    Prop.print(prop)
    prove(prop)

    # p -> q -> p
    prop: Prop.T = Prop.Implies(Prop.Var("p"),
                                Prop.Implies(Prop.Var("q"), Prop.Var("p")))
    Prop.print(prop)
    prove(prop)

    # a large one:
    N: int = 20  # you may want to change this to an even larger one
    prop: Prop.T = Prop.And([Prop.Var(f"x_{x}") for x in range(0, 20)])
    Prop.print(prop)
    prove(prop)
















