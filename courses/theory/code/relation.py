from dataclasses import dataclass
from typing import Set, Tuple


DEBUG = False

@dataclass
class Relation[X]:
    elements: Set[X]  # the set of the relation
    theSet: Set[Tuple[X, X]]  # the tuples

    def isReflexive(self) -> bool:
        for element in self.elements:
            if not (element, element) in self.theSet:
                return False
        return True

    def isSymmetry(self) -> bool:
        for (x, y) in self.theSet:
            if not (y, x) in self.theSet:
                return False
        return True

    def isTransitive(self) -> bool:
        for (x, y) in self.theSet:
            for (m, n) in self.theSet:
                if y == m:
                    if not (x, n) in self.theSet:
                        return False
        return True

    # is this relation an equivalent one?
    def isEquivalence(self) -> bool:
        return (self.isReflexive()
                and self.isSymmetry()
                and self.isTransitive())

if __name__ == "__main__":
    relation1 = Relation[int](
        elements={1, 2, 3, 4},
        theSet={(1, 1),
                (1, 2),
                (1, 3)},
    )
    print(f"{relation1} is equivalence: {relation1.isEquivalence()}")

    relation2 = Relation[int](
        elements={1, 2, 3, 4},
        theSet={(1, 1),
                (2, 2),
                (3, 3),
                (4, 4)},
    )
    print(f"{relation2} is equivalence: {relation2.isEquivalence()}")

    relation3 = Relation[str](
        elements={"hello", "world"},
        theSet={("hello", "hello"),
                ("world", "world"),
                ("hello", "world"),
                ("world", "hello")},
    )
    print(f"{relation3} is equivalence: {relation3.isEquivalence()}")














