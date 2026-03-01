import tkinter as tk
try:
    import student_gui
    
    root = tk.Tk()
    root.withdraw()
    
    student_window = tk.Toplevel(root)
    app = student_gui.StudentApp(student_window)
    
    print("Student GUI loaded successfully!")
    print("Login screen should be visible")
    
    root.after(3000, root.quit)  # Close after 3 seconds
    root.mainloop()
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
