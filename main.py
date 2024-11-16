import tkinter as tk
from tkinter import ttk, messagebox
from login import Login
from fridge import Fridge
from freezer import Freezer
from room_temp import RoomTemp
from cart import Cart
from signup import SignUp
from add_ingredient import AddIngredient
from recipe_recommend import RecipeRecommendation


class FreshlyApp:
    def __init__(self, root):
        """Freshly 애플리케이션 초기화"""
        self.root = root
        self.root.title("Freshly - 냉장고 관리 애플리케이션")
        self.root.geometry("450x700")

        # 스타일 설정
        self.style = ttk.Style()
        self.style.theme_use("clam")  # 기본 테마 설정

        # 파스텔 하늘색 톤의 색상과 폰트 설정
        self.style.configure("TNotebook", background="#E3F2FD")  # 부드러운 파스텔 하늘색 배경
        self.style.configure("TNotebook.Tab", 
                            background="#BBDEFB", 
                            foreground="#0D47A1", 
                            font=("Helvetica", 10, "bold"), 
                            padding=(10, 5))
        self.style.map("TNotebook.Tab",
                       background=[("selected", "#90CAF9")],  # 선택된 탭의 색상 변경
                       foreground=[("selected", "#0D47A1")])

        # 루트 창 배경 색상 설정
        self.root.configure(bg="#E3F2FD")

        # 탭을 관리하는 Notebook 생성
        self.notebook = ttk.Notebook(self.root, style="TNotebook")
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # 애플리케이션에서 사용하는 고정 데이터베이스 계정
        self.db_user = "root"  # 데이터베이스 사용자 이름
        self.db_password = "970814"  # 데이터베이스 사용자 비밀번호

        # 로그인 탭 생성 및 추가
        self.login_tab = Login(self.notebook, self.switch_to_signup, self.on_login_success)
        self.notebook.add(self.login_tab.frame, text="로그인")

        # 회원가입 탭 생성 및 추가
        self.sign_up_tab = SignUp(self.notebook, self.db_user, self.db_password, self.switch_to_login)
        self.notebook.add(self.sign_up_tab.frame, text="회원가입")
        self.notebook.tab(self.sign_up_tab.frame, state="hidden")  # 초기 상태에서 비활성화

        # 사용자 정보를 저장하기 위한 속성
        self.logged_in_user = None  # 로그인된 사용자 이름

        # 초기 상태에서 로그인 탭 외 모든 탭 비활성화
        self.disable_tabs()

    def switch_to_signup(self):
        """회원가입 탭으로 전환"""
        self.notebook.tab(self.sign_up_tab.frame, state="normal")
        self.notebook.select(self.sign_up_tab.frame)

    def switch_to_login(self):
        """회원가입 후 로그인 탭으로 전환"""
        self.notebook.select(self.login_tab.frame)

    def on_login_success(self, username, password):
        """로그인 성공 후 처리"""
        # 로그인된 사용자 이름 저장
        self.logged_in_user = username
        print(f"로그인 성공: 사용자 - {self.logged_in_user}")

        # 각 탭 클래스 인스턴스 생성 (고정된 DB 계정 사용)
        self.fridge = Fridge(self.notebook, self.db_user, self.db_password)
        self.freezer = Freezer(self.notebook, self.db_user, self.db_password)
        self.room_temp = RoomTemp(self.notebook, self.db_user, self.db_password)
        self.cart = Cart(self.notebook)
        self.add_ingredient_tab = AddIngredient(
            self.notebook, self.fridge, self.freezer, self.room_temp, self.db_user, self.db_password
        )
        self.recommend_recipes_tab = RecipeRecommendation(self.notebook, self.fridge, self.freezer, self.room_temp, "40bc4817df984254aa6cc217d3ee6219")

        # 새로운 탭 추가
        self.notebook.add(self.fridge.frame, text="냉장고")
        self.notebook.add(self.freezer.frame, text="냉동고")
        self.notebook.add(self.room_temp.frame, text="실온 보관")
        self.notebook.add(self.cart.frame, text="장바구니")
        self.notebook.add(self.add_ingredient_tab.frame, text="재료 추가")
        self.notebook.add(self.recommend_recipes_tab.frame, text="요리 추천")

        # 로그인 후 탭 활성화
        self.enable_tabs()
        self.notebook.select(self.fridge.frame)

    def disable_tabs(self):
        """로그인 전 모든 탭 비활성화"""
        if hasattr(self, 'fridge'):
            self.notebook.tab(self.fridge.frame, state="hidden")
        if hasattr(self, 'freezer'):
            self.notebook.tab(self.freezer.frame, state="hidden")
        if hasattr(self, 'room_temp'):
            self.notebook.tab(self.room_temp.frame, state="hidden")
        if hasattr(self, 'cart'):
            self.notebook.tab(self.cart.frame, state="hidden")
        if hasattr(self, 'add_ingredient_tab'):
            self.notebook.tab(self.add_ingredient_tab.frame, state="hidden")
        if hasattr(self, 'recommend_recipes_tab'):
            self.notebook.tab(self.recommend_recipes_tab.frame, state="hidden")
        if hasattr(self, 'sign_up_tab'):
            self.notebook.tab(self.sign_up_tab.frame, state="hidden")

    def enable_tabs(self):
        """로그인 후 모든 탭 활성화"""
        if hasattr(self, 'fridge'):
            self.notebook.tab(self.fridge.frame, state="normal")
        if hasattr(self, 'freezer'):
            self.notebook.tab(self.freezer.frame, state="normal")
        if hasattr(self, 'room_temp'):
            self.notebook.tab(self.room_temp.frame, state="normal")
        if hasattr(self, 'cart'):
            self.notebook.tab(self.cart.frame, state="normal")
        if hasattr(self, 'add_ingredient_tab'):
            self.notebook.tab(self.add_ingredient_tab.frame, state="normal")
        if hasattr(self, 'recommend_recipes_tab'):
            self.notebook.tab(self.recommend_recipes_tab.frame, state="normal")


# 프로그램 실행
if __name__ == "__main__":
    root = tk.Tk()
    app = FreshlyApp(root)
    root.mainloop()
