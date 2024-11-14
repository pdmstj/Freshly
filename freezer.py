# 냉동고
import tkinter as tk
from tkinter import messagebox
from db_connect import connect_to_freshlydb


class Freezer:
    def __init__(self, parent):
        self.frame = tk.Frame(parent)

        # 냉동고 재료 목록 로딩
        self.load_ingredients()

        # 삭제 버튼
        delete_button = tk.Button(
            self.frame,
            text="삭제",
            command=self.remove_ingredient,
        )
        delete_button.pack(pady=5)

    def load_ingredients(self):
        """냉동고에 있는 재료 목록을 DB에서 로드하여 표시합니다."""
        connection = connect_to_freshlydb()
        cursor = connection.cursor()

        # 냉동고 재료 목록을 DB에서 가져오기 (냉동고에 해당하는 재료만)
        cursor.execute("SELECT id, name FROM ingredients WHERE storage_type = '냉동'")
        ingredients = cursor.fetchall()

        # 재료 목록 UI에 표시
        self.checkbuttons = []  # 체크박스 리스트 초기화
        for ingredient in ingredients:
            var = tk.IntVar()  # 체크박스 상태를 나타내는 변수
            checkbutton = tk.Checkbutton(self.frame, text=ingredient[1], variable=var)
            checkbutton.pack(anchor="w")
            self.checkbuttons.append(
                (ingredient[0], var)
            )  # (ingredient_id, var)로 저장

        cursor.close()
        connection.close()

    def remove_ingredient(self):
        """선택한 냉동고 재료를 삭제합니다."""
        connection = connect_to_freshlydb()
        cursor = connection.cursor()

        for ingredient_id, var in self.checkbuttons:
            if var.get() == 1:  # 체크박스가 선택되었을 경우
                # 냉동고에서 재료를 삭제 쿼리
                cursor.execute(
                    "DELETE FROM ingredients WHERE id = %s AND storage_type = '냉동'",
                    (ingredient_id,),
                )

        connection.commit()
        cursor.close()
        connection.close()

        messagebox.showinfo("냉동고", "선택한 재료가 냉동고에서 삭제되었습니다!")
        self.load_ingredients()  # 재료 삭제 후, 목록 갱신
