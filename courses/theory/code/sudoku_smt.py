"""
The sudoku problem.

In classic Sudoku, the objective is to fill a 9 × 9 grid with digits
so that each column, each row, and each of the nine 3 × 3 subgrids
that compose the grid (also called "boxes", "blocks", or "regions")
contains all the numbers from 1 to 9.

Often, the puzzle setter provides a partially completed grid, which,
for a well-posed puzzle, has a single solution.

It is worthy noting that the general problem of solving Sudoku
puzzles on n^2×n^2 grids of n×n blocks is known to be NP-complete,
i.e., no efficient algorithms are known yet.

For more background information, please refer to:
https://en.wikipedia.org/wiki/Sudoku

In this code, we solve the sudoku problem with the linear arithmetic-based
SMT approach.
"""
import threading
import time
from typing import List

from z3 import *

DEBUG: bool = False

summary = dict()

# the board to place numbers
board: List[List[BoolRef]] = []
board_cons: List[BoolRef] = []

# note that the board size is box_size * box_size
def init_board(box_size: int):
    global board
    global board_cons
    board_size = box_size * box_size
    if DEBUG:
        print("board size:", board_size)
    board = [[Int(f"x_{i}_{j}") for j in range(board_size)] for i in range(board_size)]
    if DEBUG:
        print("the board: ", board)
    for i in range(board_size):
        for j in range(board_size):
            board_cons.append(And(board[i][j] >= 1, board[i][j] <= board_size))
    if DEBUG:
        print("the initial constraint:", board_cons)

def make_constraints(positions: List[BoolRef]):
    length = len(positions)
    for i in range(length):
        for j in range(i+1, length):
            board_cons.append(And(positions[i] != positions[j]))

def generate_constraints(box_size: int) -> BoolRef:
    global board
    global board_cons
    board_size = box_size*box_size
    # 1: each row has all numbers in [1, box_size * box_size]:
    for i in range(board_size):
        make_constraints(board[i])
    if DEBUG:
        print("after generating rows: ", board_cons)

    # 1: each column has all numbers in [1, box_size * box_size]:
    for i in range(board_size):
        positions: List[BoolRef] = []
        for j in range(board_size):
            positions.append(board[j][i])
        make_constraints(positions)
    # 3: each box has all numbers in [1, box_size * box_size]:
    # the start position
    pos_x = 0
    while pos_x < board_size:
        pos_y = 0
        while pos_y < board_size:
            positions: List[BoolRef] = [board[pos_x + i][pos_y+j] for i in range(box_size)
                                        for j in range(box_size)]
            make_constraints(positions)
            pos_y += box_size
        pos_x += box_size

    return And(board_cons)

sem = threading.Semaphore(1)
def the_printer():
    while True:
        if sem.acquire(blocking=True, timeout=1):
            sem.release()
            break
        print("...", end="")

def sudoku_smt(box_size: int):
    global board
    global board_cons
    board = []
    board_cons = []
    board_size = box_size*box_size
    # step 1: init the board
    init_board(box_size)
    # step 2: generate constraints
    constraints = generate_constraints(box_size)
    # step 3: solve constraints
    solver = Solver()
    solver.add(constraints)

    start = time.time()
    print(f"solving the {box_size}^2*{box_size}^2-sudoku problem starting ", end="")
    # to print some heart
    sem.acquire()
    the_printer_thread = threading.Thread(target=the_printer)
    the_printer_thread.start()
    result = solver.check()
    sem.release()
    the_printer_thread.join()
    if result == sat:
        model = solver.model()
        # print the solution, prettily
        print(f"a solution is:")
        for i in range(board_size):
            for j in range(board_size):
                value = model.eval(board[i][j])
                print(f"{value}, ", end="")
                if (j+1) % box_size == 0:
                    print("| ", end="")
            print("")
            if (i+1) % box_size == 0:
                for j in range(board_size*4):
                    print("-", end="")
                print("")
    else:
        print("no solution")
    end = time.time()
    duration = end-start
    print(f"solving the {box_size}^2*{box_size}^2-sudoku problem finished, in {duration:.6f}s")
    # bookkeeping
    summary[board_size] = duration
    return

if __name__ == '__main__':
    N = 10
    for box_size in range(1, N):
        sudoku_smt(box_size)
    #
    print("Execution summary:")
    for k, v in summary.items():
        print(f"{k}-sudoku used: {v}s")



