# 장바구니
import tkinter as tk
from tkinter import messagebox
from db_connect import connect_to_freshlydb


class Cart:
    def __init__(self, parent):
        self.frame = tk.Frame(parent)
        self.selected_ingredients = []

        # 장바구니 UI 표시할 재료 목록 로딩
        self.load_available_ingredients()

        # 장바구니 추가/삭제 버튼
        tk.Button(self.frame, text="추가", command=self.add_to_cart, width=10).pack(
            side="left", padx=5, pady=20
        )
        tk.Button(
            self.frame, text="삭제", command=self.remove_from_cart, width=10
        ).pack(side="right", padx=5, pady=20)

    def load_available_ingredients(self):
        """사용자가 선택할 수 있는 재료 목록을 DB에서 로드합니다."""
        connection = connect_to_freshlydb()
        cursor = connection.cursor()

        # 재료 목록을 DB에서 가져옵니다.
        cursor.execute("SELECT id, name FROM ingredients")
        ingredients = cursor.fetchall()

        # 재료 목록을 UI에 표시합니다.
        self.checkbuttons = []  # 체크박스 리스트 초기화
        for ingredient in ingredients:
            var = tk.IntVar()  # 체크박스의 상태를 나타내는 변수
            checkbutton = tk.Checkbutton(self.frame, text=ingredient[1], variable=var)
            checkbutton.pack(anchor="w")
            self.checkbuttons.append(
                (ingredient[0], var)
            )  # (ingredient_id, var)로 저장

        cursor.close()
        connection.close()

    def add_to_cart(self):
        """사용자가 선택한 재료들을 장바구니에 추가합니다."""
        connection = connect_to_freshlydb()
        cursor = connection.cursor()

        for ingredient_id, var in self.checkbuttons:
            if var.get() == 1:  # 체크박스가 선택되었을 경우
                # 장바구니에 추가하는 쿼리
                cursor.execute(
                    "INSERT INTO shopping_cart (ingredient_id, quantity) VALUES (%s, 1)",
                    (ingredient_id,),
                )

        connection.commit()
        cursor.close()
        connection.close()
        messagebox.showinfo("장바구니", "선택한 재료가 장바구니에 추가되었습니다!")

    def remove_from_cart(self):
        """사용자가 선택한 재료들을 장바구니에서 삭제합니다."""
        connection = connect_to_freshlydb()
        cursor = connection.cursor()

        for ingredient_id, var in self.checkbuttons:
            if var.get() == 1:  # 체크박스가 선택되었을 경우
                # 장바구니에서 삭제하는 쿼리
                cursor.execute(
                    "DELETE FROM shopping_cart WHERE ingredient_id = %s",
                    (ingredient_id,),
                )

        connection.commit()
        cursor.close()
        connection.close()
        messagebox.showinfo("장바구니", "선택한 재료가 장바구니에서 삭제되었습니다!")
