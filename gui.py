# gui.py

import tkinter as tk
from tkinter import Listbox, Scrollbar, Entry, Frame, Label, Button
from data_fetcher import get_latest_ddragon_version, get_all_skins

class SkinManagerApp:
    def __init__(self, root):
        self.root = root
        
        print("Lade Skin-Daten für die GUI...")
        version = get_latest_ddragon_version()
        self.all_skins = get_all_skins(version)
        print("Skin-Daten geladen.")
        
        self.selected_skins = set()

        self.root.title("LoL Skin Sale Alarm - Konfiguration")
        self.root.geometry("800x600")

        self.search_frame = Frame(self.root)
        self.search_frame.pack(pady=10, padx=10, fill=tk.X)
        self.search_label = Label(self.search_frame, text="Suche nach Skin:")
        self.search_label.pack(side=tk.LEFT, padx=(0, 5))
        self.search_entry = Entry(self.search_frame)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.search_entry.bind("<KeyRelease>", self.update_list)
        
        self.list_frame = Frame(self.root)
        self.list_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        self.skin_listbox = Listbox(
            self.list_frame, 
            selectmode=tk.SINGLE,
            selectbackground='white',
            selectforeground='black',
            highlightthickness=0,
            activestyle='none',
            exportselection=False
        )
        self.skin_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.skin_listbox.bind("<Button-1>", self.on_skin_click)
        
        self.scrollbar = Scrollbar(self.list_frame, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.skin_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.skin_listbox.yview)

        self.bottom_frame = Frame(self.root)
        self.bottom_frame.pack(pady=10, padx=10, fill=tk.X)
        self.save_button = Button(self.bottom_frame, text="Wunschliste speichern & Schließen", command=self.save_and_close)
        self.save_button.pack(side=tk.LEFT)

        self.counter_label = Label(self.bottom_frame, text="Ausgewählt: 0", font=("Helvetica", 10))
        self.counter_label.pack(side=tk.LEFT, padx=(10, 0))

        self.status_label = Label(self.bottom_frame, text="", fg="green")
        self.status_label.pack(side=tk.LEFT, padx=(10, 0))

        self.load_initial_wishlist()
        self.populate_list(self.all_skins)

    def load_initial_wishlist(self):
        try:
            with open('wished_skins.txt', 'r', encoding='utf-8') as f:
                self.selected_skins = {line.strip() for line in f if line.strip()}
            print(f"{len(self.selected_skins)} Skins aus bestehender Wunschliste geladen.")
        except FileNotFoundError:
            print("Keine bestehende Wunschliste gefunden.")
        self.update_counter()
        
    def on_skin_click(self, event):
        try:
            index = self.skin_listbox.nearest(event.y)
            clicked_skin = self.skin_listbox.get(index)
        except (tk.TclError, IndexError):
            return "break"

        if clicked_skin in self.selected_skins:
            self.selected_skins.remove(clicked_skin)
            self.skin_listbox.itemconfig(index, {'bg': 'white', 'fg': 'black'})
        else:
            self.selected_skins.add(clicked_skin)
            self.skin_listbox.itemconfig(index, {'bg': 'lightblue', 'fg': 'black'})
        
        self.update_counter()
        
        return "break"

    def update_counter(self):
        count = len(self.selected_skins)
        self.counter_label.config(text=f"Ausgewählt: {count}")

    def update_selection_highlight(self):
        for i in range(self.skin_listbox.size()):
            skin_name = self.skin_listbox.get(i)
            if skin_name in self.selected_skins:
                self.skin_listbox.itemconfig(i, {'bg': 'lightblue', 'fg': 'black'})
            else:
                self.skin_listbox.itemconfig(i, {'bg': 'white', 'fg': 'black'})

    def save_and_close(self):
        print("Speichere Wunschliste...")
        try:
            with open('wished_skins.txt', 'w', encoding='utf-8') as f:
                for skin in sorted(list(self.selected_skins)):
                    f.write(f"{skin}\n")
            print(f"{len(self.selected_skins)} Skins in der Wunschliste gespeichert.")
            self.root.destroy()
        except IOError as e:
            print(f"Fehler beim Speichern der Datei!: {e}")

    def populate_list(self, skin_list):
        self.skin_listbox.selection_clear(0, tk.END)
        self.skin_listbox.delete(0, tk.END)
        for skin in skin_list:
            self.skin_listbox.insert(tk.END, skin)
        self.update_selection_highlight()

    def update_list(self, event=None):
        self.status_label.config(text="")
        search_term = self.search_entry.get().lower()
        if not search_term:
            filtered_skins = self.all_skins
        else:
            filtered_skins = [skin for skin in self.all_skins if search_term in skin.lower()]
        
        self.populate_list(filtered_skins)