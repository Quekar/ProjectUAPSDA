import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk 

class AppTkinter:
    def __init__(self, root):
        self.root = root
        self.root.title("Lorem Ipsum")
        self.root.geometry("1280x720")
        self.root.resizeable(False, False)

if __name__ == "__main__":
    root = tk.Tk()
    app = AppTkinter(root)
    root.mainloop()
