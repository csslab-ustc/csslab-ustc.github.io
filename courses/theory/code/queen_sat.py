"""
N-queens problem.

The N-queens problem try to place N chess queens
on an N*N chessboard so that no two queens attack each other.
A solution requires that no two queens share the
same row, column, diagonal, or anti-diagonal.

In this code, we solve the N-queens problem via the SAT approach.
"""

import time
from typing import List

from z3 import *

debug: bool = False

# the board to place queens
board: List[List[BoolRef]] = []
board_cons: List[List[BoolRef]] = []

def init_board(the_board_size: int):
    global board
    global board_cons
    board = [[Bool(f"x_{i}_{j}") for j in range(the_board_size)] for i in range(the_board_size)]
    if debug:
        print(board)
    board_cons = [[If(board[i][j], 1, 0) for j in range(the_board_size)]
                  for i in range(the_board_size)]
    if debug:
        print(board_cons)

def generate_constraints(the_board_size: int) -> BoolRef:
    global board
    global board_cons
    constraints = []
    # 1: each row has just 1 queen:
    for row in range(the_board_size):
        constraints.append(sum(board_cons[row]) == 1)
    if debug:
        print(constraints)
    # 2: each column has just 1 queen:
    for row_index in range(the_board_size):
        col = [row[row_index] for row in board_cons]
        constraints.append(sum(col) == 1)
    # 3: each diagonal has at most 1 queen
    for intercept in range(1 - the_board_size, the_board_size, 1):
        diag = [board_cons[i][intercept + i] for i in range(the_board_size) if 0 <= intercept + i < the_board_size]
        if len(diag) > 1:
            constraints.append(sum(diag) <= 1)
    # 4: each anti-diagonal has at most 1 queen
    for intercept in range(2 * the_board_size - 1):
        anti_diag = [board_cons[i][intercept - i] for i in range(the_board_size)
                     if 0 <= intercept - i < the_board_size]
        if len(anti_diag) > 1:
            constraints.append(sum(anti_diag) <= 1)
    return And(constraints)


def n_queen_sat(the_board_size: int) -> int:
    # step 1: init the board
    init_board(the_board_size)
    # step 2: generate constraints
    constraints = generate_constraints(the_board_size)
    # step 3: solve constraints
    solver = Solver()
    solver.add(constraints)
    # count the number of solutions
    solution_count = 0

    start = time.time()
    while solver.check() == sat:
        solution_count += 1
        model = solver.model()
        solutions = []
        # print the solution
        if debug:
            print(f"a solution to the {the_board_size}-queens problem (*) stands for queens:")
        for i in range(the_board_size):
            for j in range(the_board_size):
                if model.eval(board[i][j]):
                    solutions.append(board[i][j])
                    if debug:
                        print("*", end="")
                else:
                    if debug:
                        print("#", end="")
            if debug:
                print("")

        # add negation of solutions to the solver to get new solution
        solver.add(Not(And(solutions)))
    end = time.time()
    print(f"{the_board_size}-queen problem solved: [{solution_count}] solutions in {(end - start):.6f}s")
    return solution_count

def check_solution(the_board_size: int, expected: List[int], actual: int):
    assert expected[the_board_size] == actual

if __name__ == '__main__':
    # the number of expected solutions:
    # https://oeis.org/A000170/list
    expected_solutions: List[int] = [1,1,0,0,2,10,4,40,92,352,724,2680,14200,73712,
                                     365596,2279184,14772512,95815104,666090624,
                                     4968057848,39029188884,314666222712,2691008701644,
                                     24233937684440,227514171973736,2207893435808352,
                                     22317699616364044,234907967154122528]

    for board_size in range(len(expected_solutions)):
        num_solutions = n_queen_sat(board_size)
        check_solution(board_size, expected_solutions, num_solutions)


