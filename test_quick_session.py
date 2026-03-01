import tkinter as tk
from tkinter import messagebox
import student_gui

root = tk.Tk()
root.withdraw()

# Create student window
student_window = tk.Toplevel(root)
app = student_gui.StudentApp(student_window)

# Simulate login
app.current_user = "test_student"

# Test quick session
print("Testing 25min quick session...")
try:
    app.quick_session(0.5)
    print("Quick session started successfully!")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

root.mainloop()
