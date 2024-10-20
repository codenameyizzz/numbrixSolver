# solver.py
import random
import math
from board import Board
import copy

def solve(board, debug_level, step_callback=None):
    """
    Menyelesaikan puzzle Numbrix menggunakan Simulated Annealing, sebuah teknik optimisasi probabilistik.
    
    Parameter:
    - board: Papan permainan Numbrix yang akan diselesaikan.
    - debug_level: Tingkat detail log yang diinginkan ("none", "trace").
    - step_callback: Fungsi callback yang dipanggil setiap kali papan diperbarui.
    
    Metode ini mengimplementasikan algoritma Simulated Annealing:
    1. Inisialisasi: Mulai dengan papan sembarang dan tetapkan suhu awal.
    2. Iterasi: Lakukan proses penurunan suhu dan terima atau tolak perubahan berdasarkan perbandingan konflik.
    3. Pendinginan: Turunkan suhu secara eksponensial.
    4. Kriteria Berhenti: Berhenti jika suhu mencapai 0 atau solusi ditemukan atau iterasi maksimal tercapai.
    """
    max_iterations = 50000  # Batas maksimum iterasi yang diizinkan sebelum berhenti.
    temperature = 1.0  # Suhu awal untuk proses Simulated Annealing.
    cooling_rate = 0.00002  # Laju pendinginan, mengatur seberapa cepat suhu turun.

    current_board = Board(other_board=board)  # Membuat salinan dari papan yang diberikan.
    current_board.initialize_board()  # Inisialisasi papan dengan konfigurasi sembarang.
    current_conflicts = current_board.calculate_conflicts()  # Menghitung jumlah konflik awal pada papan.
    iteration = 0  # Inisialisasi penghitung iterasi.

    if step_callback:
        step_callback(copy.deepcopy(current_board))  # Tambahkan langkah awal

    # Proses iterasi dilakukan sampai salah satu kriteria berhenti terpenuhi.
    while iteration < max_iterations and not current_board.is_goal() and temperature > 0:
        iteration += 1
        neighbors = current_board.get_neighbors()  # Dapatkan papan tetangga dari papan saat ini.
        if not neighbors:
            break  # Tidak ada tetangga yang bisa dihasilkan
        neighbor = min(neighbors, key=lambda b: b.calculate_conflicts())  # Pilih tetangga dengan konflik terkecil.
        neighbor_conflicts = neighbor.calculate_conflicts()
        delta = neighbor_conflicts - current_conflicts  # Hitung perubahan konflik dari papan saat ini ke tetangga.

        # Terima perubahan jika mengurangi konflik atau berdasarkan probabilitas yang dihitung dari delta suhu.
        if delta < 0 or random.uniform(0, 1) < math.exp(-delta / temperature):
            current_board = neighbor
            current_conflicts = neighbor_conflicts
            if step_callback:
                step_callback(copy.deepcopy(current_board))  # Tambahkan langkah baru

        temperature *= 1 - cooling_rate  # Turunkan suhu secara eksponensial.

        # Log status saat ini jika mode debug "trace" aktif dan setiap 1000 iterasi.
        if debug_level == "trace" and iteration % 1000 == 0:
            print(f"Iteration {iteration}, Temperature: {temperature:.4f}, Conflicts: {current_conflicts}")

    # Evaluasi hasil akhir setelah loop selesai.
    if current_board.is_goal():
        print(f"Success! Found a solution in {iteration} iterations.")
        print(current_board)
    else:
        print(f"Failed to find a solution after {iteration} iterations.")
        print(f"Final conflicts: {current_conflicts}")
        print(current_board)

def check_line(line):
    """
    Memeriksa satu baris input untuk memastikan bahwa formatnya valid:
    - Baris harus memiliki sembilan nilai.
    - Setiap nilai harus berupa digit (1-81) atau tanda '-' yang menandakan sel kosong.
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
    """
    Menyimpan satu baris nilai ke dalam papan pada posisi yang ditentukan:
    - Digit disimpan sebagai nilai tetap.
    - Sel kosong tidak diatur.
    """
    for col, val in enumerate(line.strip().split()):
        if val.isdigit():
            board.set(row, col, int(val), is_fixed=True)

def read_input_from_file(file, board):
    """
    Membaca konfigurasi papan dari file:
    - Memastikan file memiliki tepat 9 baris.
    - Setiap baris harus valid menurut `check_line`.
    """
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
    lines = 0
    while lines < 9:
        line = input("Please enter line " + str(lines + 1) + ": ")
        if check_line(line):
            store_line(line, lines, board)
            lines += 1
        else:
            print("Error while parsing line, expecting nine values, 1-81 or '-' separated by spaces, please try again")
    print(f"All lines entered, input board:\n{board}")
