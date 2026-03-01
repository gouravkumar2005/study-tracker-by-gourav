import sqlite3
from datetime import datetime

class NotesAndTodoSystem:
    def __init__(self, db_name='study_tracker.db'):
        self.db_name = db_name
        self._init_tables()
    
    def _init_tables(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        c.execute('''CREATE TABLE IF NOT EXISTS study_notes (
                        id INTEGER PRIMARY KEY,
                        username TEXT,
                        subject TEXT,
                        title TEXT,
                        content TEXT,
                        created_at TEXT,
                        updated_at TEXT
                     )''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS todo_tasks (
                        id INTEGER PRIMARY KEY,
                        username TEXT,
                        task TEXT,
                        subject TEXT,
                        priority TEXT,
                        due_date TEXT,
                        completed BOOLEAN DEFAULT 0,
                        created_at TEXT
                     )''')
        
        conn.commit()
        conn.close()
    
    def add_note(self, username, subject, title, content):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        c.execute('''INSERT INTO study_notes (username, subject, title, content, created_at, updated_at)
                     VALUES (?, ?, ?, ?, ?, ?)''', (username, subject, title, content, now, now))
        conn.commit()
        conn.close()
        return True
    
    def get_notes(self, username, subject=None):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        if subject:
            c.execute('SELECT * FROM study_notes WHERE username=? AND subject=? ORDER BY updated_at DESC', 
                     (username, subject))
        else:
            c.execute('SELECT * FROM study_notes WHERE username=? ORDER BY updated_at DESC', (username,))
        notes = c.fetchall()
        conn.close()
        return notes
    
    def add_task(self, username, task, subject, priority, due_date):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        c.execute('''INSERT INTO todo_tasks (username, task, subject, priority, due_date, created_at)
                     VALUES (?, ?, ?, ?, ?, ?)''', (username, task, subject, priority, due_date, now))
        conn.commit()
        conn.close()
        return True
    
    def get_tasks(self, username, completed=False):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('SELECT * FROM todo_tasks WHERE username=? AND completed=? ORDER BY due_date', 
                 (username, 1 if completed else 0))
        tasks = c.fetchall()
        conn.close()
        return tasks
    
    def complete_task(self, task_id):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('UPDATE todo_tasks SET completed=1 WHERE id=?', (task_id,))
        conn.commit()
        conn.close()
        return True
