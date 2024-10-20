import sys
import tkinter as tk
from Board import Board
from Solver import read_input_from_file, solve
from gui import NumbrixGUI  # Pastikan mengimport kelas GUI yang sesuai

def main(args):
    """
    Fungsi utama yang menjalankan logika penyelesaian papan permainan dalam mode GUI.
    """
    root = tk.Tk()  # Membuat root window
    app = NumbrixGUI(master=root)  # Membuat instance dari GUI

    if len(args) > 1:
        # Jika nama file disertakan, baca papan dari file yang diberikan.
        file = args[1]
        board = Board()
        read_input_from_file(file, board)
        app.set_board(board)  # Pastikan Anda memiliki fungsi di GUI untuk mengatur papan
    else:
        app.prompt_for_input()  # Minta input dari GUI jika tidak ada file

    root.mainloop()  # Mulai loop GUI

if __name__ == "__main__":
    main(sys.argv)
