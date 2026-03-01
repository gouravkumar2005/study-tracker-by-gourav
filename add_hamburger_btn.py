f = open('student_gui.py', 'r', encoding='utf-8')
lines = f.readlines()
f.close()

# Find create_main_screen method
for i, line in enumerate(lines):
    if 'def create_main_screen(self):' in line:
        # Add hamburger button after method definition
        insert_pos = i + 2  # After method def and try block
        
        hamburger_code = """        # Hamburger Menu Button (top-left corner)
        menu_btn = tk.Button(self.root, text="☰", command=self.create_hamburger_menu,
                            font=("Segoe UI", 20, "bold"), bg=self.colors['primary'],
                            fg="white", relief=tk.FLAT, cursor="hand2", width=3, height=1)
        menu_btn.place(x=10, y=10)

"""
        lines.insert(insert_pos, hamburger_code)
        break

f = open('student_gui.py', 'w', encoding='utf-8')
f.writelines(lines)
f.close()

print('Hamburger button added successfully')
