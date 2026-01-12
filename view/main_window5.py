import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os

from ui.car_table import CarTable
from viewmodels.AddCarDialogue2 import CarDialog

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🚗 Správa Autobazaru v2.0")
        self.root.geometry("950x600")
        
        # Cesty k souborům
        self.file_path = "data/cars.json"
        self.sold_file_path = "data/sold_cars.json"
        
        # Data v paměti
        self.cars_data = []      # Dostupná auta
        self.sold_cars_data = [] # Koupená auta

        self._create_widgets()
        self._load_all_data()

    def _create_widgets(self):
        # Notebook vytvoří záložky
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # --- ZÁLOŽKA 1: AKTUÁLNÍ NABÍDKA ---
        self.tab_available = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.tab_available, text=" 🛒 Aktuální nabídka ")
        
        # Horní lišta pro Nabídku
        top_bar = ttk.Frame(self.tab_available)
        top_bar.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(top_bar, text="+ Přidat nové", command=self._open_add_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_bar, text="✏️ Upravit", command=self._open_edit_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_bar, text="💰 KOUPIT AUTO", command=self._buy_car).pack(side=tk.RIGHT, padx=5)

        self.table = CarTable(self.tab_available)
        self.table.pack(fill=tk.BOTH, expand=True)
        
        self.stats_label = ttk.Label(self.tab_available, text="")
        self.stats_label.pack(pady=5)

        # --- ZÁLOŽKA 2: PRODANÁ AUTA ---
        self.tab_sold = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.tab_sold, text=" ✅ Historie prodejů ")

        ttk.Label(self.tab_sold, text="Seznam vozů, které již byly prodány:", font=("Arial", 10, "italic")).pack(pady=(0,10))

        # Znovu použijeme CarTable pro prodaná auta!
        self.sold_table = CarTable(self.tab_sold)
        self.sold_table.pack(fill=tk.BOTH, expand=True)

    def _load_all_data(self):
        """ Načte data pro obě tabulky """
        # Načtení dostupné nabídky
        if os.path.exists(self.sold_file_path):
            with open(self.sold_file_path, "r", encoding="utf-8") as f:
                self.sold_cars_data = json.load(f)
        
        # Načtení prodaných aut
        if os.path.exists(self.sold_file_path):
            with open(self.sold_file_path, "r", encoding="utf-8") as f:
                self.sold_cars_data = json.load(f)
        
        self._refresh_ui()

    def _save_all_data(self):
        """ Uloží oba seznamy do jejich JSON souborů """
        os.makedirs("data", exist_ok=True)
        
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.cars_data, f, indent=4, ensure_ascii=False)
            
        with open(self.sold_file_path, "w", encoding="utf-8") as f:
            json.dump(self.sold_cars_data, f, indent=4, ensure_ascii=False)

    def _buy_car(self):
        """ Přesune auto z nabídky do prodaných """
        car_id = self.table.get_selected_car_id()
        if car_id is None:
            messagebox.showwarning("Výběr", "Vyberte auto, které chcete koupit.")
            return

        car_to_buy = next((c for c in self.cars_data if c["id"] == car_id), None)
        
        if car_to_buy and messagebox.askyesno("Koupit", f"Chcete zakoupit {car_to_buy['brand']} {car_to_buy['model']}?"):
            # 1. Generování faktury
            self._generate_invoice(car_to_buy)
            
            # 2. PŘESUN DAT: Vyjmeme z nabídky a dáme do prodaných
            self.cars_data = [c for c in self.cars_data if c["id"] != car_id]
            self.sold_cars_data.append(car_to_buy)

            print(f"DEBUG: V historii je nyní {len(self.sold_cars_data)} aut.")
            
            # 3. Uložení a refresh
            self._save_all_data()
            self._refresh_ui()
            messagebox.showinfo("Úspěch", "Auto bylo přesunuto do historie prodejů.")

    def _refresh_ui(self):
        """ Obnoví obě tabulky a statistiky """
        self.table.refresh(self.cars_data)
        self.sold_table.refresh(self.sold_cars_data)
        
        total = sum(car["price"] for car in self.cars_data)
        self.stats_label.config(text=f"Aktuálně v nabídce: {len(self.cars_data)} aut | Hodnota: {total:,} Kč")

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
        """ Hlavní logika nákupu a přesunu do historie """
        car_id = self.table.get_selected_car_id()
        if car_id is None:
            messagebox.showwarning("Výběr", "Nejdříve vyberte auto v tabulce!")
            return

        # 1. Najdeme auto v aktuální nabídce
        car_to_buy = next((car for car in self.cars_data if car["id"] == car_id), None)
        
        if car_to_buy:
            if messagebox.askyesno("Potvrzení", f"Opravdu chcete koupit {car_to_buy['brand']} {car_to_buy['model']}?"):
                # 2. Generování faktury
                self._generate_invoice(car_to_buy)

                # 3. Přesun v paměti: smažeme z nabídky, přidáme do prodaných
                self.cars_data = [c for c in self.cars_data if c["id"] != car_id]
                self.sold_cars_data.append(car_to_buy)
                
                # 4. Uložení obou souborů (POZOR: voláme správný název!)
                self._save_all_data()
                
                # 5. Aktualizace tabulek na obrazovce
                self._refresh_ui()
                messagebox.showinfo("Hotovo", "Auto bylo prodáno a přesunuto do historie.")

    
    def _remove_car(self, car_id):
        """ Tato metoda už jen maže auto (bez přesunu do historie) """
        self.cars_data = [car for car in self.cars_data if car["id"] != car_id]
        self._save_all_data() # Opravený název
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
        
        self._save_all_data()
        self._refresh_ui()

    def _add_car(self, new_car):
        """ Logika přidání (stejná jako minule) """
        new_id = max([c["id"] for c in self.cars_data], default=0) + 1
        new_car["id"] = new_id
        self.cars_data.append(new_car)
        self._save_all_data()
        self._refresh_ui()

    
    def _open_add_dialog(self):
        dialog = CarDialog(self.root)
        self.root.wait_window(dialog)
        if dialog.result:
            self._add_car(dialog.result)

    def _add_car(self, new_car):
        new_id = max([c["id"] for c in self.cars_data] + [c["id"] for c in self.sold_cars_data], default=0) + 1
        new_car["id"] = new_id
        self.cars_data.append(new_car)
        self._save_all_data()
        self._refresh_ui()

    def _open_edit_dialog(self):
        car_id = self.table.get_selected_car_id()
        if car_id is None:
            messagebox.showwarning("Výběr", "Vyberte auto z nabídky k úpravě.")
            return
        car_to_edit = next((c for c in self.cars_data if c["id"] == car_id), None)
        dialog = CarDialog(self.root, car_to_edit=car_to_edit)
        self.root.wait_window(dialog)
        if dialog.result:
            self._update_car(dialog.result)

    def _update_car(self, updated_car):
        for i, car in enumerate(self.cars_data):
            if car["id"] == updated_car["id"]:
                self.cars_data[i] = updated_car
                break
        self._save_all_data()
        self._refresh_ui()

    def _generate_invoice(self, car):
        obsah = f"FAKTURA\nAuto: {car['brand']} {car['model']}\nCena: {car['price']} Kč"
        soubor = filedialog.asksaveasfilename(defaultextension=".txt", initialfile=f"Faktura_{car['id']}.txt")
        if soubor:
            with open(soubor, "w", encoding="utf-8") as f: f.write(obsah)

    def run(self):
        self.root.mainloop()