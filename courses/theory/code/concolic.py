from dataclasses import dataclass
import random
from typing import List, Tuple
import z3

# the function being tested:
def f(x, y):
    if(x == 1234):
        if(y == 4321):
            return 1/0
    return x+y


# the concolic executor

# paths
@dataclass
class PathResult:
    HasGenerated: bool
    values: List[int]

class Path:
    max_paths: int = 10
    all_paths: List[List[z3.ExprRef]] = []
    current_path: List[z3.ExprRef] = []

    def append_cond(self, e):
        self.current_path.append(e)

    def finalize(self):
        if self.current_path != []:
            self.all_paths.append(self.current_path)

    def dump(self):
        print("history paths:")
        i = 0
        for path in self.all_paths:
            print(f"\t{i}: {path}")
            i += 1
        print("current path:")
        print(f"\t{self.current_path}\n")

    def generate_fresh_symbols(self, vars)-> PathResult:
        self.max_paths -= 1
        if self.current_path == []:
            return PathResult(False, [])
        self.all_paths.append(self.current_path)
        clone_path = self.current_path.copy()
        self.current_path = []
        if clone_path == []:
            return PathResult(False, [])

        # negating the last path cond:
        new_path = [clone_path[i] if i!=len(clone_path)-1 else z3.Not(clone_path[i])
                    for i in range(len(clone_path))]
        if new_path in self.all_paths:
            return PathResult(False, [])

        # z3 solving
        solver = z3.Solver()
        solver.add(z3.And(new_path))
        res = solver.check()
        if res != z3.sat:
            return PathResult(False, [])
        model = solver.model()
        vs = [model.eval(x, True) for x in vars]
        # print(f"vs: {vs}")
        return PathResult(True, vs)

path: Path = None


@dataclass
class SymInt:
    iv: int
    sv: z3.ExprRef

    def __add__(self, intOrSymInt: int|SymInt):
        if type(intOrSymInt) is int:
            iv = self.iv + intOrSymInt
            sv = self.sv + intOrSymInt
            return SymInt(iv, sv)
        else:
            iv = self.iv + intOrSymInt.iv
            sv = self.sv + intOrSymInt.sv
            return SymInt(iv, sv)

    def __eq__(self, intOrSymInt: int|SymInt):
        if type(intOrSymInt) is int:
            b = self.iv.__eq__(intOrSymInt)
            sv = (self.sv == intOrSymInt if b else self.sv != intOrSymInt)
        else:
            b = self.iv.__eq__(intOrSymInt.iv)
            sv = (self.sv != intOrSymInt.sv if b else self.sv == intOrSymInt.sv)
        
        global path
        path.append_cond(sv)
        return b
       

if __name__ == "__main__":
    path = Path()

    random.seed()
    a = random.randint(0, 10**10)
    b = random.randint(0, 10**10)
    sym_a = z3.Int("a")
    sym_b = z3.Int("b")
    while(path.max_paths > 0):
        a = SymInt(a, sym_a)
        b = SymInt(b, sym_b)
        
        r = f(a, b)

        print(f"{a}, {b} -> {r}")

        path.dump()
        result = path.generate_fresh_symbols([sym_a, sym_b])
        if not result.HasGenerated:
            break
        a = result.values[0]
        b = result.values[1]

