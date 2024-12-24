from metaflow import FlowSpec, step, Parameter

class KuliahInformatikaFlow(FlowSpec):
    """
    Alur kerja mengikuti kuliah di informatika, mulai dari membayar SPP hingga mendapatkan nilai akhir mata kuliah.
    """

    # Parameter untuk input pengguna
    nama_mahasiswa = Parameter('nama', help="Nama mahasiswa", default="Atsaqif")
    spp_dibayar = Parameter('spp', help="Jumlah SPP yang dibayar", default=5000000)
    jumlah_pertemuan = Parameter('pertemuan', help="Jumlah pertemuan kuliah yang diikuti", default=14)
    jumlah_tugas = Parameter('tugas', help="Jumlah tugas yang dikerjakan", default=6)
    nilai_ujian = Parameter('ujian', help="Nilai ujian akhir", default=85.0)

    @step
    def start(self):
        """
        Mulai alur kerja dengan menyapa mahasiswa.
        """
        print(f"Selamat datang, {self.nama_mahasiswa}!")
        self.next(self.bayar_spp)

    @step
    def bayar_spp(self):
        """
        Langkah untuk membayar SPP.
        """
        if self.spp_dibayar >= 5000000:
            print(f"{self.nama_mahasiswa} telah membayar SPP sebesar Rp{self.spp_dibayar}.")
            self.spp_lunas = True
        else:
            print(f"{self.nama_mahasiswa} belum membayar SPP secara penuh.")
            self.spp_lunas = False
        self.next(self.kuliah)

    @step
    def kuliah(self):
        """
        Langkah untuk mengikuti kuliah.
        """
        if self.spp_lunas:
            print(f"{self.nama_mahasiswa} mengikuti {self.jumlah_pertemuan} pertemuan kuliah.")
            self.kehadiran_memadai = self.jumlah_pertemuan >= 12  # Minimal 12 pertemuan
        else:
            self.kehadiran_memadai = False
        self.next(self.kerjakan_tugas)

    @step
    def kerjakan_tugas(self):
        """
        Langkah untuk mengerjakan tugas.
        """
        if self.kehadiran_memadai:
            print(f"{self.nama_mahasiswa} mengerjakan {self.jumlah_tugas} tugas.")
            self.tugas_memadai = self.jumlah_tugas >= 5  # Minimal 5 tugas
        else:
            self.tugas_memadai = False
        self.next(self.ujian)

    @step
    def ujian(self):
        """
        Langkah untuk mengikuti ujian.
        """
        if self.tugas_memadai:
            print(f"{self.nama_mahasiswa} mengikuti ujian akhir dan mendapatkan nilai {self.nilai_ujian}.")
            self.nilai_akhir = (self.nilai_ujian * 0.7) + (self.jumlah_tugas * 0.3)
        else:
            self.nilai_akhir = "Tidak Lulus"
        self.next(self.end)

    @step
    def end(self):
        """
        Langkah terakhir: Menampilkan hasil akhir.
        """
        if isinstance(self.nilai_akhir, float):
            print(f"Selamat, {self.nama_mahasiswa}! Nilai akhir Anda adalah {self.nilai_akhir:.2f}.")
        else:
            print(f"{self.nama_mahasiswa}, Anda tidak lulus mata kuliah ini.")
        print("Proses kuliah selesai.")

# Untuk menjalankan flow:
if __name__ == "__main__":
    KuliahInformatikaFlow()
