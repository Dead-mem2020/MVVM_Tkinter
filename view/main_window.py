import tkinter as tk
from tkinter import ttk
from ui.car_table import CarTable

class MainWindow():
    """Hlavní okno aplikace"""
    
    def __init__(self):
        self.root = tk.Tk()
        self._configure_window()
        self._create_widgets()

    def _configure_window(self):
        """konfigurace hlavního okna"""
        self.root.title("🚗 Správa aut")
        self.root.geometry("900x500")
        self.root.minsize(600, 400)


    def _create_widgets(self):
        main_frame = ttk.Frame(self.root, padding=36)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # nadpis
        title = ttk.Label(
            main_frame,
            text = "🚘 Správa autobazaru 🚘",
            font = ("Segoe UI", 18, "bold"),
        )
        title.pack(pady=(0, 24))

        # tabulka aut
        table_frame = ttk.LabelFrame(main_frame, text = "Seznam_aut", padding = 10)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        self.table = CarTable(table_frame)
        self.table.pack(fill=tk.BOTH, expand = 10)

        # informační text
        info = ttk.Label(
            main_frame,
            text = ("Vyberte auto pro zobrazení detailů nebo úpravu"),
            font=("Seguo UI", 10)
        )
        info.pack(pady=(8, 0)) # odsazení od horní části

    def run(self):
        self.root.mainloop()