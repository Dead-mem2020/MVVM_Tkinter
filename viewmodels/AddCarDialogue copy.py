import tkinter as tk
from tkinter import ttk, messagebox

class AddCarDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Nový záznam")
        self.geometry("300x400")
        self.result = None # Sem se uloží data po kliknutí na uložit

        # Zablokuje hlavní okno, dokud se toto nezavře
        self.transient(parent)
        self.grab_set()

        self._create_widgets()

    def _create_widgets(self):
        frame = ttk.Frame(self, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        # Seznam polí k vyplnění
        self.entries = {}
        fields = [("Značka", "brand"), ("Model", "model"), ("Rok", "year"), 
                  ("Cena", "price"), ("Barva", "colour"), ("Najeto", "mileage")]

        for label_text, key in fields:
            ttk.Label(frame, text=label_text).pack(anchor="w")
            entry = ttk.Entry(frame)
            entry.pack(fill="x", pady=(0, 10))
            self.entries[key] = entry

        ttk.Button(frame, text="Uložit", command=self._save).pack(pady=10)

    def _save(self):
        try:
            self.result = {
                "brand": self.entries["brand"].get(),
                "model": self.entries["model"].get(),
                "year": int(self.entries["year"].get()),
                "price": int(self.entries["price"].get()),
                "colour": self.entries["colour"].get(),
                "mileage": int(self.entries["mileage"].get())
            }
            self.destroy()
        except ValueError:
            messagebox.showerror("Chyba", "Rok, Cena a Najeto musí být čísla!")