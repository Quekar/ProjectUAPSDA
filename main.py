import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import csv
import os

class MatchData:
    def __init__(self, division, ao_name, aka_name, ao_score, aka_score, ao_status, aka_status, time_elapsed):
        self.division = division
        self.ao_name = ao_name
        self.aka_name = aka_name
        self.ao_score = ao_score
        self.aka_score = aka_score
        self.ao_status = ao_status
        self.aka_status = aka_status
        self.time_elapsed = time_elapsed

class CSVLogger:
    def __init__(self, filename='karate_scores.csv'):
        self.filename = filename
        self._initialize_file()
    def _initialize_file(self):
        if not os.path.exists(self.filename):
            with open(self.filename, mode='w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'Division', 'Ao Name', 'Aka Name',
                    'Ao Score', 'Aka Score',
                    'Ao Status', 'Aka Status',
                    'Time'
                ])
    def log_match(self, match: MatchData):
        with open(self.filename, mode='a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                match.division, match.ao_name, match.aka_name,
                match.ao_score, match.aka_score,
                match.ao_status, match.aka_status,
                match.time_elapsed
            ])

class ScoreManager:
    def __init__(self):
        self.ao_score = 0
        self.aka_score = 0
        self.ao_status = "Normal"
        self.aka_status = "Normal"
    def update_score(self, team: str, delta: int):
        if team == "Ao":
            self.ao_score = max(0, self.ao_score + delta)
        elif team == "Aka":
            self.aka_score = max(0, self.aka_score + delta)

class KarateApp:
    def __init__(self, root, back_callback=None):
        self.root = root
        self.back_callback = back_callback
        self.root.title("Karate Scoring App")
        self.root.geometry("1280x720")
        self.root.resizable(False, False)
        self.score_manager = ScoreManager()
        self.stopwatch_running = False
        self.stopwatch_seconds = 0
        self.stopwatch_job = None
        self.stopwatch_visible = True

        self.ao_locked = False
        self.aka_locked = False
        self.division_locked = False

        self.create_frames()
        self.create_top_frame()
        self.create_left_frame()
        self.create_right_frame()
        self.create_bottom_frame()
    
    def toggle_stopwatch(self):
        if not self.stopwatch_running:
            self.stopwatch_running = True
            self.stopwatch_btn.config(text="Pause")
            self.update_stopwatch()
        else:
            self.stopwatch_running = False
            self.stopwatch_btn.config(text="Start")
            if self.stopwatch_job:
                self.root.after_cancel(self.stopwatch_job)
    
    def toggle_stopwatch_display(self):
        if self.stopwatch_visible:
            self.stopwatch_label_ao.place_forget()
            self.stopwatch_label_aka.place_forget()
            self.toggle_stopwatch_btn.config(text="Show Stopwatch")
            self.stopwatch_visible = False
        else:
            self.stopwatch_label_ao.place(x=250, y=320)
            self.stopwatch_label_aka.place(x=250, y=320)
            self.toggle_stopwatch_btn.config(text="Hide Stopwatch")
            self.stopwatch_visible = True

    def format_time(self, seconds):
        mins = seconds // 60
        secs = seconds % 60
        return f"{mins:02}:{secs:02}"

    def update_stopwatch(self):
        mins, secs = divmod(self.stopwatch_seconds, 60)
        time_str = f"{mins:02}:{secs:02}"
        self.stopwatch_label_ao.config(text=time_str)
        self.stopwatch_label_aka.config(text=time_str)
        self.stopwatch_seconds += 1
        self.stopwatch_job = self.root.after(1000, self.update_stopwatch)

    def apply_penalty(self, team: str, penalty_type: str):
        if team == "Ao":
            self.score_manager.ao_score = 0
            self.score_manager.ao_status = penalty_type
            self.ao_score_var.set(0)
            self.flag_label_ao.config(image=self.white_flag)
            if penalty_type in ["Shikkaku", "Kikken"]:
                self.score_manager.aka_score = 8
                self.aka_score_var.set(8)
        elif team == "Aka":
            self.score_manager.aka_score = 0
            self.score_manager.aka_status = penalty_type
            self.aka_score_var.set(0)
            self.flag_label_aka.config(image=self.white_flag)
            if penalty_type in ["Shikkaku", "Kikken"]:
                self.score_manager.ao_score = 8
                self.ao_score_var.set(8)

    def create_frames(self):
            self.frame_atas = tk.Frame(self.root, height=80, width=1280, bg='lightgray')
            self.frame_atas.place(x=0, y=0)
    
            self.frame_kiri = tk.Frame(self.root, height=560, width=640, bg='blue')
            self.frame_kiri.place(x=0, y=80)
    
            self.frame_kanan = tk.Frame(self.root, height=560, width=640, bg='red')
            self.frame_kanan.place(x=640, y=80)
    
            self.frame_bawah = tk.Frame(self.root, height=80, width=1280, bg='white')
            self.frame_bawah.place(x=0, y=640)

    def create_top_frame(self):
        self.ao_name_var = tk.StringVar()
        self.ao_name_entry = tk.Entry(self.frame_atas, textvariable=self.ao_name_var, width=20)
        self.ao_name_entry.place(x=50, y=30)

        self.division_var = tk.StringVar()
        self.division_combo = ttk.Combobox(self.frame_atas, textvariable=self.division_var, state='readonly')
        self.division_combo['values'] = ['Perebutan Gelar', 'Lomba Non Gelar']
        self.division_combo.current(0)
        self.division_combo.place(x=500, y=25)
        tk.Label(self.frame_atas, text="Division:", bg='lightgray').place(x=440, y=25)

        tk.Label(self.frame_atas, text="[5] Judges", bg='lightgray', font=("Arial", 10)).place(x=500, y=50)

        self.aka_name_var = tk.StringVar()
        self.aka_name_entry = tk.Entry(self.frame_atas, textvariable=self.aka_name_var, width=20)
        self.aka_name_entry.place(x=900, y=30)
        self.ao_name_entry.bind("<Return>", self.lock_ao_name)
        self.aka_name_entry.bind("<Return>", self.lock_aka_name)
        self.division_combo.bind("<<ComboboxSelected>>", self.lock_division)
        
        self.close_btn = tk.Button(self.frame_atas, text="Kembali", bg='red', fg='white', command=self.kembali_main)
        self.close_btn.place(x=1180, y=10, width=90, height=30)

    def lock_ao_name(self, event=None):
        if not self.ao_locked:
            name = self.ao_name_var.get().strip()
            if name:
                self.ao_locked = True
                self.ao_name_entry.destroy()
                tk.Label(self.frame_atas, text=name, bg='lightgray', font=("Arial", 12)).place(x=50, y=30)
                self.try_log_names()

    def lock_aka_name(self, event=None):
        if not self.aka_locked:
            name = self.aka_name_var.get().strip()
            if name:
                self.aka_locked = True
                self.aka_name_entry.destroy()
                tk.Label(self.frame_atas, text=name, bg='lightgray', font=("Arial", 12)).place(x=900, y=30)
                self.try_log_names()

    def lock_division(self, event=None):
        if not self.division_locked:
            division = self.division_var.get().strip()
            if division:
                self.division_locked = True
                self.division_combo.config(state="disabled")
                self.try_log_names()
   
    def try_log_names(self):
        if self.ao_locked and self.aka_locked and self.division_locked:
            match_data = MatchData(
                division=self.division_var.get(),
                ao_name=self.ao_name_var.get(),
                aka_name=self.aka_name_var.get(),
                ao_score=0,
                aka_score=0,
                ao_status="Normal",
                aka_status="Normal",
                time_elapsed="00:00"
            )
            CSVLogger().log_match(match_data)

    def create_left_frame(self):
        self.flag_box_ao = tk.Frame(self.frame_kiri, width=180, height=120, bg='white', bd=2, relief='ridge')
        self.flag_box_ao.place(x=230, y=20)

        self.blue_flag_img = Image.open("blue.png").resize((180, 120)) #bendera biru placeholder
        self.white_flag_img = Image.open("white.png").resize((180, 120)) #bendera putih placeholder
        self.blue_flag = ImageTk.PhotoImage(self.blue_flag_img)
        self.white_flag = ImageTk.PhotoImage(self.white_flag_img)

        self.flag_label_ao = tk.Label(self.flag_box_ao, image=self.blue_flag, bg='white')
        self.flag_label_ao.pack()

        self.ao_score_var = tk.IntVar(value=0)
        self.ao_score_label = tk.Label(self.frame_kiri, textvariable=self.ao_score_var, font=("Arial", 48, "bold"), fg='white', bg='blue')
        self.ao_score_label.place(x=270, y=160)

        self.ao_plus_btn = tk.Button(self.frame_kiri, text="+1", width=6, height=2, font=("Arial", 14), command=lambda: self.update_score("Ao", 1))
        self.ao_plus_btn.place(x=180, y=240)

        self.ao_minus_btn = tk.Button(self.frame_kiri, text="-1", width=6, height=2, font=("Arial", 14), command=lambda: self.update_score("Ao", -1))
        self.ao_minus_btn.place(x=360, y=240)

        self.stopwatch_label_ao = tk.Label(self.frame_kiri, text="00:00", font=("Arial", 32, "bold"), fg='white', bg='blue')
        self.stopwatch_label_ao.place(x=250, y=320)

        self.shikkaku_ao_btn = tk.Button(self.frame_kiri, text="Shikkaku", font=("Arial", 12, "bold"), width=10, bg='black', fg='white', command=lambda: self.apply_penalty("Ao", "Shikkaku"))
        self.shikkaku_ao_btn.place(x=180, y=400)

        self.kikken_ao_btn = tk.Button(self.frame_kiri, text="Kikken", font=("Arial", 12, "bold"), width=10, bg='gray', fg='white', command=lambda: self.apply_penalty("Ao", "Kikken"))
        self.kikken_ao_btn.place(x=360, y=400)

    def create_right_frame(self):
        self.flag_box_aka = tk.Frame(self.frame_kanan, width=180, height=120, bg='white', bd=2, relief='ridge')
        self.flag_box_aka.place(x=230, y=20)


        self.red_flag_img = Image.open("red.png").resize((180, 120)) #bendera merah placeholder
        self.white_flag_img = Image.open("white.png").resize((180, 120)) #bendera putih placeholder
        self.red_flag = ImageTk.PhotoImage(self.red_flag_img)
        self.white_flag = ImageTk.PhotoImage(self.white_flag_img)

        self.flag_label_aka = tk.Label(self.flag_box_aka, image=self.red_flag, bg='white')
        self.flag_label_aka.pack()

        self.aka_score_var = tk.IntVar(value=0)
        self.aka_score_label = tk.Label(self.frame_kanan, textvariable=self.aka_score_var, font=("Arial", 48, "bold"), fg='white', bg='red')
        self.aka_score_label.place(x=270, y=160)

        self.aka_plus_btn = tk.Button(self.frame_kanan, text="+1", width=6, height=2, font=("Arial", 14), command=lambda: self.update_score("Aka", 1))
        self.aka_plus_btn.place(x=180, y=240)

        self.aka_minus_btn = tk.Button(self.frame_kanan, text="-1", width=6, height=2, font=("Arial", 14), command=lambda: self.update_score("Aka", -1))
        self.aka_minus_btn.place(x=340, y=240)

        self.stopwatch_label_aka = tk.Label(self.frame_kanan, text="00:00", font=("Arial", 32, "bold"), fg='white', bg='red')
        self.stopwatch_label_aka.place(x=250, y=320)

        self.shikkaku_aka_btn = tk.Button(self.frame_kanan, text="Shikkaku", font=("Arial", 12, "bold"), width=10, bg='black', fg='white', command=lambda: self.apply_penalty("Aka", "Shikkaku"))
        self.shikkaku_aka_btn.place(x=180, y=400)

        self.kikken_aka_btn = tk.Button(self.frame_kanan, text="Kikken", font=("Arial", 12, "bold"), width=10, bg='gray', fg='white', command=lambda: self.apply_penalty("Aka", "Kikken"))
        self.kikken_aka_btn.place(x=360, y=400)


    def update_score(self, team, delta):
        self.score_manager.update_score(team, delta)
        if team == "Ao":
            self.ao_score_var.set(self.score_manager.ao_score)
        elif team == "Aka":
            self.aka_score_var.set(self.score_manager.aka_score)

    def create_bottom_frame(self):
        self.stopwatch_btn = tk.Button(self.frame_bawah, text="Start", command=self.toggle_stopwatch)
        self.stopwatch_btn.place(x=100, y=25)

        self.done_btn = tk.Button(self.frame_bawah, text="Done", bg='lightgreen', command=self.done_match)
        self.done_btn.place(x=550, y=25)
        
        self.reset_btn = tk.Button(self.frame_bawah, text="Reset", bg='tomato', command=self.reset_app)
        self.reset_btn.place(x=1000, y=25)
        self.toggle_stopwatch_btn = tk.Button(self.frame_bawah, text="Hide Stopwatch", command=self.toggle_stopwatch_display)
        self.toggle_stopwatch_btn.place(x=250, y=25)

    
    def done_match(self):
        if not self.ao_locked or not self.aka_locked or not self.division_locked:
            messagebox.showwarning("Data Belum Lengkap", "Silakan isi nama Ao, Aka, dan pilih divisi terlebih dahulu.")
            return

        if self.stopwatch_running:
            self.stopwatch_running = False
            if self.stopwatch_job:
                self.root.after_cancel(self.stopwatch_job)
            self.stopwatch_btn.config(text="Start")

        match_data = MatchData(
            division=self.division_var.get(),
            ao_name=self.ao_name_var.get(),
            aka_name=self.aka_name_var.get(),
            ao_score=self.score_manager.ao_score,
            aka_score=self.score_manager.aka_score,
            ao_status=self.score_manager.ao_status,
            aka_status=self.score_manager.aka_status,
            time_elapsed=self.format_time(self.stopwatch_seconds)
        )
        CSVLogger().log_match(match_data)

        for btn in [self.ao_plus_btn, self.ao_minus_btn, self.aka_plus_btn, self.aka_minus_btn,
                    self.shikkaku_ao_btn, self.kikken_ao_btn,
                    self.shikkaku_aka_btn, self.kikken_aka_btn]:
            btn.config(state="disabled")

        self.stopwatch_btn.config(state="disabled")
        self.done_btn.config(state="disabled")
        self.reset_btn.config(state="normal")

    def reset_app(self):
        self.ao_locked = False
        self.aka_locked = False
        self.division_locked = False

        for widget in self.frame_atas.winfo_children():
            if isinstance(widget, tk.Label) and widget.cget("text") == self.ao_name_var.get():
                widget.destroy()
        self.ao_name_var.set("")
        self.ao_name_entry = tk.Entry(self.frame_atas, textvariable=self.ao_name_var, width=20)
        self.ao_name_entry.place(x=50, y=30)
        self.ao_name_entry.bind("<Return>", self.lock_ao_name)

        for widget in self.frame_atas.winfo_children():
            if isinstance(widget, tk.Label) and widget.cget("text") == self.aka_name_var.get():
                widget.destroy()
        self.aka_name_var.set("")
        self.aka_name_entry = tk.Entry(self.frame_atas, textvariable=self.aka_name_var, width=20)
        self.aka_name_entry.place(x=900, y=30)
        self.aka_name_entry.bind("<Return>", self.lock_aka_name)

        self.division_combo.config(state="readonly")
        self.division_var.set("Perebutan Gelar")

        self.score_manager = ScoreManager()

        self.blue_flag_img = Image.open("blue.png").resize((180, 100)) #bendera biru placeholder
        self.blue_flag = ImageTk.PhotoImage(self.blue_flag_img)
        self.flag_label_ao.config(image=self.blue_flag)

        self.red_flag_img = Image.open("red.png").resize((180, 100)) #bendera biru placeholder
        self.red_flag = ImageTk.PhotoImage(self.red_flag_img)
        self.flag_label_aka.config(image=self.red_flag)

        self.flag_label_ao.config(image=self.blue_flag)
        self.flag_label_aka.config(image=self.red_flag)

        self.ao_score_var.set(0)
        self.aka_score_var.set(0)
        self.score_manager = ScoreManager()

        self.score_manager = ScoreManager()

        self.ao_score_var.set(0)
        self.aka_score_var.set(0)

        self.flag_label_ao.config(image=self.blue_flag)
        self.flag_label_aka.config(image=self.red_flag)

        if self.stopwatch_job:
            self.root.after_cancel(self.stopwatch_job)
        self.stopwatch_running = False
        self.stopwatch_seconds = 0
        self.stopwatch_label_ao.config(text="00:00")
        self.stopwatch_label_aka.config(text="00:00")
        self.stopwatch_btn.config(state="normal", text="Start")

        for btn in [self.ao_plus_btn, self.ao_minus_btn, self.aka_plus_btn, self.aka_minus_btn,
                    self.shikkaku_ao_btn, self.kikken_ao_btn,
                    self.shikkaku_aka_btn, self.kikken_aka_btn]:
            btn.config(state="normal")
        self.done_btn.config(state="normal")
    
    def kembali_main(self):
        self.frame_atas.place_forget()
        self.frame_kanan.place_forget()
        self.frame_kiri.place_forget()
        self.frame_bawah.place_forget()
        if self.back_callback:
            self.back_callback()
class AppTkinter:
    def __init__(self, root):
        self.root = root
        self.root.title("Kelompok 3")
        self.root.geometry("1280x720")

        self.root.resizable(False, False)

        self.background()
        self.frame_awal = tk.Frame(self.root, bg="", highlightthickness=0, bd=0)

        self.btn_masuk = tk.Button(self.root, text="Masuk", font=("Helvetica", 14), width=20, height=2, command=self.buka_karate)
        self.btn_masuk.place(relx=0.5, rely=0.45, anchor="center")

        self.btn_anggota = tk.Button(self.root, text="Anggota", font=("Helvetica", 14), width=20, height=2, command=self.tampilkan_anggota)
        self.btn_anggota.place(relx=0.5, rely=0.55, anchor="center")

        self.btn_menu = tk.Button(self.root, text="Keluar", font=("Helvetica", 14), width=20, height=2, command=self.keluar_aplikasi)
        self.btn_menu.place(relx=0.5, rely=0.65, anchor="center")

    def background(self):
        img = Image.open("bg.png") #background placeholder
        img = img.resize((1280, 720))
        self.bg_image = ImageTk.PhotoImage(img)
        self.bg_label = tk.Label(self.root, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    
    def buka_karate(self):
        self.frame_awal.place_forget()
        KarateApp(self.root, back_callback=self.tampilkan_menu)
    def tampilkan_menu(self):
        self.frame_awal.place(relx=0.5, rely=0.5, anchor="center")

    
    def tampilkan_anggota(self):
        self.frame_awal.place_forget()
        self.fkanan_anggota = tk.Frame(self.root, bg="white")
        self.fkanan_anggota.place(x=0, y=0, width=1280, height=720)

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

    def keluar_aplikasi(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AppTkinter(root)
    root.mainloop()
