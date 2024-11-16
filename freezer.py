# 냉동고
import tkinter as tk
from tkinter import messagebox
from db_connect import connect_to_freshlydb

class Freezer:
    def __init__(self, parent, user, password):
        self.user = user
        self.password = password
        self.frame = tk.Frame(parent, bg="#E3F2FD")  # 파스텔 하늘색 배경 추가
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        # 냉동고 재료 목록 로딩
        self.load_ingredients()

    def load_ingredients(self):
        """냉동고에 있는 재료 목록을 DB에서 로드하여 표시합니다."""
        # 기존에 있던 위젯들 삭제
        for widget in self.frame.winfo_children():
            widget.destroy()

        # 제목 레이블 추가
        title_label = tk.Label(self.frame, text="냉동고 재료 목록", font=("Helvetica", 16, "bold"), bg="#E3F2FD", fg="#0D47A1")
        title_label.pack(pady=(0, 10))

        # 재료 목록 로드 버튼 추가
        reload_button = tk.Button(
            self.frame,
            text="목록 갱신",
            command=self.load_ingredients,
            bg="#BBDEFB",
            fg="#0D47A1",
            font=("Helvetica", 12, "bold"),
            relief="raised",
            borderwidth=2
        )
        reload_button.pack(pady=5)

        # 삭제 버튼 추가
        delete_button = tk.Button(
            self.frame,
            text="선택 항목 삭제",
            command=self.remove_ingredient,
            bg="#FF8A80",
            fg="#B71C1C",
            font=("Helvetica", 12, "bold"),
            relief="raised",
            borderwidth=2
        )
        delete_button.pack(pady=5)

        # DB 연결
        connection = connect_to_freshlydb(self.user, self.password)
        if not connection:
            messagebox.showerror("DB 연결 오류", "데이터베이스에 연결할 수 없습니다.")
            return

        cursor = connection.cursor()

        # 냉동고 재료 목록을 DB에서 가져오기 (냉동고에 해당하는 재료만)
        cursor.execute("SELECT id, name FROM ingredients WHERE storage_type_id = (SELECT id FROM storage_types WHERE section_name = '냉동')")
        ingredients = cursor.fetchall()

        # 재료 목록 UI에 표시
        self.checkbuttons = []  # 체크박스 리스트 초기화
        for ingredient in ingredients:
            var = tk.IntVar()  # 체크박스 상태를 나타내는 변수
            checkbutton = tk.Checkbutton(self.frame, text=ingredient[1], variable=var, font=("Helvetica", 12), bg="#E3F2FD", anchor="w")
            checkbutton.pack(anchor="w", padx=10, pady=2)
            self.checkbuttons.append((ingredient[0], var, ingredient[1]))  # (ingredient_id, var, ingredient_name)로 저장

        cursor.close()
        connection.close()

    def get_all_ingredients(self):
        """현재 냉동고에 있는 모든 재료의 이름을 반환합니다."""
        return [ingredient[2] for ingredient in self.checkbuttons]

    def remove_ingredient(self):
        """선택한 냉동고 재료를 삭제합니다."""
        connection = connect_to_freshlydb(self.user, self.password)
        if not connection:
            messagebox.showerror("DB 연결 오류", "데이터베이스에 연결할 수 없습니다.")
            return

        cursor = connection.cursor()

        for ingredient_id, var, _ in self.checkbuttons:
            if var.get() == 1:  # 체크박스가 선택되었을 경우
                # 냉동고에서 재료를 삭제 쿼리
                cursor.execute(
                    "DELETE FROM ingredients WHERE id = %s",
                    (ingredient_id,),
                )

        connection.commit()
        cursor.close()
        connection.close()

        messagebox.showinfo("냉동고", "선택한 재료가 냉동고에서 삭제되었습니다!")
        self.load_ingredients()  # 재료 삭제 후, 목록 갱신

# 예시로 Freezer 클래스 사용 (루트 윈도우 생성)
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Freezer Example")
    root.configure(bg="#E3F2FD")  # 루트 창 배경색 설정

    # 사용자 정보를 여기에 정의 (root 사용자 예시)
    user = "root"
    password = "970814"

    freezer = Freezer(root, user, password)

    root.mainloop()
