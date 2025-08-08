# gui.py
import tkinter as tk

class SkinManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LoL Skin Sale Alarm")
        self.root.geometry("800x600")

        self.welcome_label = tk.Label(self.root, text="Willkommen zum LolSaleAlarm!", font=("Helvetica", 16))
        self.welcome_label.pack(pady=20)