import tkinter as tk
from tkinter import ttk, messagebox, filedialog # Přidán filedialog
import json
import os

from ui.car_table import CarTable
from viewmodels.AddCarDialogue2 import CarDialog # Pozor na přejmenování třídy

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

        top = ttk.Frame(container)
        top.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(top, text="Seznam vozidel", font=("Arial", 14, "bold")).pack(side=tk.LEFT)
        
        # TLAČÍTKO PŘIDAT
        ttk.Button(top, text="+ Přidat auto", command=self._open_add_dialog).pack(side=tk.RIGHT, padx=5)
        
        # NOVÉ TLAČÍTKO KOUPIT
        ttk.Button(top, text="💰 Koupit vybrané", command=self._buy_car).pack(side=tk.RIGHT, padx=5)

        self.table = CarTable(container)
        self.table.pack(fill=tk.BOTH, expand=True)
        
        self.stats_label = ttk.Label(container, text="")
        self.stats_label.pack(pady=10)
        
        # PŘIDÁME TLAČÍTKO UPRAVIT
        ttk.Button(top, text="✏️ Upravit auto", command=self._open_edit_dialog).pack(side=tk.RIGHT, padx=5)
        
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
        dialog = CarDialog(self.root)
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

    def _buy_car(self):
        """ Logika pro nákup auta """
        car_id = self.table.get_selected_car_id()
        
        if car_id is None:
            messagebox.showwarning("Výběr", "Nejdříve vyberte auto v tabulce!")
            return

        # Najdeme data o autě v našem seznamu podle ID
        car_to_buy = next((car for car in self.cars_data if car["id"] == car_id), None)
        
        if car_to_buy:
            # Zeptáme se pro jistotu
            potvrzeni = messagebox.askyesno("Potvrzení", f"Opravdu chcete koupit {car_to_buy['brand']} {car_to_buy['model']}?")
            
            if potvrzeni:
                self._generate_invoice(car_to_buy) # 1. Vytvoří fakturu
                self._remove_car(car_id)           # 2. Odstraní z databáze
                messagebox.showinfo("Hotovo", "Auto bylo koupeno a faktura vygenerována.")

    def _remove_car(self, car_id):
        """ Odstraní auto ze seznamu a uloží JSON """
        self.cars_data = [car for car in self.cars_data if car["id"] != car_id]
        self._save_data()
        self._refresh_ui()

    def _generate_invoice(self, car):
        """ Vytvoří textový soubor jako fakturu """
        obsah_faktury = f"""
        ========================================
                   FAKTURA - AUTOBAZAR
        ========================================
        ID Vozidla:  {car['id']}
        Značka:      {car['brand']}
        Model:       {car['model']}
        Rok výroby:  {car['year']}
        Barva:       {car['colour']}
        Najeto:      {car['mileage']} km
        ----------------------------------------
        CELKOVÁ CENA: {car['price']:,} Kč
        ----------------------------------------
        Děkujeme za váš nákup!
        ========================================
        """
        
        # Otevře okno pro výběr místa uložení
        soubor = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Textové soubory", "*.txt")],
            initialfile=f"Faktura_{car['brand']}_{car['model']}.txt",
            title="Uložit fakturu jako..."
        )
        
        if soubor:
            with open(soubor, "w", encoding="utf-8") as f:
                f.write(obsah_faktury)

    def _refresh_ui(self):
        """ Znovu načte tabulku a statistiky """
        self.table.refresh(self.cars_data)
        total = sum(car["price"] for car in self.cars_data)
        self.stats_label.config(text=f"Celkem aut: {len(self.cars_data)} | Hodnota: {total:,} Kč")


    def _open_add_dialog(self):
        """ Otevření dialogu pro nové auto (bez dat) """
        dialog = CarDialog(self.root)
        self.root.wait_window(dialog)
        if dialog.result:
            self._add_car(dialog.result)

    def _open_edit_dialog(self):
        """ Otevření dialogu pro úpravu (s daty vybraného auta) """
        car_id = self.table.get_selected_car_id()
        if car_id is None:
            messagebox.showwarning("Výběr", "Vyberte auto, které chcete upravit.")
            return

        # Najdeme auto podle ID
        car_to_edit = next((c for c in self.cars_data if c["id"] == car_id), None)
        
        dialog = CarDialog(self.root, car_to_edit=car_to_edit)
        self.root.wait_window(dialog)

        if dialog.result:
            self._update_car(dialog.result)

    def _update_car(self, updated_car):
        """ Najde staré auto v seznamu a nahradí ho novým """
        for i, car in enumerate(self.cars_data):
            if car["id"] == updated_car["id"]:
                self.cars_data[i] = updated_car
                break
        
        self._save_data()
        self._refresh_ui()

    def _add_car(self, new_car):
        """ Logika přidání (stejná jako minule) """
        new_id = max([c["id"] for c in self.cars_data], default=0) + 1
        new_car["id"] = new_id
        self.cars_data.append(new_car)
        self._save_data()
        self._refresh_ui()

    def run(self):
        self.root.mainloop()