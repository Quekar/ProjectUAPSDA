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
        
        self.btn_messagebox = tk.Button(self.frame_awal, text="Masuk", font=("Helvetica", 14) command=self.pesan1)
        self.btn_messagebox.pack(pady=10)

        self.btn_masuk = tk.Button(self.frame_awal, text="Anggota", font=("Helvetica", 14) )
        self.btn_masuk.pack(pady=10)
        
        self.btn_masuk = tk.Button(self.frame_awal, text="Perkenalan", font=("Helvetica", 14) )
        self.btn_masuk.pack(pady=10)
        
        self.frame_utama = tk.Frame(root)

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
