# board.py
import random

def is_one_away(val1, val2):
    """Return whether or not the two values are numerically adjacent."""
    return abs(val1 - val2) == 1

def get_directional_neighbors(row, col):
    """Given a row and column value, return the row and column values of the corresponding up, down, left and right
    neighboring squares."""
    return [[a + b for a, b in zip((row, col), directional)]
            for directional in ((-1, 0), (1, 0), (0, -1), (0, 1))]

def get_all_coordinates_at_distance(row, col, distance):
    """Return all feasible coordinates in a board which have a Manhattan Distance of `distance` from the location given
    by (row, col)."""
    coordinates = set()

    if distance <= 0:
        return coordinates

    pairs = [(x, distance - x) for x in range(distance + 1)]
    for quadrant_multiplier in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
        row_multiplier, col_multiplier = quadrant_multiplier
        for row_pair_part, col_pair_part in pairs:
            r = row + (row_pair_part * row_multiplier)
            c = col + (col_pair_part * col_multiplier)
            if 0 <= r < 9 and 0 <= c < 9:
                coordinates.add((r, c))

    return coordinates

class Val:
    """
    Kelas ini merepresentasikan lokasi nilai pada papan Numbrix.
    """

    def __init__(self, val_to_copy=None):
        """
        Inisialisasi objek Val.
        Objek Val ini dapat diinisialisasi dengan nilai awal atau bisa juga merupakan salinan dari Val lain.
        - `val_to_copy`: Objek Val lain yang nilai dan statusnya akan disalin. Jika None, Val diinisialisasi tanpa nilai.
        """
        self.val = None  # Nilai dari Val, diinisialisasi sebagai None.
        self.is_fixed = False  # Menunjukkan apakah nilai ini adalah petunjuk (diberikan) dan tidak boleh diubah.

        # Jika objek Val lain diberikan, salin nilai dan status 'is_fixed' dari objek tersebut.
        if val_to_copy is not None:
            self.val = val_to_copy.val
            self.is_fixed = val_to_copy.is_fixed
            self.possible_values = val_to_copy.possible_values.copy()
        else:
            self.possible_values = [x for x in range(1, 82)]  # Semua nilai awal mungkin

    def remove_possible_value(self, possible_value):
        """Remove a value from this Val's `possible_values`."""
        if not self.is_set() and possible_value in self.possible_values:
            self.possible_values.remove(possible_value)

    def is_set(self):
        """
        Periksa apakah Val ini memiliki nilai yang ditentukan.
        Mengembalikan True jika 'val' bukan None, yang menunjukkan bahwa nilai telah diatur.
        """
        return self.val is not None

    def possible_values_size(self):
        """Return the size of this Val's `possible_values`."""
        return len(self.possible_values)

    def get(self):
        """
        Dapatkan nilai saat ini.
        Mengembalikan nilai dari atribut 'val'.
        """
        return self.val

    def set(self, value, is_fixed=False):
        """
        Tetapkan nilai dan apakah itu tetap.
        - `value`: Nilai yang akan diatur.
        - `is_fixed`: Boolean yang menunjukkan apakah nilai ini tidak boleh diubah.
        Ini memperbarui 'val' dan 'is_fixed' berdasarkan parameter yang diberikan.
        """
        self.val = value
        self.is_fixed = is_fixed
        if is_fixed:
            self.possible_values = []  # Clear possible values if fixed

    def __str__(self):
        """
        Representasi string dari Val.
        Jika nilai telah diatur ('is_set' mengembalikan True), mengembalikan nilai sebagai string.
        Jika tidak, mengembalikan "-" yang menunjukkan bahwa Val belum diatur.
        """
        if self.is_set():
            return str(self.get())
        else:
            return "-"

class Board:
    """Papan Numbrix."""

    def __init__(self, other_board=None):
        if other_board is not None:
            self.board = []
            for val in other_board.board:
                self.board.append(Val(val_to_copy=val))
        else:
            self.board = [Val() for _ in range(81)]  # Inisialisasi papan kosong

    def is_complete(self):
        """Check if the board has valid values for all squares."""
        return False not in [v.is_set() for v in self.board]

    def is_not_feasible(self):
        """Check if the current board is no longer feasible.

        This may happen if:
         * Any squares no longer have any feasible values which they can hold
         * Any squares have become somewhat surrounded but they do not have their required "correct neighbors"
        """
        for row in range(9):
            for col in range(9):
                val = self.get(row, col)
                if val.is_set() and not self.would_be_feasible(row, col, val.get()):
                    return True

        return len([1 for v in self.board if not v.is_set() and v.possible_values_size() == 0]) > 0

    def get(self, row, col):
        """Dapatkan nilai pada lokasi (baris, kolom)."""
        if not (0 <= row < 9 and 0 <= col < 9):
            return None
        return self.board[row * 9 + col]

    def set(self, row, col, val, is_fixed=False):
        """Atur nilai pada lokasi (baris, kolom)."""
        if not (0 <= row < 9 and 0 <= col < 9):
            raise ValueError(
                f"Nilai baris dan kolom harus berada dalam rentang [0 .. 8] tetapi diberi baris: {row}, kolom: {col}"
            )
        self.board[row * 9 + col].set(val, is_fixed)

        # Ripple effect: remove possible values from surrounding cells
        for distance in range(1, 17):  # 16 is the maximum board distance
            for r, c in get_all_coordinates_at_distance(row, col, distance):
                if self.get(r, c) is not None:
                    for v in range(val - distance + 1, val + distance):
                        if 1 <= v <= 81:
                            self.get(r, c).remove_possible_value(v)

    def would_be_feasible(self, row, col, val):
        """Check if the provided value would be feasible at the specified location.

        For a value to be feasible at a location, it must have (provided it is not 1 or 81):
         * At least two open neighbors (if none of the directional neighbors are correct)
         * Or one correct directional neighbor and at least one open neighbor
         * Or two correct directional neighbors

        If the value is 1 or 81:
         * It can either have at least one open neighbor
         * Or one correct directional neighbor
        """
        open_neighbors = 0
        correct_directional_neighbors = 0

        for directional_row, directional_col in get_directional_neighbors(row, col):
            if not (0 <= directional_row < 9 and 0 <= directional_col < 9):
                continue

            directional_val = self.get(directional_row, directional_col)
            if not directional_val.is_set():
                open_neighbors += 1
            elif is_one_away(val, directional_val.get()):
                correct_directional_neighbors += 1

        if val == 1 or val == 81:
            return open_neighbors >= 1 or correct_directional_neighbors == 1
        else:
            return (correct_directional_neighbors == 0 and open_neighbors >= 2) or \
                   (correct_directional_neighbors == 1 and open_neighbors >= 1) or \
                   correct_directional_neighbors == 2

    def get_next_boards(self):
        """Evaluate the board and take the next logical assignments on some specific square. Return all boards that
        represent feasible moves on the minimal options location.
        """
        next_boards = []

        minimal_options_val_tuple = None

        for row in range(9):
            for col in range(9):
                val = self.get(row, col)
                if not val.is_set() and (
                        minimal_options_val_tuple is None
                        or val.possible_values_size() < minimal_options_val_tuple[0].possible_values_size()):
                    minimal_options_val_tuple = (val, row, col)

        if minimal_options_val_tuple is None:
            return next_boards  # No possible moves

        # Minimal options location has been identified, now return all feasible values as possible next boards
        val, row, col = minimal_options_val_tuple
        for value in val.possible_values:
            if self.would_be_feasible(row, col, value):
                new_board = Board(other_board=self)
                new_board.set(row, col, value)
                next_boards.append(new_board)

        return next_boards

    def initialize_board(self):
        """Inisialisasi papan untuk pencarian lokal."""
        numbers = list(range(1, 82))
        for val in self.board:
            if val.is_fixed:
                if val.get() in numbers:
                    numbers.remove(val.get())
        random.shuffle(numbers)
        for val in self.board:
            if not val.is_fixed:
                if numbers:
                    val.set(numbers.pop())

    def calculate_conflicts(self):
        """Hitung jumlah konflik di papan."""
        conflicts = 0
        position_of_number = [None] * 82  # Indeks 0 tidak digunakan

        # Peta posisi setiap angka
        for row in range(9):
            for col in range(9):
                num = self.get(row, col).get()
                if num is not None:
                    position_of_number[num] = (row, col)

        # Periksa setiap angka dari 1 hingga 81
        for num in range(1, 82):
            if position_of_number[num] is None:
                continue  # Angka tidak ditempatkan di papan
            row, col = position_of_number[num]
            val = self.get(row, col)

            # Tentukan angka tetangga yang diharapkan
            if num == 1:
                expected_neighbors = [2]
            elif num == 81:
                expected_neighbors = [80]
            else:
                expected_neighbors = [num - 1, num + 1]

            # Periksa jika tetangga yang diharapkan berdekatan
            found_neighbors = 0
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                adj_row, adj_col = row + dr, col + dc
                if 0 <= adj_row < 9 and 0 <= adj_col < 9:
                    adj_num = self.get(adj_row, adj_col).get()
                    if adj_num in expected_neighbors:
                        found_neighbors += 1

            # Perbarui konflik
            conflicts += len(expected_neighbors) - found_neighbors

        return conflicts

    def get_neighbors(self):
        """Hasilkan papan tetangga dengan menukar dua sel acak yang tidak tetap."""
        neighbors = []
        non_fixed_positions = [
            (row, col)
            for row in range(9)
            for col in range(9)
            if not self.get(row, col).is_fixed
        ]

        # Hasilkan sejumlah tetangga acak yang tetap
        for _ in range(10):  # Hasilkan 10 tetangga acak
            if len(non_fixed_positions) < 2:
                break
            pos1, pos2 = random.sample(non_fixed_positions, 2)
            row1, col1 = pos1
            row2, col2 = pos2
            val1 = self.get(row1, col1).get()
            val2 = self.get(row2, col2).get()
            new_board = Board(other_board=self)
            new_board.set(row1, col1, val2, is_fixed=False)
            new_board.set(row2, col2, val1, is_fixed=False)
            neighbors.append(new_board)
        return neighbors

    def is_goal(self):
        """Periksa apakah papan adalah solusi yang valid."""
        return self.calculate_conflicts() == 0

    def __repr__(self):
        """Representasi string dari papan."""
        output = "+----------------------------+\n"
        for row in range(9):
            output += "|"
            for col in range(9):
                val = self.get(row, col)
                output += str(val).rjust(3)
            output += " |\n"
        output += "+----------------------------+"
        return output
