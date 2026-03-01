f = open('student_gui.py', 'r', encoding='utf-8')
c = f.read()
f.close()

start = c.find('    def create_settings_tab(self):')
if start != -1:
    end = c.find('    def ', start + 10)
    if end != -1:
        c = c[:start] + c[end:]
        f = open('student_gui.py', 'w', encoding='utf-8')
        f.write(c)
        f.close()
        print('Settings tab removed successfully')
    else:
        print('Could not find end of settings tab')
else:
    print('Settings tab not found')
