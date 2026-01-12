import tkinter as tk
from tkinter import ttk

class CarTable(ttk.Frame):
    COLUMNS = ("id", "brand", "model", "year", "price", "colour", "mileage")
    COLUMNS_NAME = {
        "id": "ID",
        "brand": "Značka",
        "model": "Model",
        "year": "Rok",
        "price": "Cena (Kč)",
        "colour": "Barva",
        "mileage": "Najeto (km)"
    }

    def __init__(self, parent):
        super().__init__(parent)
        self._create_widgets()

    def _create_widgets(self):
        """ Vytvoří tabulku a scrollbar """
        style = ttk.Style() # https://docs.python.org/3/library/tkinter.ttk.html
        style.configure("Treeview", rowheight=30, font=("Segoe UI", 10)) # Řádka v tabulce
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold")) # Záhlavý

        # Vytváření tabulky
        self.tree = ttk.Treeview(
            self,
            columns=self.COLUMNS,
            show="headings",
            selectmode="browse"
        )

        #Scrollbar
        self.scrollbar = ttk.Scrollbar(
            self,
            orient=tk.VERTICAL,
            command=self.tree.yview
        )

        # Rozmístění
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self._configure_columns()

    def _configure_columns(self):
        """ Nastavení hlavičky sloupců a jejich šířky """
        column_widths = {
            "id": 50, "brand": 100, "model": 100,
            "year": 70, "price": 100, "colour": 100, 
            "mileage": 100}
        
        for col in self.COLUMNS:
            self.tree.heading(col, text=self.COLUMNS_NAME[col])
            self.tree.column(col, width=column_widths[col], anchor=tk.CENTER)


    def refresh(self, cars_data: list):
        """ Obnoví data v tabulce"""

        for item in self.tree.get_children():
            self.tree.delete(item)

        for car in cars_data:  # <-- OPRAVA: bylo "self.tree.get_children()"
            values = (
                car["id"],
                car["brand"],
                car["model"],
                car["year"],
                car["price"],
                car["colour"],
                car["mileage"]
            )
            self.tree.insert("", tk.END, values=values)

    def get_selected_car_id(self):
        """ Vrátí ID vybraného auta v tabulce, nebo None, pokud není nic vybráno """
        selected_item = self.tree.selection() # Získá označený řádek
        if not selected_item:
            return None
        
        # Získáme hodnoty z řádku (ID je v prvním sloupci - index 0)
        values = self.tree.item(selected_item)['values']
        return values[0] # Vracíme ID