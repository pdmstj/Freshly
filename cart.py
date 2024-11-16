# 장바구니 (구매 전 메모용)
import tkinter as tk
from tkinter import messagebox
import os
import pickle


class Cart:
    def __init__(self, parent):
        """Cart 클래스 초기화"""
        self.frame = tk.Frame(parent, bg="#E3F2FD")  # 파스텔 하늘색 배경 추가
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)  # 프레임을 화면에 표시

        # 제목 레이블 추가
        title_label = tk.Label(self.frame, text="장바구니 (구매 전 메모용)", font=("Helvetica", 16, "bold"), bg="#E3F2FD", fg="#0D47A1")
        title_label.pack(pady=(0, 10))

        # 재료 입력 필드
        self.ingredient_entry = tk.Entry(self.frame, font=("Helvetica", 12))
        self.ingredient_entry.pack(pady=5, padx=10, fill="x")

        # 장바구니 추가 버튼
        tk.Button(self.frame, text="추가", command=self.add_to_cart, width=10, font=("Helvetica", 12, "bold"), bg="#A5D6A7", fg="#1B5E20", relief="raised", borderwidth=2).pack(pady=5)
        
        # 장바구니 리스트박스
        self.cart_listbox = tk.Listbox(self.frame, font=("Helvetica", 12))
        self.cart_listbox.pack(pady=10, padx=10, fill="both", expand=True)

        # 장바구니 삭제 버튼
        tk.Button(self.frame, text="삭제", command=self.remove_from_cart, width=10, font=("Helvetica", 12, "bold"), bg="#FF8A80", fg="#B71C1C", relief="raised", borderwidth=2).pack(pady=5)

        # 장바구니 로드
        self.load_cart()

    def load_cart(self):
        """장바구니에 있는 재료들을 파일에서 로드하여 Listbox에 표시"""
        if os.path.exists("shopping_cart.pkl"):
            try:
                with open("shopping_cart.pkl", "rb") as f:
                    ingredients = pickle.load(f)
                    
                    # 기존 목록 삭제
                    self.cart_listbox.delete(0, tk.END)

                    # 장바구니 목록을 Listbox에 표시
                    for ingredient in ingredients:
                        self.cart_listbox.insert(tk.END, ingredient)
            except Exception as e:
                messagebox.showerror("오류", f"장바구니를 불러오는 중 오류가 발생했습니다: {e}")

    def add_to_cart(self):
        """입력된 재료를 장바구니에 추가"""
        ingredient_name = self.ingredient_entry.get().strip()
        if not ingredient_name:
            messagebox.showwarning("입력 오류", "추가할 재료 이름을 입력해주세요.")
            return

        try:
            # 장바구니에 재료 추가
            self.cart_listbox.insert(tk.END, ingredient_name)
            messagebox.showinfo("장바구니", "재료가 장바구니에 추가되었습니다!")
            
            # 변경된 장바구니 저장
            self.save_cart()
        except Exception as e:
            messagebox.showerror("오류", f"장바구니에 추가하는 중 오류가 발생했습니다: {e}")

    def remove_from_cart(self):
        """선택된 재료를 장바구니에서 삭제"""
        selected_index = self.cart_listbox.curselection()  # 선택된 항목 인덱스 가져오기
        if not selected_index:
            messagebox.showwarning("선택 오류", "삭제할 재료를 선택해주세요.")
            return

        try:
            # 선택된 재료 삭제
            self.cart_listbox.delete(selected_index)
            messagebox.showinfo("장바구니", "선택한 재료가 장바구니에서 삭제되었습니다!")
            
            # 변경된 장바구니 저장
            self.save_cart()
        except Exception as e:
            messagebox.showerror("오류", f"장바구니에서 삭제하는 중 오류가 발생했습니다: {e}")

    def save_cart(self):
        """장바구니에 있는 재료들을 파일에 저장"""
        try:
            ingredients = self.cart_listbox.get(0, tk.END)
            with open("shopping_cart.pkl", "wb") as f:
                pickle.dump(ingredients, f)
        except Exception as e:
            messagebox.showerror("오류", f"장바구니를 저장하는 중 오류가 발생했습니다: {e}")


# 예시로 Cart 클래스 사용 (루트 윈도우 생성)
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Freshly - 냉장고 관리 애플리케이션")
    root.configure(bg="#E3F2FD")  # 루트 창 배경색 설정

    cart = Cart(root)

    root.mainloop()
