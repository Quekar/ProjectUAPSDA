import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk 

class AppTkinter:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Tkinter")
        self.root.geometry("1280x720")
        self.root.resizable(False, False)

        self.background()
        # klo ada yg mau / niat ganti ke canvas silahkan, gwehj malas
        self.frame_awal = tk.Frame(self.root, highlightbackground="red" ,highlightcolor="red", bd=0, highlightthickness=5)
        self.frame_awal.place(relx=0.5, rely=0.5, anchor="center")
        
        self.btn_messagebox = tk.Button(self.frame_awal, text="Masuk", font=("Helvetica", 14), command=self.pesan1)
        self.btn_messagebox.pack(pady=10)

        self.btn_masuk = tk.Button(self.frame_awal, text="Anggota", font=("Helvetica", 14), command=self.anggota)
        self.btn_masuk.pack(pady=10)
        
        self.btn_masuk = tk.Button(self.frame_awal, text="Perkenalan", font=("Helvetica", 14), command=self.perkenalan)
        self.btn_masuk.pack(pady=10)
        
        self.frame_utama = tk.Frame(root)

    def anggota(self):
        self.frame_awal.place_forget()
        self.tampilkananggota()
    
    def perkenalan(self):
        self.frame_awal.place_forget()
        self.tampilperkenalan()
    
    def tampilperkenalan(self):
        self.frame_perkenalan = tk.Frame(self.root, highlightbackground="blue", highlightthickness=3)
        self.frame_perkenalan.place(relx=0.5, rely=0.5, anchor="center")

        # Placeholder, plis ganti nanti
        teks = (
            "Ini adalah project akhir Struktur Data Algoritma yang menggunakan Tkinter \n"
            "ato semacamnya.(ini hanya placeholder)"
        )
        
         label_perkenalan = tk.Label(
            self.frame_perkenalan,
            text=teks,
            font=("Helvetica", 14),
            bg="white",
            justify="center",
            anchor="n"
        )
        label_perkenalan.pack(padx=30, pady=30)
        self.btn_back_perkenalan = tk.Button(self.frame_perkenalan, text="Kembali", font=("Helvetica", 14), command=self.kembali_perkenalan)
        self.btn_back_perkenalan.pack(side="bottom", pady=20)


    def tampilkananggota(self):
        self.fkiri_anggota = tk.Frame(self.root, width=320, height=720, bg="white")
        self.fkiri_anggota.pack_propagate(False)  # Mencegah resize otomatis
        self.fkiri_anggota.pack(side="left", fill="y")

        self.fkanan_anggota = tk.Frame(self.root, width=960, height=720, bg="white")
        self.fkanan_anggota.pack_propagate(False)
        self.fkanan_anggota.pack(side="right", fill="both", expand=True)

        label_judul = tk.Label(self.fkiri_anggota, text="Anggota Kami", font=("Helvetica", 30, "bold"), bg="white", anchor="w")
        label_judul.pack(padx=10, pady=(10, 20), anchor="w")

        data_anggota = [
            {"nama": "Nama : Andhika Akbar Pratama", "npm": "NPM  : 2417051056", "bg": "#ff69b4"},
            {"nama": "Nama : M. Diaz Al Hafidz", "npm": "NPM  : 2417051071", "bg": "#cebea5"},
            {"nama": "Nama : Karina Aini", "npm": "NPM  : 2417051063", "bg": "#fff5e6"},
            {"nama": "Nama : Ardhia Salwa Indriani", "npm": "NPM  : 2457051004", "bg": "#fdfbd4"},
        ]

        for anggota in data_anggota:
            petak = tk.Frame(self.fkanan_anggota, bg=anggota["bg"], bd=1, relief="solid")
            petak.pack(fill="x", padx=10, pady=5)

            label_nama = tk.Label(petak, text=anggota["nama"], font=("Helvetica", 20), bg=anggota["bg"], anchor="w")
            label_nama.pack(fill="x", padx=5, pady=(5, 0))

            label_npm = tk.Label(petak, text=anggota["npm"], font=("Helvetica", 20), bg=anggota["bg"], anchor="w")
            label_npm.pack(fill="x", padx=5, pady=(0, 5))

        
        self.btn_back_anggota = tk.Button(self.fkanan_anggota, text="Kembali", font=("Helvetica", 18), command=self.kembali_anggota, bg="red", fg="white")
        self.btn_back_anggota.pack(side="bottom", pady=20, padx=20, fill="x")

    def kembali_anggota(self):
        self.fkiri_anggota.pack_forget()
        self.fkanan_anggota.pack_forget()
        self.frame_awal.place(relx=0.5, rely=0.5, anchor="center")

    def kembali_perkenalan(self):
        self.frame_perkenalan.place_forget()
        self.frame_awal.place(relx=0.5, rely=0.5, anchor="center")


    def background(self):
        img = Image.open("bg.png") # placeholder, bisa diganti
        img = img.resize((1280, 720))
        self.photo = ImageTk.PhotoImage(img)
        self.label_gambar = tk.Label(self.root, image=self.photo)
        self.label_gambar.place(x=0, y=0, relwidth=1, relheight=1)

    def pesan1(self):
        messagebox.showinfo("Error", "Maaf, fungsi ini belum dibuat")

if __name__ == "__main__":
    root = tk.Tk()
    app = AppTkinter(root)
    root.mainloop()
