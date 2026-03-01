import tkinter as tk
from tkinter import messagebox
import webbrowser
import student_gui
import parent_gui

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Study Tracker App")
        self.root.geometry("400x300")

        self.create_main_screen()

    def create_main_screen(self):
        # Create a main frame for better layout
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        tk.Label(main_frame, text="Welcome to Study Tracker", font=("Arial", 20, "bold"), bg="#f0f0f0").pack(pady=40)

        button_style = {"font": ("Arial", 12), "width": 20, "height": 2, "bg": "#4CAF50", "fg": "white", "relief": tk.RAISED}

        tk.Button(main_frame, text="Student Login", command=self.open_student_app, **button_style).pack(pady=15)
        tk.Button(main_frame, text="Parent Login", command=self.open_parent_app, **button_style).pack(pady=15)

        tk.Button(main_frame, text="Exit", command=self.root.quit, **button_style).pack(pady=30)

    def open_student_app(self):
        student_window = tk.Toplevel(self.root)
        student_app = student_gui.StudentApp(student_window)

    def open_parent_app(self):
        parent_window = tk.Toplevel(self.root)
        parent_app = parent_gui.ParentApp(parent_window)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
