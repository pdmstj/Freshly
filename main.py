import tkinter as tk
from tkinter import ttk, messagebox


# 메인
class Freshly:
    def __init__(self, root):
        self.root = root
        self.root.title("Freshly")
        self.root.geometry("320x540")

        # 탭 구성
        notebook = ttk.Notebook(root)

        self.main_tab = ttk.Frame(notebook)
        self.fridge_tab = ttk.Frame(notebook)
        self.freezer_tab = ttk.Frame(notebook)
        self.cart_tab = ttk.Frame(notebook)
        self.profile_tab = ttk.Frame(notebook)

        notebook.add(self.main_tab, text="메인")
        notebook.add(self.fridge_tab, text="냉장")
        notebook.add(self.freezer_tab, text="냉동")
        notebook.add(self.cart_tab, text="장바구니")
        notebook.add(self.profile_tab, text="마이페이지")
        notebook.pack(expand=True, fill="both")

        # UI 구성
        self.setup_main_tab()
        self.setup_fridge_tab()
        self.setup_freezer_tab()
        self.setup_cart_tab()
        self.setup_profile_tab()

    def setup_main_tab(self):
        # 메인(로그인, 회원가입 버튼)
        tk.Label(self.main_tab, text="환영합니다!", font=("Arial", 14)).pack(pady=10)

        tk.Button(
            self.main_tab, text="로그인", command=self.login_screen, width=20
        ).pack(pady=5)
        tk.Button(
            self.main_tab, text="회원가입", command=self.register_screen, width=20
        ).pack(pady=5)

    def setup_fridge_tab(self):
        # 냉장 식재료 목록 테이블 추가
        self.create_ingredient_table(self.fridge_tab)

    def setup_freezer_tab(self):
        # 냉동 식재료 목록 테이블 추가
        self.create_ingredient_table(self.freezer_tab)

    def setup_cart_tab(self):
        # 장바구니 식재료 목록 테이블 및 버튼 추가
        tk.Label(self.cart_tab, text="장바구니", font=("Arial", 12)).pack(pady=10)
        self.create_ingredient_table(self.cart_tab)

        tk.Button(self.cart_tab, text="추가", command=self.add_to_cart, width=10).pack(
            side="left", padx=5, pady=20
        )
        tk.Button(
            self.cart_tab, text="삭제", command=self.remove_from_cart, width=10
        ).pack(side="right", padx=5, pady=20)

    def setup_profile_tab(self):
        # 마이페이지
        tk.Label(self.profile_tab, text="마이페이지", font=("Arial", 14)).pack(pady=10)

        # 사용자 정보 입력
        tk.Label(self.profile_tab, text="이름:").pack(anchor="w", padx=20)
        tk.Entry(self.profile_tab).pack(fill="x", padx=20, pady=5)

        tk.Label(self.profile_tab, text="아이디:").pack(anchor="w", padx=20)
        tk.Entry(self.profile_tab).pack(fill="x", padx=20, pady=5)

        tk.Label(self.profile_tab, text="비밀번호:").pack(anchor="w", padx=20)
        tk.Entry(self.profile_tab, show="*").pack(fill="x", padx=20, pady=5)

        tk.Button(self.profile_tab, text="수정", width=10).pack(pady=10)

    def create_ingredient_table(self, tab):
        # 식재료 테이블 생성
        tree = ttk.Treeview(
            tab, columns=("이름", "구매일", "소비기한"), show="headings"
        )
        tree.heading("이름", text="이름")
        tree.heading("구매일", text="구매일")
        tree.heading("소비기한", text="소비기한")
        tree.pack(fill="both", expand=True)

        # 임시 데이터 추가
        tree.insert("", "end", values=("부추", "24.10.14", "24.10.21"))
        tree.insert("", "end", values=("감자", "24.10.09", "24.11.09"))

    def login_screen(self):
        # 로그인 화면 생성
        login_win = tk.Toplevel(self.root)
        login_win.title("로그인")
        login_win.geometry("300x200")

        tk.Label(login_win, text="아이디:").pack(anchor="w", padx=20)
        tk.Entry(login_win).pack(fill="x", padx=20, pady=5)

        tk.Label(login_win, text="비밀번호:").pack(anchor="w", padx=20)
        tk.Entry(login_win, show="*").pack(fill="x", padx=20, pady=5)

        tk.Button(
            login_win,
            text="로그인",
            command=lambda: messagebox.showinfo("로그인", "로그인 성공!"),
        ).pack(pady=10)

    def register_screen(self):
        # 회원가입 화면이긔
        register_win = tk.Toplevel(self.root)
        register_win.title("회원가입")
        register_win.geometry("300x250")

        tk.Label(register_win, text="이름:").pack(anchor="w", padx=20)
        tk.Entry(register_win).pack(fill="x", padx=20, pady=5)

        tk.Label(register_win, text="아이디:").pack(anchor="w", padx=20)
        tk.Entry(register_win).pack(fill="x", padx=20, pady=5)

        tk.Label(register_win, text="비밀번호:").pack(anchor="w", padx=20)
        tk.Entry(register_win, show="*").pack(fill="x", padx=20, pady=5)

        tk.Label(register_win, text="이메일:").pack(anchor="w", padx=20)
        tk.Entry(register_win).pack(fill="x", padx=20, pady=5)

        tk.Button(
            register_win,
            text="회원가입",
            command=lambda: messagebox.showinfo("회원가입", "회원가입 성공!"),
        ).pack(pady=10)

# 프로그램 실행
root = tk.Tk()
app = Freshly(root)
root.mainloop()
