import tkinter as tk
from gui import SkinManagerApp
from data_fetcher import get_latest_ddragon_version, get_all_skins

if __name__ == "__main__":
    print("Starte Anwendung...")
    print("Lade Skin-Daten...")
    version = get_latest_ddragon_version()

    all_skins_list = get_all_skins(version)
    print("Skin-Daten geladen.")

    root = tk.Tk()
    app = SkinManagerApp(root, all_skins_list)
    
    root.mainloop()