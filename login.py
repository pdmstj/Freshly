# 로그인
import tkinter as tk
from tkinter import messagebox
from db_connect import connect_to_freshlydb
import hashlib


class Login:
    def __init__(self, notebook, switch_to_signup, on_login_success):
        """로그인 화면 초기화"""
        self.notebook = notebook
        self.switch_to_signup = switch_to_signup
        self.on_login_success = on_login_success

        # 로그인 화면 UI 설정
        self.frame = tk.Frame(self.notebook, bg="#E3F2FD")  # 파스텔 하늘색 배경 추가
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        # 사용자 이름 레이블과 입력 필드
        self.username_label = tk.Label(self.frame, text="아이디", font=("Helvetica", 12, "bold"), bg="#E3F2FD", fg="#0D47A1")
        self.username_label.pack(pady=(20, 5))
        self.username_entry = tk.Entry(self.frame, font=("Helvetica", 12))
        self.username_entry.pack(pady=5)

        # 비밀번호 레이블과 입력 필드
        self.password_label = tk.Label(self.frame, text="비밀번호", font=("Helvetica", 12, "bold"), bg="#E3F2FD", fg="#0D47A1")
        self.password_label.pack(pady=(20, 5))
        self.password_entry = tk.Entry(self.frame, show="*", font=("Helvetica", 12))
        self.password_entry.pack(pady=5)

        # 로그인 버튼
        self.login_button = tk.Button(
            self.frame, 
            text="로그인", 
            command=self.login, 
            bg="#A5D6A7", 
            fg="#1B5E20", 
            font=("Helvetica", 12, "bold"), 
            relief="raised", 
            borderwidth=2
        )
        self.login_button.pack(pady=(20, 5))

        # 회원가입 버튼
        self.signup_button = tk.Button(
            self.frame, 
            text="회원가입", 
            command=self.switch_to_signup, 
            bg="#BBDEFB", 
            fg="#0D47A1", 
            font=("Helvetica", 12, "bold"), 
            relief="raised", 
            borderwidth=2
        )
        self.signup_button.pack(pady=(5, 20))

    def login(self):
        """로그인 프로세스"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        # 빈 값 확인
        if not username or not password:
            messagebox.showwarning("입력 오류", "아이디와 비밀번호를 모두 입력하세요.")
            return

        # 로그인 성공 여부 확인
        if check_login(username, password):
            self.on_login_success(username, password)  # 로그인 성공 시 사용자 정보 전달
        else:
            messagebox.showerror("로그인 실패", "아이디 또는 비밀번호가 틀립니다.")


# 사용자 로그인 정보 db에서 확인
def check_login(username, password):
    """사용자 로그인 정보 확인"""
    user = "root"  # 데이터베이스 고정 사용자 계정
    password_db = "970814"  # 고정 비밀번호

    connection = connect_to_freshlydb(user, password_db)
    if not connection:
        messagebox.showerror("DB 연결 오류", "데이터베이스에 연결할 수 없습니다.")
        return False

    cursor = connection.cursor()
    try:
        # 입력된 비밀번호를 해싱
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # 아이디와 해싱된 비밀번호가 데이터베이스와 일치하는지 확인
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, hashed_password))
        result = cursor.fetchone()

        return result is not None

    except Exception as e:
        print(f"Error during login: {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


# 예시로 Login 클래스 사용 (루트 윈도우 생성)
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Login Example")
    root.configure(bg="#E3F2FD")  # 루트 창 배경색 설정

    def switch_to_signup():
        """회원가입 화면으로 전환"""
        messagebox.showinfo("회원가입", "회원가입 화면으로 전환")

    def on_login_success(username, password):
        """로그인 성공 후 처리"""
        messagebox.showinfo("로그인 성공", f"환영합니다, {username}님!")

    login_frame = Login(root, switch_to_signup, on_login_success)

    root.mainloop()
