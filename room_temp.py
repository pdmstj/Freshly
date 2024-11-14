# 삭제버튼
import tkinter as tk
from tkinter import messagebox
from db_connect import connect_to_freshlydb

class RoomTemp:
    def __init__(self, parent):
        self.frame = tk.Frame(parent)
        self.ingredient_listbox = tk.Listbox(self.frame, selectmode=tk.SINGLE)
        self.ingredient_listbox.pack(padx=20, pady=20, fill="both", expand=True)

        # 삭제 버튼
        delete_button = tk.Button(
            self.frame,
            text="삭제",
            command=self.remove_ingredient_from_db,
        )
        delete_button.pack(pady=5)

        # 재료 목록 불러오기
        self.load_ingredients()

    def load_ingredients(self):
        """DB에서 재료 목록을 불러와서 Listbox에 표시"""
        connection = connect_to_freshlydb()
        cursor = connection.cursor()

        # 실온 재료 목록 가져오기
        cursor.execute("SELECT id, name FROM ingredients WHERE storage_type = '실온'")
        ingredients = cursor.fetchall()

        # Listbox 재료 추가
        self.ingredient_listbox.delete(0, tk.END)  # 기존 목록 삭제
        for ingredient in ingredients:
            self.ingredient_listbox.insert(tk.END, ingredient[1])  # 재료 이름 추가

        cursor.close()
        connection.close()

    def remove_ingredient_from_db(self):
        """선택된 재료를 DB에서 삭제합니다."""
        selected_index = (
            self.ingredient_listbox.curselection()
        )  # 선택된 항목 인덱스 가져오기

        if selected_index:
            selected_ingredient_name = self.ingredient_listbox.get(
                selected_index
            )  # 선택된 재료 이름

            # db 연결
            connection = connect_to_freshlydb()
            cursor = connection.cursor()

            # 재료 ID 가져오기
            cursor.execute(
                "SELECT id FROM ingredients WHERE name = %s AND storage_type = '실온'",
                (selected_ingredient_name,),
            )
            ingredient_id = cursor.fetchone()

            if ingredient_id:
                # 재료 DB에서 삭제하는 쿼리
                cursor.execute(
                    "DELETE FROM ingredients WHERE id = %s", (ingredient_id[0],)
                )
                connection.commit()
                messagebox.showinfo("삭제 완료", "선택한 재료가 삭제되었습니다!")
                self.load_ingredients()  # 삭제 후 재료 목록 갱신
            else:
                messagebox.showwarning("삭제 오류", "선택한 재료를 찾을 수 없습니다.")

            cursor.close()
            connection.close()
        else:
            messagebox.showwarning("선택 오류", "삭제할 재료를 선택해주세요.")
