import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk 

class AppTkinter:
    def __init__(self, root):
        self.root = root
        self.root.title("Lorem Ipsum")
        self.root.geometry("1280x720")
        self.root.resizeable(False, False)
        
        self.frame_awal = tk.Frame(root, bg="white")
        self.frame_awal.pack(fill="both", expand=True)

        self.label_nama = tk.Label(self.frame_awal, text="Selamat Datang di Project SDA", font=("Helvetica", 18), bg="white")
        self.label_nama.pack(pady=50)

        self.btn_masuk = tk.Button(self.frame_awal, text="Masuk", font=("Helvetica", 14), command=self.buka_halaman_utama)
        self.btn_masuk.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = AppTkinter(root)
    root.mainloop()
