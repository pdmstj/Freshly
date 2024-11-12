#마이페이지
import tkinter as tk


class Profile:
    def __init__(self, parent):
        self.frame = tk.Frame(parent)

        tk.Label(self.frame, text="마이페이지", font=("Arial", 14)).pack(pady=10)

        tk.Label(self.frame, text="이름:").pack(anchor="w", padx=20)
        tk.Entry(self.frame).pack(fill="x", padx=20, pady=5)

        tk.Label(self.frame, text="아이디:").pack(anchor="w", padx=20)
        tk.Entry(self.frame).pack(fill="x", padx=20, pady=5)

        tk.Label(self.frame, text="비밀번호:").pack(anchor="w", padx=20)
        tk.Entry(self.frame, show="*").pack(fill="x", padx=20, pady=5)

        tk.Button(self.frame, text="수정", width=10).pack(pady=10)
