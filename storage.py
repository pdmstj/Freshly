# 냉장, 냉동, 실온 처리

import tkinter as tk
from db_connect import connect_to_freshlydb


class Storage:
    def __init__(self, notebook):
        self.notebook = notebook
        # 각 탭을 생성
        self.fridge_tab = tk.Frame(self.notebook)
        self.freezer_tab = tk.Frame(self.notebook)
        self.room_temp_tab = tk.Frame(self.notebook)

        # 탭 추가
        notebook.add(self.fridge_tab, text="냉장")
        notebook.add(self.freezer_tab, text="냉동")
        notebook.add(self.room_temp_tab, text="실온")

        # 각 탭에 맞는 재료 로드
        self.load_ingredients("냉장", self.fridge_tab)
        self.load_ingredients("냉동", self.freezer_tab)
        self.load_ingredients("실온", self.room_temp_tab)

    def load_ingredients(self, storage_type, tab_frame):
        connection = connect_to_freshlydb()
        cursor = connection.cursor()

        # 각 저장 유형별로 재료 불러오기
        cursor.execute(
            "SELECT name, expiration_date FROM ingredients WHERE storage_type = %s",
            (storage_type,),
        )
        ingredients = cursor.fetchall()

        # 재료를 탭에 표시
        for ingredient in ingredients:
            label = tk.Label(tab_frame, text=f"{ingredient[0]} - {ingredient[1]}")
            label.pack(anchor="w", padx=10, pady=2)

        cursor.close()
        connection.close()
