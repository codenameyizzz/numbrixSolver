# Solver.py

import random
import math
from Board import Board

def solve(board, debug_level):
    """Use Simulated Annealing to solve the Numbrix puzzle."""
    max_iterations = 50000
    temperature = 1.0
    cooling_rate = 0.00002
    current_board = Board(other_board=board)
    current_board.initialize_board()
    current_conflicts = current_board.calculate_conflicts()
    iteration = 0

    while iteration < max_iterations and not current_board.is_goal() and temperature > 0:
        iteration += 1
        neighbors = current_board.get_neighbors()
        neighbor = min(neighbors, key=lambda b: b.calculate_conflicts())
        neighbor_conflicts = neighbor.calculate_conflicts()
        delta = neighbor_conflicts - current_conflicts

        if delta < 0 or random.uniform(0, 1) < math.exp(-delta / temperature):
            current_board = neighbor
            current_conflicts = neighbor_conflicts

        temperature *= 1 - cooling_rate  # Exponential cooling

        if debug_level == "trace" and iteration % 1000 == 0:
            print(f"Iteration {iteration}, Temperature: {temperature:.4f}, Conflicts: {current_conflicts}")

    if current_board.is_goal():
        print(f"Success! Found a solution in {iteration} iterations.")
        print(current_board)
    else:
        print(f"Failed to find a solution after {iteration} iterations.")
        print(f"Final conflicts: {current_conflicts}")
        print(current_board)

def check_line(line):
    """Check that:
      * a line has nine values
      * each val is either digit or "-"
      * digit values are between 1 and 81
    """
    vals = line.strip().split()
    if len(vals) != 9:
        return False

    for val in vals:
        if not (val.isdigit() or val == "-"):
            return False
        if val.isdigit():
            num = int(val)
            if not 1 <= num <= 81:
                return False

    return True

def store_line(line, row, board):
    """Set a line of the board."""
    for col, val in enumerate(line.strip().split()):
        if val.isdigit():
            board.set(row, col, int(val), is_fixed=True)
        else:
            pass  # Empty cells remain unset

def read_input_from_file(file, board):
    """Read a board from a file."""
    with open(file) as f:
        lines = f.readlines()
        if len(lines) != 9:
            raise ValueError("Input file must contain exactly 9 lines.")
        for row, line in enumerate(lines):
            if check_line(line):
                store_line(line, row, board)
            else:
                raise ValueError(f"Invalid line {row + 1} in input file.")
    print(f"All lines read from {file}, input board:\n{board}")

def read_input_from_stdin(board):
    """Read a board from stdin."""
    lines_read = 0
    while lines_read < 9:
        line = input(f"Please enter line {lines_read + 1}: ")
        if check_line(line):
            store_line(line, lines_read, board)
            lines_read += 1
        else:
            print("Error: Each line must contain nine values (1-81 or '-') separated by spaces. Please try again.")
    print(f"All lines entered, input board:\n{board}")
