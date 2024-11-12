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
        notebook = ttk.Notebook(root)

        # 각 탭 클래스 인스턴스화
        self.main_tab = Login(notebook)
        self.fridge = Fridge(notebook)
        self.freezer = Freezer(notebook)
        self.room_temp = RoomTemp(notebook)
        self.cart = Cart(notebook)
        self.my_tab = MyTab(notebook)
        self.sign_up_tab = SignUp(notebook)

        # 재료 추가 탭 인스턴스화 (냉장, 냉동, 실온 클래스 전달)
        self.add_ingredient_tab = AddIngredient(
            notebook, self.fridge, self.freezer, self.room_temp
        )

        notebook.add(self.main_tab.frame, text="메인")
        notebook.add(self.fridge.frame, text="냉장")
        notebook.add(self.freezer.frame, text="냉동")
        notebook.add(self.room_temp.frame, text="실온")
        notebook.add(self.cart.frame, text="장바구니")
        notebook.add(self.my_tab.frame, text="마이페이지")
        notebook.add(self.sign_up_tab.frame, text="회원가입")
        notebook.add(
            self.add_ingredient_tab.frame, text="재료 추가"
        )  # 재료 추가 탭 추가

        notebook.pack(expand=True, fill="both")


# 프로그램 실행
if __name__ == "__main__":
    root = tk.Tk()
    app = FreshlyApp(root)
    root.mainloop()
