import sqlite3

db = sqlite3.connect('study_tracker.db')
c = db.cursor()

# Activity log table
c.execute('''CREATE TABLE IF NOT EXISTS activity_log (
                id INTEGER PRIMARY KEY,
                username TEXT,
                session_id INTEGER,
                timestamp TEXT,
                activity_type TEXT,
                app_name TEXT,
                window_title TEXT,
                url TEXT,
                screenshot_path TEXT
             )''')

# Session screenshots table
c.execute('''CREATE TABLE IF NOT EXISTS session_screenshots (
                id INTEGER PRIMARY KEY,
                username TEXT,
                session_id INTEGER,
                timestamp TEXT,
                screenshot_path TEXT,
                activity_detected TEXT
             )''')

db.commit()
db.close()
print("Tables created successfully!")
