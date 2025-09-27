from dataclasses import dataclass
from typing import Optional, List, Set, Any

DEBUG = False

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
                for p in ps:
                    Prop.print(p)
                    print(", ", end="")
                print("]")
                return
            case Prop.Or(ps):
                print(f"{ps}", end="")
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
        value: Prop
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
                   print(", ", end="")
                   print0(tail)
        print0(self)
        print("]", end=" ")


# take as input a proposition, calculates and return the
# set of variables in it.
def collectVars(p: Prop.T):
    theSet = set()
    def collect0(p: Prop.T, s: Set[str]):
        match p:
            case Prop.TrueLiteral(), Prop.FalseLiteral():
                return
            case Prop.Var(x):
                s.add(x)
            case Prop.And(props):
                for q in props:
                    collect0(q, s)
            case Prop.Or(props):
                for q in props:
                    collect0(q, s)
    collect0(p, theSet)
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
    raise ValueError

def dispatch(theSet: Set[str], p: Prop.T, table: Table.T):
        if len(theSet) == 0:
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
    prop1 = Prop.And([Prop.Var("x"), Prop.Var("y")])
    print(prop1)
    Prop.print(prop1)
    varSet = collectVars(prop1)
    prove(prop1)
















