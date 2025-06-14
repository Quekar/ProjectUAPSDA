import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class AppTkinter:
    def __init__(self, root):
        self.root = root
        self.root.title("Kelompok 3")
        self.root.geometry("1280x720")

        self.root.resizable(False, False)

        self.background()

        self.frame_awal = tk.Frame(self.root, bg="", highlightthickness=0, bd=0)

        # Frame untuk tombol-tombol utama di tengah
        self.btn_messagebox = tk.Button(self.root, text="Masuk", font=("Helvetica", 14), width=20, height=2, command=self.pesan1)
        self.btn_messagebox.place(relx=0.5, rely=0.45, anchor="center")

        self.btn_anggota = tk.Button(self.root, text="Anggota", font=("Helvetica", 14), width=20, height=2, command=self.tampilkan_anggota)
        self.btn_anggota.place(relx=0.5, rely=0.55, anchor="center")

        self.btn_menu = tk.Button(self.root, text="Menu", font=("Helvetica", 14), width=20, height=2, command=self.tampilkan_Menu)
        self.btn_menu.place(relx=0.5, rely=0.65, anchor="center")

    def background(self):
        img = Image.open("tkinter 2.png")  # Ganti sesuai kebutuhan
        img = img.resize((1280, 720))
        self.bg_image = ImageTk.PhotoImage(img)
        self.bg_label = tk.Label(self.root, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    def pesan1(self):
        messagebox.showinfo("Error", "Maaf, fungsi ini belum dibuat")

    def tampilkan_anggota(self):
        self.frame_awal.place_forget()

        # Full frame kanan tanpa kiri
        self.fkanan_anggota = tk.Frame(self.root, bg="white")
        self.fkanan_anggota.place(x=0, y=0, width=1280, height=720)

        # Judul di atas tengah
        label_judul = tk.Label(self.fkanan_anggota, text="Anggota Kami", font=("Helvetica", 28, "bold"), bg="white")
        label_judul.pack(pady=(30, 20))

        data_anggota = [
            {"nama": "Nama : Andhika Akbar Pratama", "npm": "NPM  : 2417051056", "bg": "#ff69b4"},
            {"nama": "Nama : M. Diaz Al Hafidz", "npm": "NPM  : 2417051071", "bg": "#cebea5"},
            {"nama": "Nama : Karina Aini", "npm": "NPM  : 2417051063", "bg": "#fff5e6"},
            {"nama": "Nama : Ardhia Salwa Indriani", "npm": "NPM  : 2457051004", "bg": "#fdfbd4"},
        ]


        for anggota in data_anggota:
            petak = tk.Frame(self.fkanan_anggota, bg=anggota["bg"], bd=1, relief="solid")
            petak.pack(padx="100", pady=5, fill="x")

            label_nama = tk.Label(petak, text=anggota["nama"], font=("Helvetica", 16, "bold"), bg=anggota["bg"], anchor="w")
            label_nama.pack(fill="x", padx=20, pady=(15, 5))

            label_npm = tk.Label(petak, text=anggota["npm"], font=("Helvetica", 16), bg=anggota["bg"], anchor="w")
            label_npm.pack(fill="x", padx=20, pady=(0, 5))

        self.btn_back_anggota = tk.Button(
            self.fkanan_anggota, text="Kembali", font=("Helvetica", 14),
            command=self.kembali_anggota, bg="red", fg="white", width=15
        )
        self.btn_back_anggota.pack(pady=(30, 30))
 

    def kembali_anggota(self):
        self.fkanan_anggota.place_forget()
        self.frame_awal.place(relx=0.5, rely=0.5, anchor="center")

    def Menu(self):
        self.frame_awal.place_forget()
        self.root.attributes("-fullscreen", True)
        self.tampilkan_Menu()

    def tampilkan_Menu(self):
        self.frame_Menu = tk.Frame(self.root, bg="white")
        self.frame_Menu.place(x=0, y=0, relwidth=1, relheight=1)

        kotak_tengah = tk.Frame(self.frame_Menu, bg="white")
        kotak_tengah.place(relx=0.5, rely=0.5, anchor="center")

        teks = (
            "Ini adalah project akhir Struktur Data Algoritma yang menggunakan Tkinter \n"
            "ato semacamnya. (ini hanya placeholder)"
        )

        label_Menu = tk.Label(self.frame_Menu, text=teks, font=("Helvetica", 14), bg="white", justify="center", anchor="n")
        label_Menu.pack(padx=30, pady=30)

        self.btn_back_Menu = tk.Button(kotak_tengah, text="Kembali", font=("Helvetica", 14), command=self.kembali_Menu)
        self.btn_back_Menu.pack(pady=(50, 10))

    def kembali_Menu(self):
        self.frame_Menu.place_forget()
        self.frame_awal.place(relx=0.5, rely=0.5, anchor="center")


if __name__ == "__main__":
    root = tk.Tk()
    app = AppTkinter(root)
    root.mainloop()
