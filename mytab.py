# 마이페이지
import tkinter as tk
from tkinter import messagebox
from db_connect import connect_to_freshlydb

class MyTab:
    def __init__(self, parent):
        self.frame = tk.Frame(parent)
        self.user_id = user_id  # 로그인된 사용자 아이디

        tk.Label(self.frame, text="마이페이지", font=("Arial", 14)).pack(pady=10)

        self.name_var = tk.StringVar()
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        tk.Label(self.frame, text="이름:").pack(anchor="w", padx=20)
        self.name_entry = tk.Entry(self.frame, textvariable=self.name_var)
        tk.Entry(self.frame).pack(fill="x", padx=20, pady=5)

        tk.Label(self.frame, text="아이디:").pack(anchor="w", padx=20)
        self.username_entry = tk.Entry(
            self.frame, textvariable=self.username_var, state="readonly")
        tk.Entry(self.frame).pack(fill="x", padx=20, pady=5)

        tk.Label(self.frame, text="비밀번호:").pack(anchor="w", padx=20)
        self.password_entry = tk.Entry(self.frame, textvariable=self.password_var, show="*")
        self.password_entry.pack(fill="x", padx=20, pady=5)

        tk.Button(self.frame, text="수정", width=10, command=self.update_user_info).pack(pady=10)

        # 사용자 정보 로드
        self.load_user_info()

    def load_user_info(self):
        """DB에서 사용자 정보를 불러와서 UI에 표시"""
        connection = connect_to_freshlydb()
        cursor = connection.cursor()

        # 사용자 정보 DB에서 가져오기
        cursor.execute(
            "SELECT name, username, password FROM users WHERE id = %s", (self.user_id,)
        )
        user_info = cursor.fetchone()

        if user_info:
            self.name_var.set(user_info[0])
            self.username_var.set(user_info[1])
            self.password_var.set(user_info[2])

        cursor.close()
        connection.close()

    def update_user_info(self):
        """사용자가 입력한 정보를 DB에 업데이트"""
        new_name = self.name_var.get()
        new_password = self.password_var.get()

        connection = connect_to_freshlydb()
        cursor = connection.cursor()

        # 사용자 정보 업데이트
        cursor.execute(
            "UPDATE users SET name = %s, password = %s WHERE id = %s",
            (new_name, new_password, self.user_id),
        )

        connection.commit()
        cursor.close()
        connection.close()

        messagebox.showinfo("수정 완료", "사용자 정보가 수정되었습니다.")
