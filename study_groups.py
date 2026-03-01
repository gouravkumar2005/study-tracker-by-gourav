import sqlite3
from datetime import datetime

class StudyGroupsSystem:
    def __init__(self, db_name='study_tracker.db'):
        self.db_name = db_name
        self._init_tables()
    
    def _init_tables(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        c.execute('''CREATE TABLE IF NOT EXISTS study_groups (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        description TEXT,
                        created_by TEXT,
                        created_at TEXT,
                        member_count INTEGER DEFAULT 1,
                        thumbnail_path TEXT,
                        group_type TEXT DEFAULT 'public'
                     )''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS group_members (
                        group_id INTEGER,
                        username TEXT,
                        joined_at TEXT,
                        role TEXT DEFAULT 'member',
                        is_online INTEGER DEFAULT 0,
                        PRIMARY KEY(group_id, username)
                     )''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS group_messages (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        group_id INTEGER,
                        username TEXT,
                        message TEXT,
                        timestamp TEXT,
                        is_pinned INTEGER DEFAULT 0,
                        reply_to INTEGER,
                        FOREIGN KEY(group_id) REFERENCES study_groups(id)
                     )''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS message_reactions (
                        message_id INTEGER,
                        username TEXT,
                        emoji TEXT,
                        PRIMARY KEY(message_id, username, emoji)
                     )''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS group_polls (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        group_id INTEGER,
                        question TEXT,
                        options TEXT,
                        created_by TEXT,
                        created_at TEXT
                     )''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS group_challenges (
                        id INTEGER PRIMARY KEY,
                        group_id INTEGER,
                        challenge_name TEXT,
                        target_hours INTEGER,
                        start_date TEXT,
                        end_date TEXT,
                        status TEXT DEFAULT 'active'
                     )''')
        
        conn.commit()
        conn.close()
    
    def create_group(self, name, description, creator, thumbnail_path=None):
        """Create new study group"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        c.execute('''INSERT INTO study_groups (name, description, created_by, created_at, thumbnail_path)
                     VALUES (?, ?, ?, ?, ?)''', (name, description, creator, now, thumbnail_path))
        group_id = c.lastrowid
        
        c.execute('''INSERT INTO group_members (group_id, username, joined_at, role)
                     VALUES (?, ?, ?, 'admin')''', (group_id, creator, now))
        
        conn.commit()
        conn.close()
        return group_id
    
    def join_group(self, group_id, username):
        """Join existing group"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        try:
            c.execute('''INSERT INTO group_members (group_id, username, joined_at)
                         VALUES (?, ?, ?)''', (group_id, username, now))
            c.execute('UPDATE study_groups SET member_count = member_count + 1 WHERE id=?', (group_id,))
            conn.commit()
            conn.close()
            return True
        except:
            conn.close()
            return False
    
    def get_user_groups(self, username):
        """Get groups user is member of"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        c.execute('''SELECT g.id, g.name, g.description, g.member_count, gm.role
                     FROM study_groups g
                     JOIN group_members gm ON g.id = gm.group_id
                     WHERE gm.username = ?''', (username,))
        groups = c.fetchall()
        conn.close()
        return groups
    
    def get_group_info(self, group_id):
        """Get group information"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('SELECT * FROM study_groups WHERE id=?', (group_id,))
        group = c.fetchone()
        conn.close()
        return group
    
    def get_group_members(self, group_id):
        """Get all members of a group"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('SELECT username, role, joined_at FROM group_members WHERE group_id=?', (group_id,))
        members = c.fetchall()
        conn.close()
        return members
    
    def send_message(self, group_id, username, message, reply_to=None):
        """Send message to group with optional reply"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        c.execute('''INSERT INTO group_messages (group_id, username, message, timestamp, reply_to)
                     VALUES (?, ?, ?, ?, ?)''', (group_id, username, message, now, reply_to))
        conn.commit()
        conn.close()
        return True
    
    def pin_message(self, message_id):
        """Pin a message"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('UPDATE group_messages SET is_pinned=1 WHERE id=?', (message_id,))
        conn.commit()
        conn.close()
        return True
    
    def get_pinned_messages(self, group_id):
        """Get pinned messages"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('''SELECT id, username, message, timestamp FROM group_messages 
                     WHERE group_id=? AND is_pinned=1''', (group_id,))
        messages = c.fetchall()
        conn.close()
        return messages
    
    def add_reaction(self, message_id, username, emoji):
        """Add emoji reaction to message"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        try:
            c.execute('INSERT INTO message_reactions VALUES (?, ?, ?)', (message_id, username, emoji))
            conn.commit()
            conn.close()
            return True
        except:
            conn.close()
            return False
    
    def get_reactions(self, message_id):
        """Get all reactions for a message"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('SELECT emoji, COUNT(*) FROM message_reactions WHERE message_id=? GROUP BY emoji', (message_id,))
        reactions = c.fetchall()
        conn.close()
        return reactions
    
    def create_poll(self, group_id, username, question, options):
        """Create a poll in group"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        options_str = '|'.join(options)
        
        c.execute('''INSERT INTO group_polls (group_id, question, options, created_by, created_at)
                     VALUES (?, ?, ?, ?, ?)''', (group_id, question, options_str, username, now))
        conn.commit()
        conn.close()
        return True
    
    def set_user_online(self, group_id, username, is_online=True):
        """Set user online/offline status"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('UPDATE group_members SET is_online=? WHERE group_id=? AND username=?', 
                  (1 if is_online else 0, group_id, username))
        conn.commit()
        conn.close()
        return True
    
    def get_online_members(self, group_id):
        """Get online members count"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('SELECT COUNT(*) FROM group_members WHERE group_id=? AND is_online=1', (group_id,))
        count = c.fetchone()[0]
        conn.close()
        return count
    
    def get_messages(self, group_id, limit=50):
        """Get recent messages from group"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('''SELECT username, message, timestamp FROM group_messages 
                     WHERE group_id=? ORDER BY id DESC LIMIT ?''', (group_id, limit))
        messages = c.fetchall()
        conn.close()
        return list(reversed(messages))  # Oldest first
    
    def get_group_leaderboard(self, group_id):
        """Get group leaderboard"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        c.execute('''SELECT gm.username, 
                            COALESCE(SUM(ss.hours), 0) as total_hours,
                            COALESCE(AVG(ss.focus_score), 0) as avg_focus
                     FROM group_members gm
                     LEFT JOIN study_sessions ss ON gm.username = ss.username
                     WHERE gm.group_id = ?
                     GROUP BY gm.username
                     ORDER BY total_hours DESC''', (group_id,))
        
        leaderboard = c.fetchall()
        conn.close()
        return leaderboard
    
    def update_group_thumbnail(self, group_id, thumbnail_path):
        """Update group thumbnail"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('UPDATE study_groups SET thumbnail_path=? WHERE id=?', (thumbnail_path, group_id))
        conn.commit()
        conn.close()
        return True
    
    def create_group_challenge(self, group_id, challenge_name, target_hours, days=7):
        """Create group challenge"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        from datetime import timedelta
        start_date = datetime.now().strftime('%Y-%m-%d')
        end_date = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')
        
        c.execute('''INSERT INTO group_challenges 
                     (group_id, challenge_name, target_hours, start_date, end_date)
                     VALUES (?, ?, ?, ?, ?)''', 
                  (group_id, challenge_name, target_hours, start_date, end_date))
        
        conn.commit()
        conn.close()
        return True
