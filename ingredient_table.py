#식재료 추가
import tkinter as tk
from tkinter import ttk


class IngredientTable:
    def __init__(self, parent):
        self.tree = ttk.Treeview(
            parent, columns=("재료명", "구매일자", "유통기한"), show="headings"
        )
        self.tree.heading("재료명", text="재료명")
        self.tree.heading("구매일자", text="구매일자")
        self.tree.heading("유통기한", text="유통기한")
        self.tree.pack(fill="both", expand=True)

    def add_ingredient(self, name, purchase_date, expiration_date):
        self.tree.insert("", "end", values=(name, purchase_date, expiration_date))

    def remove_ingredient(self):
        selected_item = self.tree.selection()
        for item in selected_item:
            self.tree.delete(item)
