import tkinter as tk
from tkinter import ttk, messagebox

class AddCarDialogue(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Přidat nové auto")
        self.geometry("300x450")
        self.result = None  # Sem uložíme data, pokud uživatel klikne na 'Uložit'

        # Modální okno (vynutí pozornost na toto okno)
        self.transient(parent)
        self.grab_set()

        self._create_widgets()

    def _create_widgets(self):
        """ Vytvoří vstupní pole formuláře """
        container = ttk.Frame(self, padding=20)
        container.pack(fill=tk.BOTH, expand=True)

        # Definice polí (Label + Entry)
        fields = [
            ("Značka", "brand"),
            ("Model", "model"),
            ("Rok", "year"),
            ("Cena (Kč)", "price"),
            ("Barva", "colour"),
            ("Najeto (km)", "mileage")
        ]

        self.entries = {}
        for label_text, attr in fields:
            ttk.Label(container, text=label_text).pack(anchor=tk.W, pady=(5, 0))
            entry = ttk.Entry(container)
            entry.pack(fill=tk.X, pady=(0, 5))
            self.entries[attr] = entry

        # Tlačítko pro potvrzení
        ttk.Button(container, text="Uložit auto", command=self._on_save).pack(pady=20)

    def _on_save(self):
        """ Validace a předání dat zpět do hlavního okna """
        try:
            # Převedeme texty na správné datové typy
            self.result = {
                "brand": self.entries["brand"].get(),
                "model": self.entries["model"].get(),
                "year": int(self.entries["year"].get()),
                "price": int(self.entries["price"].get()),
                "colour": self.entries["colour"].get(),
                "mileage": int(self.entries["mileage"].get())
            }
            self.destroy() # Zavře okno
        except ValueError:
            messagebox.showerror("Chyba", "Rok, Cena a Najeto musí být čísla!")