import tkinter as tk
from tkinter import ttk, messagebox

root = tk.Tk()
root.title("test")
root.geometry("320x540")

label = tk.Label(root, text="안녕하세긔?")
label.pack()


def on_button_click():
    messagebox.showinfo("알림", "클릭클릭")


button = ttk.Button(root, text="클릭하시긔", command=on_button_click)
button.pack()

root.mainloop()
