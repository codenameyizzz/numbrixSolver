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
        else:
            self.val = None  # Jika tidak ada objek yang disalin, tetapkan 'val' sebagai None.

    def is_set(self):
        """
        Periksa apakah Val ini memiliki nilai yang ditentukan.
        Mengembalikan True jika 'val' bukan None, yang menunjukkan bahwa nilai telah diatur.
        """
        return self.val is not None

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
