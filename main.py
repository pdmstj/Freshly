import tkinter as tk
from tkinter import ttk
from login import Login
from fridge import Fridge
from freezer import Freezer
from room_temp import RoomTemp
from cart import Cart
from mytab import MyTab
from signup import SignUp
from add_ingredient import AddIngredient


class FreshlyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Freshly")
        self.root.geometry("320x540")

        # Notebook 생성 및 탭 추가
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack()

        # 각 탭 클래스 인스턴스화
        self.main_tab = Login(self.notebook, self.switch_to_signup)
        self.fridge = Fridge(self.notebook)
        self.freezer = Freezer(self.notebook)
        self.room_temp = RoomTemp(self.notebook)
        self.cart = Cart(self.notebook)
        self.my_tab = MyTab(self.notebook)
        self.sign_up_tab = SignUp(self.notebook)

        # 재료 추가 탭 인스턴스화 (냉장, 냉동, 실온 클래스 전달)
        self.add_ingredient_tab = AddIngredient(
            self.notebook, self.fridge, self.freezer, self.room_temp
        )

        self.notebook.add(self.main_tab.frame, text="메인")
        self.notebook.add(self.fridge.frame, text="냉장")
        self.notebook.add(self.freezer.frame, text="냉동")
        self.notebook.add(self.room_temp.frame, text="실온")
        self.notebook.add(self.cart.frame, text="장바구니")
        self.notebook.add(self.my_tab.frame, text="마이페이지")
        self.notebook.add(self.sign_up_tab.frame, text="회원가입")
        self.notebook.add(
            self.add_ingredient_tab.frame, text="재료 추가"
        )  # 재료 추가 탭 추가

        #notebook.pack(expand=True, fill="both")

    def switch_to_signup(self):
        # 회원가입 탭으로 전환
        self.notebook.select(self.sign_up_tab.frame)


# 프로그램 실행
if __name__ == "__main__":
    root = tk.Tk()
    app = FreshlyApp(root)
    root.mainloop()
