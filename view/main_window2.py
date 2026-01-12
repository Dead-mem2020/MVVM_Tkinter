import tkinter as tk
from tkinter import ttk
import json
import os

# Importy tvých tříd
from ui.car_table import CarTable
from viewmodels.AddCarDialogue2 import AddCarDialog

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🚗 Správa Autobazaru")
        self.root.geometry("800x500")
        
        self.file_path = "data/cars.json"
        self.cars_data = [] # Data v paměti

        self._create_widgets()
        self._load_data() # Načte JSON při startu

    def _create_widgets(self):
        container = ttk.Frame(self.root, padding=20)
        container.pack(fill=tk.BOTH, expand=True)

        # Horní lišta s tlačítkem
        top = ttk.Frame(container)
        top.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(top, text="Seznam vozidel", font=("Arial", 14, "bold")).pack(side=tk.LEFT)
        ttk.Button(top, text="+ Přidat auto", command=self._open_add_dialog).pack(side=tk.RIGHT)

        # Tabulka
        self.table = CarTable(container)
        self.table.pack(fill=tk.BOTH, expand=True)

    def _load_data(self):
        """ Načte data ze souboru do self.cars_data """
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    self.cars_data = json.load(f)
            except: self.cars_data = []
        self.table.refresh(self.cars_data)

    def _save_data(self):
        """ Uloží self.cars_data do JSON souboru """
        # Vytvoří složku 'data', pokud neexistuje
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.cars_data, f, indent=4, ensure_ascii=False)

    def _open_add_dialog(self):
        dialog = AddCarDialog(self.root)
        self.root.wait_window(dialog) # Čeká na zavření okna

        if dialog.result:
            # AUTO-INCREMENT ID
            if not self.cars_data:
                new_id = 1
            else:
                new_id = max(car["id"] for car in self.cars_data) + 1
            
            dialog.result["id"] = new_id
            self.cars_data.append(dialog.result)
            
            self._save_data() # Uloží do JSONu
            self.table.refresh(self.cars_data) # Překreslí tabulku

    def run(self):
        self.root.mainloop()