def solve(board, debug_level):
    """Use a depth-first search to solve the Numbrix puzzle.

    Approach:
     * Pop the top of the stack of boards to explore
     * Pick a square containing a defined value which has open neighbors
     * Push boards to the stack with the possible "next moves" from the defined value
     * Mark the current board as "seen"
     * If the board is complete, validate it and return success
     * If there are no more possible next moves, report failure
    """
    i = 0
    leaves = 0
    cross_overs = 0

    seen = set()
    stack = [board]

    while len(stack) > 0:
        curr = stack.pop()
        i += 1
        if i % 100 == 0 and debug_level == "info":
            print(f"Iteration {i}, leaves: {leaves}, cross overs: {cross_overs}, current board:\n{curr}")
        elif debug_level == "trace" or debug_level == "pause":
            print(f"Iteration {i}, leaves: {leaves}, cross overs: {cross_overs}, current board:\n{curr}")
            if debug_level == "pause":
                input(":")

        if repr(curr) in seen or curr.is_not_feasible():
            if curr.is_not_feasible():
                leaves += 1
            else:
                cross_overs += 1
            continue

        elif curr.is_complete():
            print(f"Success! Took {i} iterations, found {leaves} dead ends and {cross_overs} graph cross overs.")
            print("  --> Final board:")
            print(curr)
            return

        else:
            boards = curr.get_next_boards()
            stack.extend(boards)
            seen.add(repr(curr))

    print(f"Failure, could not find a solution after {i} iterations. Saw {leaves} dead ends and {cross_overs} "
          "graph cross overs.")


def check_line(line):
    """Check that:
      * a line has nine values
      * each val has length 1 or 2
      * each val is either digital or "-"
      * digital values are between 1 and 81
    """
    vals = line.split()
    if not len(vals) == 9:
        return False

    for val in vals:
        if not 1 <= len(val) <= 2:
            return False
        if not (val.isdigit() or val == "-"):
            return False
        if val.isdigit() and not 1 <= int(val) <= 81:
            return False

    return True


def store_line(line, row, board):
    """Set a line of this solver's board."""
    for col, val in enumerate(line.split()):
        if val.isdigit():
            board.set(row, col, int(val))


def read_input_from_file(file, board):
    """Read a board from a file."""
    with open(file) as f:
        lines = f.readlines()
        for row, line in enumerate(lines):
            store_line(line.strip(), row, board)

    print(f"All lines read from {file}, input board:\n{board}")


def read_input_from_stdin(board):
    """Read a board from stdin."""
    lines = 0
    while lines < 9:
        line = input("Please enter line " + str(lines + 1) + ": ")
        if check_line(line):
            store_line(line, lines, board)
            lines += 1
        else:
            print("Error while parsing line, expecting nine values, 1-81 or '-' separated by spaces, please try again")

    print(f"All lines entered, input board:\n{board}")
