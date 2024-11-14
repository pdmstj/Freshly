# 회원가입
import tkinter as tk
from tkinter import messagebox
from db_connect import connect_to_freshlydb


class SignUp:
    def __init__(self, parent):
        self.frame = tk.Frame(parent)

        tk.Label(self.frame, text="회원가입", font=("Arial", 14)).pack(pady=10)

        # 이름, 아이디, 비밀번호, 이메일 입력 필드
        self.name_entry = tk.Entry(self.frame)
        self.username_entry = tk.Entry(self.frame)
        self.password_entry = tk.Entry(self.frame, show="*")
        self.email_entry = tk.Entry(self.frame)

        # 입력 필드 UI 설정
        self.create_input_field("이름", self.name_entry)
        self.create_input_field("아이디", self.username_entry)
        self.create_input_field("비밀번호", self.password_entry)
        self.create_input_field("이메일", self.email_entry)

        # 회원가입 버튼
        tk.Button(self.frame, text="회원가입", width=10, command=self.signup).pack(pady=10)

     def create_input_field(self, label_text, entry_widget):
        """라벨과 입력 필드를 생성하는 공통 함수"""
        tk.Label(self.frame, text=label_text).pack(anchor="w", padx=20)
        entry_widget.pack(fill="x", padx=20, pady=5)

    def signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        email = self.email_entry.get()
        name = self.name_entry.get()

        # 회원가입 정보가 빈 값인지 확인
        if not username or not password or not email or not name:
            messagebox.showwarning("회원가입", "모든 필드를 채워주세요.")
            return

        # DB에 회원가입 정보 저장
        if save_user_to_db(username, password, name, email):
            messagebox.showinfo("회원가입", "회원가입이 성공적으로 완료되었습니다.")
        else:
            messagebox.showerror("회원가입", "회원가입 실패, 아이디가 이미 존재합니다.")


# 회원가입 정보 DB에 저장하는 함수
def save_user_to_db(username, password, name, email):
    connection = connect_to_freshlydb()
    cursor = connection.cursor()

    # 아이디 중복 검사
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    if cursor.fetchone():
        cursor.close()
        connection.close()
        return False  # 이미 존재하는 아이디

    # 새로운 사용자 추가
    query = "INSERT INTO users (username, password, name, email) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (username, password, name, email))
    connection.commit()

    cursor.close()
    connection.close()
    return True