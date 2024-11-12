#로그인
import tkinter as tk

class Login:
    def __init__(self, parent):
        self.frame = tk.Frame(parent)
        
        tk.Label(self.frame, text="로그인", font=("Arial", 14)).pack(pady=10)
        
        tk.Label(self.frame, text="아이디:").pack(anchor="w", padx=20)
        tk.Entry(self.frame).pack(fill="x", padx=20, pady=5)
        
        tk.Label(self.frame, text="비밀번호:").pack(anchor="w", padx=20)
        tk.Entry(self.frame, show="*").pack(fill="x", padx=20, pady=5)
        
        tk.Button(self.frame, text="로그인", width=10).pack(pady=10)
        tk.Button(self.frame, text="회원가입", width=10).pack(pady=5)
