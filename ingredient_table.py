# 식재료 추가
import tkinter as tk
from tkinter import ttk


class IngredientTable:
    def __init__(self, parent):
        self.frame = tk.Frame(parent)
        self.table = tk.Listbox(self.frame)
        self.table.pack(fill="both", expand=True)

        self.selected_ingredient_id = None  # 선택된 재료의 ID

        self.load_ingredients()

    def load_ingredients(self):
        """DB에서 재료 목록을 불러와서 테이블에 표시합니다."""
        connection = connect_to_freshlydb()
        cursor = connection.cursor()
        cursor.execute("SELECT id, name FROM ingredients")
        ingredients = cursor.fetchall()

        for ingredient in ingredients:
            self.table.insert(tk.END, ingredient[1])  # 재료 이름 테이블에 추가

        cursor.close()
        connection.close()

    def get_selected_ingredient_id(self):
        """사용자가 선택한 재료의 ID를 반환합니다."""
        selected_index = self.table.curselection()
        if selected_index:
            ingredient_name = self.table.get(selected_index[0])
            return self.get_ingredient_id_by_name(ingredient_name)
        return None

    def get_ingredient_id_by_name(self, name):
        """재료 이름에 해당하는 ingredient_id를 DB에서 찾습니다."""
        connection = connect_to_freshlydb()
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM ingredients WHERE name = %s", (name,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()

        if result:
            return result[0]
        return None

    def update_table(self):
        """테이블을 갱신하여 변경된 내용을 반영합니다."""
        self.table.delete(0, tk.END)  # 기존 데이터 모두 삭제
        self.load_ingredients()  # 재료 목록을 다시 로드해 테이블 업데이트
