f = open('student_gui.py', 'r', encoding='utf-8')
c = f.read()
f.close()

# Find the position after theme initialization
import re
match = re.search(r'self\.colors = self\.theme_manager\.get_theme\(self\.current_theme\)', c)

if match and 'self.create_login_screen()' not in c[:5000]:
    pos = match.end()
    c = c[:pos] + '\n\n        self.create_login_screen()' + c[pos:]
    
    f = open('student_gui.py', 'w', encoding='utf-8')
    f.write(c)
    f.close()
    print('Fixed - Added create_login_screen() call')
else:
    print('Already has create_login_screen() or pattern not found')
