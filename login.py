# 로그인
import tkinter as tk
from tkinter import messagebox
from db_connect import connect_to_freshlydb
import hashlib


class Login:
    def __init__(self, notebook, switch_to_signup, on_login_success):
        self.notebook = notebook
        self.switch_to_signup = switch_to_signup
        self.on_login_success = on_login_success

        # 로그인 화면 UI 설정
        self.frame = tk.Frame(self.notebook)

        # 사용자 이름 레이블과 입력 필드
        self.username_label = tk.Label(self.frame, text="아이디")
        self.username_label.pack(pady=(20, 5))  # 위쪽에 여백 추가
        self.username_entry = tk.Entry(self.frame)
        self.username_entry.pack(pady=5)  # 아래 여백 추가

        # 비밀번호 레이블과 입력 필드
        self.password_label = tk.Label(self.frame, text="비밀번호")
        self.password_label.pack(pady=(20, 5))  # 위쪽에 여백 추가
        self.password_entry = tk.Entry(self.frame, show="*")
        self.password_entry.pack(pady=5)  # 아래 여백 추가

        # 로그인 버튼
        self.login_button = tk.Button(self.frame, text="로그인", command=self.login)
        self.login_button.pack(pady=(20, 5))  # 위쪽에 여백 추가

        # 회원가입 버튼
        self.signup_button = tk.Button(
            self.frame, text="회원가입", command=self.switch_to_signup
        )
        self.signup_button.pack(pady=(5, 20))  # 아래쪽에 여백 추가

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # 로그인 성공 시 호출되는 콜백 함수
        if check_login(username, password):
            self.on_login_success()  # 로그인 성공 시 성공 콜백 호출
        else:
            messagebox.showerror("Login", "아이디 또는 비밀번호가 틀립니다.")


# 사용자 로그인 정보 db에서 확인
def check_login(username, password):
    connection = connect_to_freshlydb()
    cursor = connection.cursor()

    try:
        # 비밀번호를 비교
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # 아이디와 해싱된 비밀번호가 일치하는지 확인
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, hashed_password))
        result = cursor.fetchone()

    except Exception as e:
        print(f"Error during login: {e}")
        return False
    finally:
        cursor.close()
        connection.close()

    # 로그인 성공 여부 반환
    return result is not None
