#재료 추가
import tkinter as tk
from tkinter import ttk
from datetime import date
from ingredient_table import IngredientTable


class AddIngredient:
    def __init__(self, parent, fridge, freezer, room_temp):
        self.frame = tk.Frame(parent)
        self.fridge = fridge
        self.freezer = freezer
        self.room_temp = room_temp

        # 저장 위치 선택
        self.storage_type = tk.StringVar()
        self.storage_type.set("냉장")  # 기본값: 냉장

        storage_label = tk.Label(self.frame, text="저장 위치 선택:")
        storage_label.pack(pady=5)

        storage_options = ttk.Combobox(self.frame, textvariable=self.storage_type)
        storage_options["values"] = ("냉장", "냉동", "실온")
        storage_options.pack(pady=5)

        # 재료 입력
        ingredient_label = tk.Label(self.frame, text="재료명:")
        ingredient_label.pack(pady=5)

        self.ingredient_entry = tk.Entry(self.frame)
        self.ingredient_entry.pack(pady=5)

        # 구매 일자
        purchase_date_label = tk.Label(self.frame, text="구매 일자 (YYYY-MM-DD):")
        purchase_date_label.pack(pady=5)

        self.purchase_date_entry = tk.Entry(self.frame)
        self.purchase_date_entry.insert(0, date.today().isoformat())  # 오늘 날짜 기본값
        self.purchase_date_entry.pack(pady=5)

        # 유통기한
        expiration_date_label = tk.Label(self.frame, text="유통기한 (YYYY-MM-DD):")
        expiration_date_label.pack(pady=5)

        self.expiration_date_entry = tk.Entry(self.frame)
        self.expiration_date_entry.insert(0, date.today().isoformat())  # 기본값
        self.expiration_date_entry.pack(pady=5)

        # 재료 추가 버튼
        add_button = tk.Button(
            self.frame, text="재료 추가", command=self.add_ingredient
        )
        add_button.pack(pady=5)

    def add_ingredient(self):
        ingredient = self.ingredient_entry.get()
        purchase_date = self.purchase_date_entry.get()
        expiration_date = self.expiration_date_entry.get()
        storage_type = self.storage_type.get()

        if ingredient and purchase_date and expiration_date:
            # 선택된 저장 위치에 재료 추가
            if storage_type == "냉장":
                self.fridge.ingredient_table.add_ingredient(
                    ingredient, purchase_date, expiration_date
                )
            elif storage_type == "냉동":
                self.freezer.ingredient_table.add_ingredient(
                    ingredient, purchase_date, expiration_date
                )
            elif storage_type == "실온":
                self.room_temp.ingredient_table.add_ingredient(
                    ingredient, purchase_date, expiration_date
                )

            # 입력 초기화
            self.ingredient_entry.delete(0, tk.END)
            self.purchase_date_entry.delete(0, tk.END)
            self.purchase_date_entry.insert(0, date.today().isoformat())
            self.expiration_date_entry.delete(0, tk.END)
            self.expiration_date_entry.insert(0, date.today().isoformat())
