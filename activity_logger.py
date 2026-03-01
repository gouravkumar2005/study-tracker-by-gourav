import sqlite3
import os
from datetime import datetime
from PIL import ImageGrab
import win32gui
import win32process
import psutil

class ActivityLogger:
    def __init__(self, db_name='study_tracker.db'):
        self.db_name = db_name
        self.screenshot_dir = 'session_screenshots'
        if not os.path.exists(self.screenshot_dir):
            os.makedirs(self.screenshot_dir)
    
    def log_activity(self, username, session_id, activity_type, app_name='', window_title='', url='', screenshot_path=''):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        c.execute('''INSERT INTO activity_log 
                     (username, session_id, timestamp, activity_type, app_name, window_title, url, screenshot_path)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                  (username, session_id, timestamp, activity_type, app_name, window_title, url, screenshot_path))
        conn.commit()
        conn.close()
    
    def take_screenshot(self, username, session_id, activity_detected=''):
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{username}_{session_id}_{timestamp}.png"
            filepath = os.path.join(self.screenshot_dir, filename)
            
            screenshot = ImageGrab.grab()
            screenshot.save(filepath)
            
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute('''INSERT INTO session_screenshots 
                         (username, session_id, timestamp, screenshot_path, activity_detected)
                         VALUES (?, ?, ?, ?, ?)''',
                      (username, session_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
                       filepath, activity_detected))
            conn.commit()
            conn.close()
            
            return filepath
        except Exception as e:
            print(f"Screenshot error: {e}")
            return None
    
    def get_active_window_info(self):
        try:
            hwnd = win32gui.GetForegroundWindow()
            window_title = win32gui.GetWindowText(hwnd)
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            process = psutil.Process(pid)
            app_name = process.name()
            return app_name, window_title
        except:
            return 'Unknown', 'Unknown'
    
    def get_session_activity_log(self, username, session_id):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('''SELECT timestamp, activity_type, app_name, window_title, url 
                     FROM activity_log 
                     WHERE username=? AND session_id=? 
                     ORDER BY timestamp''',
                  (username, session_id))
        activities = c.fetchall()
        conn.close()
        return activities
    
    def get_session_screenshots(self, username, session_id):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('''SELECT timestamp, screenshot_path, activity_detected 
                     FROM session_screenshots 
                     WHERE username=? AND session_id=? 
                     ORDER BY timestamp''',
                  (username, session_id))
        screenshots = c.fetchall()
        conn.close()
        return screenshots
    
    def get_latest_session_id(self, username):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('SELECT MAX(id) FROM study_sessions WHERE username=?', (username,))
        result = c.fetchone()
        conn.close()
        return result[0] if result[0] else 0
