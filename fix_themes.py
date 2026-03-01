import re

# Read the file
with open('student_gui.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the theme cost logic
old_pattern = r"if theme != 'light':\s+cost = 500 if theme == 'dark' else 750\s+tk\.Label\(theme_box, text=f\"🪙 \{cost\}\""
new_code = """if theme in ['light', 'dark']:
                tk.Label(theme_box, text="FREE", font=("Segoe UI", 9, "bold"), 
                        bg=self.colors['bg_light'], fg=self.colors['success']).pack(side=tk.RIGHT, padx=10)
            else:
                tk.Label(theme_box, text=f"🪙 750\""""

content = re.sub(old_pattern, new_code, content)

# Write back
with open('student_gui.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed!")
