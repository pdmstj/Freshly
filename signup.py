import tkinter as tk
from tkinter import messagebox
from db_connect import connect_to_freshlydb
import hashlib
from mysql.connector import Error


class SignUp:
    def __init__(self, parent, user, password, switch_to_login):
        """회원가입 화면을 초기화합니다."""
        self.user = user  # 애플리케이션 고정 사용자 계정
        self.password = password
        self.switch_to_login = switch_to_login

        # 메인 프레임 생성
        self.frame = tk.Frame(parent, bg="#E3F2FD")  # 파스텔 하늘색 배경 추가
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        # 타이틀
        tk.Label(self.frame, text="회원가입", font=("Helvetica", 16, "bold"), bg="#E3F2FD", fg="#0D47A1").pack(pady=10)

        # 입력 필드
        self.name_entry = tk.Entry(self.frame, font=("Helvetica", 12))
        self.username_entry = tk.Entry(self.frame, font=("Helvetica", 12))
        self.password_entry = tk.Entry(self.frame, show="*", font=("Helvetica", 12))
        self.confirm_password_entry = tk.Entry(self.frame, show="*", font=("Helvetica", 12))
        self.email_entry = tk.Entry(self.frame, font=("Helvetica", 12))

        # 입력 필드 UI 설정
        self.create_input_field("이름", self.name_entry)
        self.create_input_field("아이디", self.username_entry)
        self.create_input_field("비밀번호", self.password_entry)
        self.create_input_field("비밀번호 확인", self.confirm_password_entry)
        self.create_input_field("이메일", self.email_entry)

        # 회원가입 버튼
        tk.Button(
            self.frame, 
            text="회원가입", 
            width=10, 
            command=self.signup, 
            bg="#A5D6A7", 
            fg="#1B5E20", 
            font=("Helvetica", 12, "bold"), 
            relief="raised", 
            borderwidth=2
        ).pack(pady=10)

    def create_input_field(self, label_text, entry_widget):
        """라벨과 입력 필드를 생성하는 공통 함수"""
        tk.Label(self.frame, text=label_text, font=("Helvetica", 12, "bold"), bg="#E3F2FD", fg="#0D47A1").pack(anchor="w", padx=20)
        entry_widget.pack(fill="x", padx=20, pady=5)

    def signup(self):
        """회원가입 프로세스"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        email = self.email_entry.get().strip()
        name = self.name_entry.get().strip()

        # 빈 값 체크
        if not username or not password or not email or not name:
            messagebox.showwarning("회원가입", "모든 필드를 채워주세요.")
            return

        # 비밀번호 확인
        if password != confirm_password:
            messagebox.showwarning("회원가입", "비밀번호가 일치하지 않습니다.")
            return

        # 비밀번호 해싱
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # DB에 회원가입 정보 저장
        if self.save_user_to_db(username, hashed_password, name, email):
            messagebox.showinfo("회원가입", "회원가입이 성공적으로 완료되었습니다.")
            # 입력 필드 초기화 및 로그인 페이지 이동
            self.name_entry.delete(0, tk.END)
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            self.confirm_password_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)
            self.switch_to_login()
        else:
            messagebox.showerror("회원가입", "회원가입 실패: 아이디가 이미 존재하거나 시스템 오류가 발생했습니다.")

    def save_user_to_db(self, username, password, name, email):
        """회원 정보를 데이터베이스에 저장"""
        connection = None
        cursor = None
        try:
            # 데이터베이스 연결
            connection = connect_to_freshlydb(self.user, self.password)
            if not connection or not connection.is_connected():
                messagebox.showerror("회원가입", "데이터베이스에 연결할 수 없습니다.")
                return False

            cursor = connection.cursor()

            # 아이디 중복 검사
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            if cursor.fetchone():
                messagebox.showwarning("회원가입", "아이디가 이미 존재합니다. 다른 아이디를 사용하세요.")
                return False

            # 새로운 사용자 추가
            query = "INSERT INTO users (username, password, name, email) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (username, password, name, email))
            connection.commit()
            return True

        except Error as e:
            # 데이터베이스 오류 처리
            messagebox.showerror("회원가입", f"데이터베이스 오류: {e}")
            return False

        finally:
            # 자원 정리
            try:
                if cursor:
                    cursor.close()
                if connection and connection.is_connected():
                    connection.close()
            except Exception as cleanup_error:
                print(f"자원 정리 중 오류 발생: {cleanup_error}")
