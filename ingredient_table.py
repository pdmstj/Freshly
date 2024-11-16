# 식재료 추가
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from db_connect import connect_to_freshlydb


class IngredientTable:
    def __init__(self, parent, user, password):
        self.user = user
        self.password = password

        self.frame = tk.Frame(parent)
        self.frame.pack(fill="both", expand=True)  # 프레임을 화면에 표시

        # 재료 테이블
        self.table = tk.Listbox(self.frame)
        self.table.pack(fill="both", expand=True)

        # 버튼 추가
        add_button = tk.Button(self.frame, text="재료 추가", command=self.add_ingredient)
        add_button.pack(side="left", padx=5, pady=5)

        delete_button = tk.Button(self.frame, text="재료 삭제", command=self.delete_ingredient)
        delete_button.pack(side="right", padx=5, pady=5)

        self.load_ingredients()

    def load_ingredients(self):
        """DB에서 재료 목록을 불러와서 테이블에 표시합니다."""
        connection = connect_to_freshlydb(self.user, self.password)
        if not connection:
            messagebox.showerror("DB 연결 오류", "데이터베이스에 연결할 수 없습니다.")
            return

        cursor = connection.cursor()
        cursor.execute("SELECT id, name FROM ingredients")
        ingredients = cursor.fetchall()

        # 테이블에 재료 추가
        self.table.delete(0, tk.END)  # 기존 데이터를 모두 삭제하고 새로 추가
        for ingredient in ingredients:
            self.table.insert(tk.END, ingredient[1])  # 재료 이름 테이블에 추가

        cursor.close()
        connection.close()

    def add_ingredient(self):
        """사용자가 새로운 재료를 추가합니다."""
        new_ingredient = simpledialog.askstring("재료 추가", "추가할 재료 이름을 입력하세요:")
        if new_ingredient:
            connection = connect_to_freshlydb(self.user, self.password)
            if not connection:
                messagebox.showerror("DB 연결 오류", "데이터베이스에 연결할 수 없습니다.")
                return

            cursor = connection.cursor()
            cursor.execute("INSERT INTO ingredients (name) VALUES (%s)", (new_ingredient,))
            connection.commit()
            cursor.close()
            connection.close()

            messagebox.showinfo("성공", f"{new_ingredient} 재료가 추가되었습니다.")
            self.load_ingredients()

    def delete_ingredient(self):
        """사용자가 선택한 재료를 삭제합니다."""
        selected_index = self.table.curselection()
        if not selected_index:
            messagebox.showwarning("선택 오류", "삭제할 재료를 선택하세요.")
            return

        ingredient_name = self.table.get(selected_index[0])
        ingredient_id = self.get_ingredient_id_by_name(ingredient_name)

        if ingredient_id:
            connection = connect_to_freshlydb(self.user, self.password)
            if not connection:
                messagebox.showerror("DB 연결 오류", "데이터베이스에 연결할 수 없습니다.")
                return

            cursor = connection.cursor()
            cursor.execute("DELETE FROM ingredients WHERE id = %s", (ingredient_id,))
            connection.commit()
            cursor.close()
            connection.close()

            messagebox.showinfo("성공", f"{ingredient_name} 재료가 삭제되었습니다.")
            self.load_ingredients()

    def get_ingredient_id_by_name(self, name):
        """재료 이름에 해당하는 ingredient_id를 DB에서 찾습니다."""
        connection = connect_to_freshlydb(self.user, self.password)
        if not connection:
            messagebox.showerror("DB 연결 오류", "데이터베이스에 연결할 수 없습니다.")
            return None

        cursor = connection.cursor()
        cursor.execute("SELECT id FROM ingredients WHERE name = %s", (name,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()

        if result:
            return result[0]
        return None


# 예시로 IngredientTable 클래스 사용 (루트 윈도우 생성)
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Ingredient Table Example")

    # 사용자 정보를 여기에 정의 (root 사용자 예시)
    user = "root"
    password = "970814"

    ingredient_table = IngredientTable(root, user, password)

    root.mainloop()
