from z3 import *


class Todo(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

    def __repr__(self):
        return self.__str__()


def four_queen():
    solver = Solver()
    # the basic data structure:
    N = 4
    board = [[Bool('b_{}_{}'.format(i, j)) for i in range(N)]
             for j in range(N)]

    # constraint 1: each row has just one queen:
    rows = []
    for i in range(N):
        current_row = []
        for j in range(N):
            current_row.append(board[i][j])
            for k in range(N):
                if k != j:
                    current_row.append(Not(board[i][k]))
        rows.append(current_row)

    # constraint 2: each column has just one queen:
    raise Todo("Challenge: add constraints which describe each column has just one queen")

    # constraint 3: each diagonal has at most one queen:
    raise Todo("Challenge: add constraints which describe each diagonal has at most one queen")

    # constraint 4: each anti-diagonal has at most one queen:
    raise Todo("Challenge: add constraints which describe each anti-diagonal has at most one queen")



if __name__ == '__main__':
    # Four Queen should have 2 set of solutions
    four_queen()

