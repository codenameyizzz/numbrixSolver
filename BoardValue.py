# BoardValue.py

class Val:
    """
    A class to represent a value location in a Numbrix board.
    """

    def __init__(self, val_to_copy=None):
        """Initialize the Val object."""
        self.val = None
        self.is_fixed = False  # Indicates if the value is a clue (given)

        if val_to_copy is not None:
            self.val = val_to_copy.val
            self.is_fixed = val_to_copy.is_fixed
        else:
            self.val = None

    def is_set(self):
        """Check if this Val has a defined value."""
        return self.val is not None

    def get(self):
        """Get the current value."""
        return self.val

    def set(self, value, is_fixed=False):
        """Set the value and whether it is fixed."""
        self.val = value
        self.is_fixed = is_fixed

    def __str__(self):
        """String representation of the Val."""
        if self.is_set():
            return str(self.get())
        else:
            return "-"
