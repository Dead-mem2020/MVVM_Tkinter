import tkinter as tk
from tkinter import ttk

class CarTable(ttk.Frame):
    COLUMNS = ("id", "brand", "model", "year", "price", "colour", "mileage")
    COLUMNS_NAME = { #Python - klíč/key
        "id": "ID",
        "brand": "Značka",
        "year": "Rok",
        "price": "Cena (Kč)",
        "colour": "Barva",
        "mileage": "Najeto (km)"
    }

    def __init__(self, parent):
        super().__init__(parent)
        self._create_widgets()
        
    def _create_widgets(self):
        """Vytvoří tabulku a scrollbar"""
        style = ttk.Style()
        style.configure("Treeview", rowheight=30, font=("Seguo UI", 10)) # řádka v tabulce
        style.configure("Treeview.Heading", font=("Segue UI", 10, "bold")) # záhlaví #tupple

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

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


    def _configure_columns(self):
        """Nastavení hlavičky sloupců a jejich šířky"""
        column_width = {
            "id": 50, "brand": 100, "model":100, 
            "year": 70, "price": 100, "colour": 100, 
            "mileage": 100
        }

        for col in self.COLUMNS:
            self.tree.heading(col, text=self.COLUMNS_NAME[col])
            self.tree.column(col, width=column_width[col], anchor=tk.CENTER)