#삭제버튼
import tkinter as tk
from ingredient_table import IngredientTable


class RoomTemp:
    def __init__(self, parent):
        self.frame = tk.Frame(parent)
        self.ingredient_table = IngredientTable(self.frame)

        # 재료 삭제 버튼 추가
        delete_button = tk.Button(
            self.frame,
            text="재료 삭제",
            command=self.ingredient_table.remove_ingredient,
        )
        delete_button.pack(pady=5)
