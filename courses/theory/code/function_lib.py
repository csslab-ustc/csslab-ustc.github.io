from dataclasses import dataclass
from typing import Mapping, Optional, Callable

DEBUG = False

# our first implementation leverages a map
@dataclass
class FunctionWithMap[X, Y]:
    theMap: Mapping[X, Y]  # the tuples

    def get(self, key: X) -> Optional[Y]:
        if key in self.theMap:
            return self.theMap[key]
        return None

    def put(self, key: X, value: Y):
        self.theMap[key] = value


# our second implementation leverages a lambda
@dataclass
class FunctionWithLambda[X, Y]:
    theLambda: Callable[[X], Y] = lambda _: None # the lambda

    def get(self, key: X) -> Optional[Y]:
        return self.lam(key)

    def put(self, key: X, value: Y):
        oldTheLambda = self.theLambda
        self.theLambda = lambda k: value if k==key else oldTheLambda(key)



if __name__ == "__main__":
    fun1 = FunctionWithMap[int, int](
        theMap={}
    )
    fun1.put(1, 2)
    fun1.put(2, 3)
    fun1.put(3, 4)
    fun1.put(3, 88)
    for x in range(0, 4):
        print(f"f({x}) = {fun1.get(x)}")

    fun2 = FunctionWithLambda()
    fun1.put(1, 2)
    fun1.put(2, 3)
    fun1.put(3, 4)
    fun1.put(3, 99)
    for x in range(0, 4):
        print(f"f({x}) = {fun1.get(x)}")













