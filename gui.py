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
        self.skin_listbox = Listbox(self.list_frame, selectmode=tk.MULTIPLE)
        self.skin_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar = Scrollbar(self.list_frame, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.skin_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.skin_listbox.yview)

        self.bottom_frame = Frame(self.root)
        self.bottom_frame.pack(pady=10, padx=10, fill=tk.X)
        self.save_button = Button(self.bottom_frame, text="Wunschliste speichern", command=self.save_wishlist)
        self.save_button.pack(side=tk.LEFT)
        self.status_label = Label(self.bottom_frame, text="", fg="green")
        self.status_label.pack(side=tk.LEFT, padx=(10, 0))

        self.populate_list(self.all_skins)

    def save_wishlist(self):
        print("Speichere Wunschliste...")
        selected_indices = self.skin_listbox.curselection()
        selected_skins = [self.skin_listbox.get(i) for i in selected_indices]
        try:
            with open('wished_skins.txt', 'w', encoding='utf-8') as f:
                for skin in selected_skins:
                    f.write(f"{skin}\n")
            status_message = f"{len(selected_skins)} Skins in der Wunschliste gespeichert."
            self.status_label.config(text=status_message)
            print(status_message)
        except IOError as e:
            error_message = "Fehler beim Speichern der Datei!"
            self.status_label.config(text=error_message, fg="red")
            print(f"{error_message}: {e}")

    def populate_list(self, skin_list):
        self.skin_listbox.delete(0, tk.END)
        for skin in skin_list:
            self.skin_listbox.insert(tk.END, skin)

    def update_list(self, event=None):
        self.status_label.config(text="")
        search_term = self.search_entry.get().lower()
        if not search_term:
            filtered_skins = self.all_skins
        else:
            filtered_skins = [skin for skin in self.all_skins if search_term in skin.lower()]
        self.populate_list(filtered_skins)