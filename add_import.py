f = open('student_gui.py', 'r', encoding='utf-8')
lines = f.readlines()
f.close()

if 'import sqlite3\n' not in lines:
    lines.insert(10, 'import sqlite3\n')
    f = open('student_gui.py', 'w', encoding='utf-8')
    f.writelines(lines)
    f.close()
    print('Added sqlite3 import')
else:
    print('sqlite3 already imported')
