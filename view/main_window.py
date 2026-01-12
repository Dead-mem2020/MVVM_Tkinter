import tkinter as tk
from tkinter import ttk
from ui.car_table import CarTable
from viewmodels.AddCarDialogue2 import AddCarDialogue
# Předpokládáme: from ui.car_table import CarTable
# Předpokládáme: from ui.add_car_dialog import AddCarDialog

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        # DOČASNÁ DATA (v paměti)
        self.cars_data = [] 
        
        self._configure_window()
        self._create_widgets()
    
    def _configure_window(self):
        self.root.title("🚗 Správa Aut")
        self.root.geometry("900x550")
    
    def _create_widgets(self):
        main_frame = ttk.Frame(self.root, padding=36)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Horní panel s nadpisem a tlačítkem
        header = ttk.Frame(main_frame)
        header.pack(fill=tk.X, pady=(0, 20))

        ttk.Label(header, text="Správa autobazaru", font=("Segoe UI", 18, "bold")).pack(side=tk.LEFT)
        
        # TLAČÍTKO PRO PŘIDÁNÍ
        btn_add = ttk.Button(header, text="+ Přidat auto", command=self._open_add_dialog)
        btn_add.pack(side=tk.RIGHT)

        # Tabulka
        self.table = CarTable(main_frame)
        self.table.pack(fill=tk.BOTH, expand=True)

        # Statistiky
        self.stats_label = ttk.Label(main_frame, text="Zatím nebyla přidána žádná auta.", font=("Segoe UI", 10))
        self.stats_label.pack(pady=(10, 0))

    def _open_add_dialog(self):
        """ Otevře okno pro přidání a zpracuje výsledek """
        dialog = AddCarDialogue(self.root)
        self.root.wait_window(dialog) # Program zde počká, než se okno zavře

        if dialog.result:
            self._add_car_to_list(dialog.result)

    def _add_car_to_list(self, car_dict):
        """ Logika pro Auto-increment a přidání do UI """
        
        # AUTO-INCREMENT ID
        if not self.cars_data:
            new_id = 1
        else:
            new_id = max(car["id"] for car in self.cars_data) + 1
        
        car_dict["id"] = new_id
        
        # Přidání do našeho seznamu v paměti
        self.cars_data.append(car_dict)
        
        # Refresh UI (Tabulka + Statistiky)
        self.table.refresh(self.cars_data)
        self._update_stats()

    def _update_stats(self):
        total_value = sum(car["price"] for car in self.cars_data)
        self.stats_label.configure(
            text=f"Počet vozidel: {len(self.cars_data)} | Celková hodnota: {total_value} Kč"
        )

    def run(self):
        self.root.mainloop()