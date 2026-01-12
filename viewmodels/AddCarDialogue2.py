import tkinter as tk
from tkinter import ttk, messagebox

class CarDialog(tk.Toplevel):
    # Přejmenovali jsme z AddCarDialog na CarDialog, protože teď i upravuje
    def __init__(self, parent, car_to_edit=None):
        super().__init__(parent)
        self.title("Upravit auto" if car_to_edit else "Nové auto")
        self.geometry("300x450")
        self.result = None
        self.car_to_edit = car_to_edit # Pokud je zde objekt, jsme v režimu úprav

        self.transient(parent)
        self.grab_set()

        self._create_widgets()
        
        # Pokud upravujeme, vyplníme políčka stávajícími daty
        if car_to_edit:
            self._populate_fields(car_to_edit)

    def _create_widgets(self):
        frame = ttk.Frame(self, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        self.entries = {}
        fields = [("Značka", "brand"), ("Model", "model"), ("Rok", "year"), 
                  ("Cena", "price"), ("Barva", "colour"), ("Najeto", "mileage")]

        for label_text, key in fields:
            ttk.Label(frame, text=label_text).pack(anchor="w")
            entry = ttk.Entry(frame)
            entry.pack(fill="x", pady=(0, 10))
            self.entries[key] = entry

        btn_text = "Uložit změny" if self.car_to_edit else "Přidat auto"
        ttk.Button(frame, text=btn_text, command=self._validate_and_save).pack(pady=10)

    def _populate_fields(self, car):
        """ Vyplní políčka daty z existujícího auta """
        for key, value in car.items():
            if key in self.entries:
                self.entries[key].insert(0, str(value))

    def _validate_and_save(self):
        """ VALIDACE DAT """
        try:
            # 1. Kontrola prázdných polí
            for key, entry in self.entries.items():
                if not entry.get().strip():
                    messagebox.showwarning("Chyba", f"Pole {key} nesmí být prázdné!")
                    return

            # 2. Sběr dat a úprava textu (Velká písmena)
            # .strip() odstraní mezery na začátku a konci
            # .title() udělá první písmeno velké (Škoda, Octavia)
            # .upper() udělá vše velkým (pro SPZ nebo značky, pokud chceš)
            brand = self.entries["brand"].get().strip().title()
            model = self.entries["model"].get().strip().capitalize()
            colour = self.entries["colour"].get().strip().lower()

            # 3. Převod na čísla a kontrola záporných hodnot
            year = int(self.entries["year"].get())
            price = int(self.entries["price"].get())
            mileage = int(self.entries["mileage"].get())

            if year < 1886 or price < 0 or mileage < 0:
                raise ValueError("Nereálné hodnoty")

            self.result = {
                "brand": brand,
                "model": model,
                "year": year,
                "price": price,
                "colour": colour,
                "mileage": mileage
            }
            
            # Pokud upravujeme, zachováme původní ID
            if self.car_to_edit:
                self.result["id"] = self.car_to_edit["id"]

            self.destroy()

        except ValueError:
            messagebox.showerror("Chyba", "Zadejte platná čísla (Rok, Cena, Najeto)!")