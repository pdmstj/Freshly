# 냉장, 냉동, 실온 처리

import tkinter as tk
from tkinter import ttk, messagebox
from db_connect import connect_to_freshlydb


class Storage:
    def __init__(self, notebook, user, password):
        self.notebook = notebook
        self.user = user
        self.password = password

        # 각 탭을 생성
        self.fridge_tab = tk.Frame(self.notebook)
        self.freezer_tab = tk.Frame(self.notebook)
        self.room_temp_tab = tk.Frame(self.notebook)

        # 탭 추가
        notebook.add(self.fridge_tab, text="냉장")
        notebook.add(self.freezer_tab, text="냉동")
        notebook.add(self.room_temp_tab, text="실온")

        # 각 탭에 맞는 재료 로드
        self.load_ingredients("냉장", self.fridge_tab)
        self.load_ingredients("냉동", self.freezer_tab)
        self.load_ingredients("실온", self.room_temp_tab)

    def load_ingredients(self, storage_type, tab_frame):
        """저장소별로 재료를 로드하여 탭에 표시합니다."""
        try:
            connection = connect_to_freshlydb(self.user, self.password)
            if not connection:
                messagebox.showerror("DB 연결 오류", "데이터베이스에 연결할 수 없습니다.")
                return

            cursor = connection.cursor()

            # 각 저장 유형별로 재료 불러오기
            cursor.execute(
                "SELECT name, expiration_date FROM ingredients WHERE storage_type_id = (SELECT id FROM storage_types WHERE section_name = %s)",
                (storage_type,)
            )
            ingredients = cursor.fetchall()

            # 기존에 있던 위젯들 삭제
            for widget in tab_frame.winfo_children():
                widget.destroy()

            # 재료를 탭에 표시
            for ingredient in ingredients:
                label = tk.Label(tab_frame, text=f"{ingredient[0]} - {ingredient[1]}")
                label.pack(anchor="w", padx=10, pady=2)

        except Exception as e:
            messagebox.showerror("오류", f"재료를 불러오는 중 오류가 발생했습니다: {e}")
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'connection' in locals() and connection.is_connected():
                connection.close()


# 예시로 Storage 클래스 사용 (루트 윈도우 생성)
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Storage Management")

    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill="both")

    # 사용자 정보를 여기에 정의 (root 사용자 예시)
    db_user = "root"
    db_password = "970814"

    storage = Storage(notebook, db_user, db_password)

    root.mainloop()
