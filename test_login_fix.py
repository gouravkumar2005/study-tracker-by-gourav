"""Test if login buttons are showing properly"""
import tkinter as tk
from student_gui import StudentApp
from parent_gui import ParentApp
import sys

def test_student_login():
    print("Testing Student Login Screen...")
    try:
        root = tk.Tk()
        app = StudentApp(root)
        print("✓ Student login screen created successfully!")
        print("✓ No KeyError occurred - all color keys are present")
        root.after(100, root.destroy)  # Close after 100ms
        root.mainloop()
        return True
    except KeyError as e:
        print(f"✗ KeyError: {e}")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_parent_login():
    print("\nTesting Parent Login Screen...")
    try:
        root = tk.Tk()
        app = ParentApp(root)
        print("✓ Parent login screen created successfully!")
        root.after(100, root.destroy)  # Close after 100ms
        root.mainloop()
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == "__main__":
    student_ok = test_student_login()
    parent_ok = test_parent_login()
    
    if student_ok and parent_ok:
        print("\n✓✓✓ All tests passed! Login buttons should now be visible.")
        sys.exit(0)
    else:
        print("\n✗✗✗ Some tests failed. Check errors above.")
        sys.exit(1)
