# 재료 추가
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import date
from db_connect import connect_to_freshlydb


class AddIngredient:
    def __init__(self, parent, fridge, freezer, room_temp, user, password):
        self.user = user
        self.password = password

        self.frame = tk.Frame(parent, bg="#E3F2FD")  # 파스텔 하늘색 배경 추가
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)  # 프레임을 화면에 표시

        self.fridge = fridge
        self.freezer = freezer
        self.room_temp = room_temp

        # 저장 위치 선택
        self.storage_type = tk.StringVar()
        self.storage_type.set("냉장")  # 기본값: 냉장

        storage_label = tk.Label(self.frame, text="저장 위치 선택:", font=("Helvetica", 12, "bold"), bg="#E3F2FD", fg="#0D47A1")
        storage_label.pack(pady=5)

        storage_options = ttk.Combobox(self.frame, textvariable=self.storage_type, font=("Helvetica", 12))
        storage_options["values"] = ("냉장", "냉동", "실온")
        storage_options.pack(pady=5)

        # 재료 입력
        ingredient_label = tk.Label(self.frame, text="재료명:", font=("Helvetica", 12, "bold"), bg="#E3F2FD", fg="#0D47A1")
        ingredient_label.pack(pady=5)

        self.ingredient_entry = tk.Entry(self.frame, font=("Helvetica", 12))
        self.ingredient_entry.pack(pady=5)

        # 구매 일자
        purchase_date_label = tk.Label(self.frame, text="구매 일자 (YYYY-MM-DD):", font=("Helvetica", 12, "bold"), bg="#E3F2FD", fg="#0D47A1")
        purchase_date_label.pack(pady=5)

        self.purchase_date_entry = tk.Entry(self.frame, font=("Helvetica", 12))
        self.purchase_date_entry.insert(0, date.today().isoformat())  # 오늘 날짜 기본값
        self.purchase_date_entry.pack(pady=5)

        # 유통기한
        expiration_date_label = tk.Label(self.frame, text="유통기한 (YYYY-MM-DD):", font=("Helvetica", 12, "bold"), bg="#E3F2FD", fg="#0D47A1")
        expiration_date_label.pack(pady=5)

        self.expiration_date_entry = tk.Entry(self.frame, font=("Helvetica", 12))
        self.expiration_date_entry.insert(0, date.today().isoformat())  # 기본값
        self.expiration_date_entry.pack(pady=5)

        # 재료 추가 버튼
        add_button = tk.Button(
            self.frame, 
            text="재료 추가", 
            command=self.add_ingredient, 
            bg="#A5D6A7", 
            fg="#1B5E20", 
            font=("Helvetica", 12, "bold"), 
            relief="raised", 
            borderwidth=2
        )
        add_button.pack(pady=5)

    def add_ingredient(self):
        ingredient = self.ingredient_entry.get()
        purchase_date = self.purchase_date_entry.get()
        expiration_date = self.expiration_date_entry.get()
        storage_type = self.storage_type.get()

        if ingredient and purchase_date and expiration_date:
            connection = connect_to_freshlydb(self.user, self.password)
            cursor = connection.cursor()

            # 저장 위치를 storage_type_id로 변환
            cursor.execute("SELECT id FROM storage_types WHERE section_name = %s", (storage_type,))
            result = cursor.fetchone()

            if result:
                storage_type_id = result[0]
            else:
                messagebox.showerror("오류", f"잘못된 저장소 유형: {storage_type}")
                connection.close()
                return

            # 재료 추가 쿼리
            cursor.execute(
                "INSERT INTO ingredients (name, purchase_date, expiration_date, storage_type_id) VALUES (%s, %s, %s, %s)",
                (ingredient, purchase_date, expiration_date, storage_type_id),
            )

            connection.commit()
            cursor.close()
            connection.close()

            # 입력 초기화
            self.ingredient_entry.delete(0, tk.END)
            self.purchase_date_entry.delete(0, tk.END)
            self.purchase_date_entry.insert(0, date.today().isoformat())
            self.expiration_date_entry.delete(0, tk.END)
            self.expiration_date_entry.insert(0, date.today().isoformat())

            # 해당 저장 위치의 재료 목록 갱신
            if storage_type == "냉장":
                self.fridge.load_ingredients()
            elif storage_type == "냉동":
                self.freezer.load_ingredients()
            elif storage_type == "실온":
                self.room_temp.load_ingredients()

            # 추가 완료 메시지
            messagebox.showinfo(
                "성공", f"{ingredient} 재료가 {storage_type}에 추가되었습니다."
            )


# 예시로 AddIngredient 클래스 사용 (루트 윈도우 생성)
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Add Ingredient Example")
    root.configure(bg="#E3F2FD")  # 루트 창 배경색 설정

    # 사용자 정보를 여기에 정의 (root 사용자 예시)
    user = "root"
    password = "970814"

    add_ingredient = AddIngredient(root, None, None, None, user, password)

    root.mainloop()
