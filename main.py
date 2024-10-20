# main.py

from Board import Board
from Solver import read_input_from_stdin, read_input_from_file, solve
import sys

DEBUG_LEVEL = "none"
# DEBUG_LEVEL = "trace"

def main(args):
    """Instantiate the board, populate it, then solve."""
    board = Board()

    if len(args) > 1:
        file = args[1]
        read_input_from_file(file, board)
    else:
        read_input_from_stdin(board)

    print("Solving...")
    print()
    solve(board, DEBUG_LEVEL)

if __name__ == "__main__":
    main(sys.argv)
