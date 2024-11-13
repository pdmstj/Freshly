#장바구니
import tkinter as tk
from tkinter import messagebox
from ingredient_table import IngredientTable


class Cart:
    def __init__(self, parent):
        self.frame = tk.Frame(parent)

        IngredientTable(self.frame)

        tk.Button(self.frame, text="추가", command=self.add_to_cart, width=10).pack(
            side="left", padx=5, pady=20
        )
        tk.Button(
            self.frame, text="삭제", command=self.remove_from_cart, width=10
        ).pack(side="right", padx=5, pady=20)

    def add_to_cart(self):
        messagebox.showinfo("장바구니", "장바구니에 추가되었습니다!")

    def remove_from_cart(self):
        messagebox.showinfo("장바구니", "장바구니에서 삭제되었습니다!")
