import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import csv
import os

class MatchData:
    def _init_(self, division, ao_name, aka_name, ao_score, aka_score, ao_status, aka_status, time_elapsed):
        self.division = division
        self.ao_name = ao_name
        self.aka_name = aka_name
        self.ao_score = ao_score
        self.aka_score = aka_score
        self.ao_status = ao_status
        self.aka_status = aka_status
        self.time_elapsed = time_elapsed

class CSVLogger:
    def _init_(self, filename='karate_scores.csv'):
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
    def _init_(self):
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
    def _init_(self, root, back_callback=None):
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
