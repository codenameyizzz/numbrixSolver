# Board.py

from BoardValue import Val
import random

class Board:
    """A Numbrix board."""

    def __init__(self, other_board=None):
        if other_board is not None:
            self.board = []
            for val in other_board.board:
                self.board.append(Val(val_to_copy=val))
        else:
            self.board = [Val() for _ in range(81)]  # Initialize empty board

    def get(self, row, col):
        """Get the value at location (row, col)."""
        if not (0 <= row < 9 and 0 <= col < 9):
            return None
        return self.board[row * 9 + col]

    def set(self, row, col, val, is_fixed=False):
        """Set the value at location (row, col)."""
        if not (0 <= row < 9 and 0 <= col < 9):
            raise ValueError(
                f"Row and column values must be in the range [0 .. 8] but got row: {row}, column: {col}"
            )
        self.board[row * 9 + col].set(val, is_fixed)

    def initialize_board(self):
        """Initialize the board for local search."""
        # Create a list of all numbers from 1 to 81
        numbers = list(range(1, 82))
        # Remove the fixed values from the list
        for val in self.board:
            if val.is_fixed:
                numbers.remove(val.get())
        # Shuffle the remaining numbers
        random.shuffle(numbers)
        # Assign the numbers to the non-fixed cells
        for val in self.board:
            if not val.is_fixed:
                val.set(numbers.pop())

    def calculate_conflicts(self):
        """Calculate the number of conflicts in the board."""
        conflicts = 0
        position_of_number = [None] * 82  # Index 0 unused

        # Map the position of each number
        for row in range(9):
            for col in range(9):
                num = self.get(row, col).get()
                position_of_number[num] = (row, col)

        # Check each number from 1 to 81
        for num in range(1, 82):
            row, col = position_of_number[num]
            val = self.get(row, col)

            # Determine expected adjacent numbers
            if num == 1:
                expected_neighbors = [2]
            elif num == 81:
                expected_neighbors = [80]
            else:
                expected_neighbors = [num - 1, num + 1]

            # Check if expected neighbors are adjacent
            found_neighbors = 0
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                adj_row, adj_col = row + dr, col + dc
                if 0 <= adj_row < 9 and 0 <= adj_col < 9:
                    adj_num = self.get(adj_row, adj_col).get()
                    if adj_num in expected_neighbors:
                        found_neighbors += 1

            # Update conflicts
            conflicts += len(expected_neighbors) - found_neighbors

        return conflicts

    def get_neighbors(self):
        """Generate neighboring boards by swapping two random non-fixed cells."""
        neighbors = []
        non_fixed_positions = [
            (row, col)
            for row in range(9)
            for col in range(9)
            if not self.get(row, col).is_fixed
        ]

        # Generate a fixed number of random neighbors
        for _ in range(10):  # Generate 10 random neighbors
            if len(non_fixed_positions) < 2:
                break
            i, j = random.sample(range(len(non_fixed_positions)), 2)
            new_board = Board(other_board=self)
            (row1, col1) = non_fixed_positions[i]
            (row2, col2) = non_fixed_positions[j]
            val1 = self.get(row1, col1).get()
            val2 = self.get(row2, col2).get()
            new_board.set(row1, col1, val2)
            new_board.set(row2, col2, val1)
            neighbors.append(new_board)
        return neighbors

    def is_goal(self):
        """Check if the board is a valid solution."""
        return self.calculate_conflicts() == 0

    def __repr__(self):
        """String representation of the board."""
        output = "+----------------------------+\n"
        for row in range(9):
            output += "|"
            for col in range(9):
                val = self.get(row, col)
                output += str(val).rjust(3)
            output += " |\n"
        output += "+----------------------------+"
        return output
