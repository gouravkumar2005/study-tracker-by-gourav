import sqlite3
import os

class Database:
    def __init__(self, db_name='study_tracker.db'):
        self.db_name = db_name
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        # Users table
        c.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        username TEXT UNIQUE,
                        password TEXT,
                        role TEXT,
                        parent_username TEXT
                     )''')

        # Study sessions table
        c.execute('''CREATE TABLE IF NOT EXISTS study_sessions (
                        id INTEGER PRIMARY KEY,
                        username TEXT,
                        date TEXT,
                        hours REAL,
                        completed BOOLEAN
                     )''')

        # Progress table
        c.execute('''CREATE TABLE IF NOT EXISTS progress (
                        username TEXT PRIMARY KEY,
                        total_hours REAL,
                        current_streak INTEGER,
                        badges TEXT
                     )''')

        # Badges table
        c.execute('''CREATE TABLE IF NOT EXISTS badges (
                        id INTEGER PRIMARY KEY,
                        username TEXT,
                        badge_id TEXT,
                        badge_name TEXT,
                        earned_date TEXT,
                        UNIQUE(username, badge_id)
                     )''')

        conn.commit()
        
        # Migrate existing database to add new columns
        self._migrate_database(c)
        
        conn.commit()
        conn.close()

    def _migrate_database(self, cursor):
        """Add new columns to existing tables if they don't exist"""
        try:
            # Add level and xp columns to users table if they don't exist
            cursor.execute("PRAGMA table_info(users)")
            columns = [col[1] for col in cursor.fetchall()]
            
            if 'level' not in columns:
                cursor.execute("ALTER TABLE users ADD COLUMN level INTEGER DEFAULT 1")
            if 'xp' not in columns:
                cursor.execute("ALTER TABLE users ADD COLUMN xp INTEGER DEFAULT 0")
            if 'profile_photo' not in columns:
                cursor.execute("ALTER TABLE users ADD COLUMN profile_photo TEXT")
            
            # Add new columns to study_sessions if they don't exist
            cursor.execute("PRAGMA table_info(study_sessions)")
            columns = [col[1] for col in cursor.fetchall()]
            
            if 'warnings' not in columns:
                cursor.execute("ALTER TABLE study_sessions ADD COLUMN warnings INTEGER DEFAULT 0")
            if 'focus_score' not in columns:
                cursor.execute("ALTER TABLE study_sessions ADD COLUMN focus_score REAL DEFAULT 100")
            if 'end_time' not in columns:
                cursor.execute("ALTER TABLE study_sessions ADD COLUMN end_time TEXT")
            if 'session_type' not in columns:
                cursor.execute("ALTER TABLE study_sessions ADD COLUMN session_type TEXT DEFAULT 'regular'")
        except Exception as e:
            print(f"Migration warning: {e}")
            # Continue anyway - tables might not exist yet

    def register_user(self, username, password, role, parent_username=None):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password, role, parent_username) VALUES (?, ?, ?, ?)",
                      (username, password, role, parent_username))
            c.execute("INSERT INTO progress (username, total_hours, current_streak, badges) VALUES (?, 0, 0, '')",
                      (username,))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    def authenticate_user(self, username, password, role):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=? AND role=?", (username, password, role))
        user = c.fetchone()
        conn.close()
        return user is not None

    def update_study_hours(self, username, hours, warnings=0, focus_score=100, session_type='regular'):
        from datetime import datetime
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        today = datetime.now().strftime('%Y-%m-%d')
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Update total hours
        c.execute("UPDATE progress SET total_hours = total_hours + ? WHERE username = ?", (hours, username))

        # Insert study session with new columns
        try:
            c.execute("""INSERT INTO study_sessions 
                         (username, date, hours, completed, warnings, focus_score, end_time, session_type)
                         VALUES (?, ?, ?, 1, ?, ?, ?, ?)""", 
                     (username, today, hours, warnings, focus_score, current_time, session_type))
        except sqlite3.OperationalError:
            # Fallback for old schema
            c.execute("""INSERT INTO study_sessions (username, date, hours, completed)
                         VALUES (?, ?, ?, 1)""", (username, today, hours))

        # Add XP
        xp_earned = int(hours * 100)
        if warnings == 0:
            xp_earned = int(xp_earned * 1.5)
        
        try:
            c.execute("UPDATE users SET xp = xp + ? WHERE username = ?", (xp_earned, username))
            
            # Check for level up
            c.execute("SELECT xp, level FROM users WHERE username = ?", (username,))
            result = c.fetchone()
            if result:
                xp, level = result
                new_level = (xp // 1000) + 1
                if new_level > level:
                    c.execute("UPDATE users SET level = ? WHERE username = ?", (new_level, username))
        except:
            pass  # XP columns don't exist yet

        conn.commit()
        conn.close()

        # Update streak
        self.update_streak(username)

    def update_streak(self, username):
        from datetime import datetime, timedelta
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        today = datetime.now().date()
        yesterday = today - timedelta(days=1)

        # Check if user studied yesterday
        c.execute("SELECT COUNT(*) FROM study_sessions WHERE username = ? AND date = ? AND completed = 1",
                  (username, yesterday.strftime('%Y-%m-%d')))
        studied_yesterday = c.fetchone()[0] > 0

        # Check if user studied today
        c.execute("SELECT COUNT(*) FROM study_sessions WHERE username = ? AND date = ? AND completed = 1",
                  (username, today.strftime('%Y-%m-%d')))
        studied_today = c.fetchone()[0] > 0

        if studied_today:
            if studied_yesterday:
                # Continue streak
                c.execute("UPDATE progress SET current_streak = current_streak + 1 WHERE username = ?", (username,))
            else:
                # Start new streak
                c.execute("UPDATE progress SET current_streak = 1 WHERE username = ?", (username,))
        else:
            # Reset streak if no study today
            c.execute("UPDATE progress SET current_streak = 0 WHERE username = ?", (username,))

        conn.commit()
        conn.close()

    def update_streak_on_login(self, username):
        from datetime import datetime, timedelta
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        today = datetime.now().date()

        # Get the last study date
        c.execute("SELECT date FROM study_sessions WHERE username = ? AND completed = 1 ORDER BY date DESC LIMIT 1",
                  (username,))
        last_study_row = c.fetchone()

        if last_study_row:
            last_study_date = datetime.strptime(last_study_row[0], '%Y-%m-%d').date()
            days_since_last_study = (today - last_study_date).days

            if days_since_last_study == 0:
                # Studied today, ensure streak is at least 1
                c.execute("SELECT current_streak FROM progress WHERE username = ?", (username,))
                current_streak = c.fetchone()[0] or 0
                if current_streak == 0:
                    c.execute("UPDATE progress SET current_streak = 1 WHERE username = ?", (username,))
            elif days_since_last_study == 1:
                # Studied yesterday, keep current streak (will increment on today's study)
                pass  # Do not change streak
            else:
                # More than 1 day gap, reset streak
                c.execute("UPDATE progress SET current_streak = 0 WHERE username = ?", (username,))
        else:
            # No previous study, streak is 0
            c.execute("UPDATE progress SET current_streak = 0 WHERE username = ?", (username,))

        conn.commit()
        conn.close()

    def check_and_award_badges(self, username):
        """Comprehensive badge system with multiple achievement types"""
        from datetime import datetime
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        # Get user progress
        c.execute("SELECT total_hours, current_streak FROM progress WHERE username = ?", (username,))
        progress = c.fetchone()
        if not progress:
            conn.close()
            return
        
        total_hours, current_streak = progress

        # Get longest streak
        c.execute("SELECT MAX(current_streak) FROM progress WHERE username = ?", (username,))
        longest_streak_result = c.fetchone()
        longest_streak = longest_streak_result[0] if longest_streak_result[0] else 0

        # Get total sessions and perfect sessions
        c.execute("SELECT COUNT(*) FROM study_sessions WHERE username = ? AND completed = 1", (username,))
        total_sessions = c.fetchone()[0]
        
        try:
            c.execute("SELECT COUNT(*) FROM study_sessions WHERE username = ? AND completed = 1 AND warnings = 0", (username,))
            perfect_sessions = c.fetchone()[0]
        except:
            perfect_sessions = 0  # Column doesn't exist yet

        # Get user level
        try:
            c.execute("SELECT level FROM users WHERE username = ?", (username,))
            level_result = c.fetchone()
            level = level_result[0] if level_result else 1
        except:
            level = 1

        # Get recent session info
        try:
            c.execute("""SELECT date, hours, warnings, strftime('%H', end_time) as hour 
                         FROM study_sessions WHERE username = ? 
                         ORDER BY id DESC LIMIT 1""", (username,))
            recent_session = c.fetchone()
        except:
            recent_session = None  # New columns don't exist

        badges_to_award = []

        # Milestone Badges (based on total hours)
        hour_milestones = [
            ('first_steps', '🎯 First Steps', 1),
            ('getting_started', '📚 Getting Started', 5),
            ('dedicated_learner', '💪 Dedicated Learner', 10),
            ('study_enthusiast', '⭐ Study Enthusiast', 25),
            ('knowledge_seeker', '🔍 Knowledge Seeker', 50),
            ('study_master', '🏆 Study Master', 100),
            ('legendary_scholar', '👑 Legendary Scholar', 250),
            ('ultimate_genius', '🌟 Ultimate Genius', 500),
            ('unstoppable', '🚀 Unstoppable', 1000)
        ]
        
        for badge_id, badge_name, hours_req in hour_milestones:
            if total_hours >= hours_req:
                badges_to_award.append((badge_id, badge_name))

        # Streak Badges
        streak_badges = [
            ('consistent_starter', '🔥 Consistent Starter', 3),
            ('week_warrior', '⚡ Week Warrior', 7),
            ('fortnight_champion', '💥 Fortnight Champion', 14),
            ('monthly_master', '🌙 Monthly Master', 30),
            ('unstoppable_streak', '🎆 Unstoppable Streak', 60),
            ('legendary_streak', '👑 Legendary Streak', 100)
        ]
        
        for badge_id, badge_name, streak_req in streak_badges:
            if current_streak >= streak_req or longest_streak >= streak_req:
                badges_to_award.append((badge_id, badge_name))

        # Session Count Badges
        if total_sessions >= 10:
            badges_to_award.append(('session_starter', '📖 Session Starter'))
        if total_sessions >= 50:
            badges_to_award.append(('session_veteran', '🎓 Session Veteran'))
        if total_sessions >= 100:
            badges_to_award.append(('session_master', '🏅 Session Master'))
        if total_sessions >= 500:
            badges_to_award.append(('session_legend', '🌟 Session Legend'))

        # Perfect Session Badges
        if perfect_sessions >= 5:
            badges_to_award.append(('focus_beginner', '👀 Focus Beginner'))
        if perfect_sessions >= 20:
            badges_to_award.append(('focus_expert', '🎯 Focus Expert'))
        if perfect_sessions >= 50:
            badges_to_award.append(('focus_master', '💎 Focus Master'))

        # Time-based Badges (if recent session exists)
        if recent_session:
            session_date, session_hours, warnings, hour_str = recent_session
            hour = int(hour_str) if hour_str else 12
            
            # Early Bird (before 8 AM)
            if hour < 8:
                badges_to_award.append(('early_bird', '🌅 Early Bird'))
            
            # Night Owl (after 10 PM)
            if hour >= 22:
                badges_to_award.append(('night_owl', '🦉 Night Owl'))
            
            # Marathon Session (5+ hours)
            if session_hours >= 5:
                badges_to_award.append(('marathon', '🏃 Marathon'))
            
            # Speed Demon (< 30 min focused session)
            if session_hours <= 0.5 and warnings == 0:
                badges_to_award.append(('speed_demon', '⚡ Speed Demon'))

            # Weekend Study
            session_datetime = datetime.strptime(session_date, '%Y-%m-%d')
            if session_datetime.weekday() >= 5:  # Saturday or Sunday
                badges_to_award.append(('weekend_warrior', '🎮 Weekend Warrior'))

        # Level Badges
        level_badges = [
            ('level_5', '🥉 Bronze Scholar', 5),
            ('level_10', '🥈 Silver Scholar', 10),
            ('level_15', '🥇 Gold Scholar', 15),
            ('level_25', '💎 Diamond Scholar', 25),
            ('level_50', '👑 Master Scholar', 50)
        ]
        
        for badge_id, badge_name, level_req in level_badges:
            if level >= level_req:
                badges_to_award.append((badge_id, badge_name))

        # Insert new badges
        today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        newly_earned = []
        for badge_id, badge_name in badges_to_award:
            try:
                c.execute("""INSERT OR IGNORE INTO badges (username, badge_id, badge_name, earned_date)
                            VALUES (?, ?, ?, ?)""", (username, badge_id, badge_name, today))
                if c.rowcount > 0:
                    newly_earned.append(badge_name)
            except:
                pass  # Badge already exists

        conn.commit()
        conn.close()
        
        return newly_earned

    def get_earned_badges(self, username):
        """Get all earned badges for a user"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        try:
            c.execute("SELECT badge_id, badge_name, earned_date FROM badges WHERE username = ? ORDER BY earned_date DESC", 
                     (username,))
            badges = c.fetchall()
            conn.close()
            return [{'id': b[0], 'name': b[1], 'date': b[2]} for b in badges]
        except:
            conn.close()
            return []  # Badges table doesn't exist yet

    def get_student_progress(self, username):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT total_hours, current_streak, badges FROM progress WHERE username = ?", (username,))
        progress = c.fetchone()
        
        # Get user level and XP (with fallback)
        try:
            c.execute("SELECT level, xp FROM users WHERE username = ?", (username,))
            user_info = c.fetchone()
        except:
            user_info = None
        
        # Get badge count (with fallback)
        try:
            c.execute("SELECT COUNT(*) FROM badges WHERE username = ?", (username,))
            badge_count = c.fetchone()[0]
        except:
            badge_count = 0
        
        # Get perfect sessions (with fallback)
        try:
            c.execute("SELECT COUNT(*) FROM study_sessions WHERE username = ? AND completed = 1 AND warnings = 0", (username,))
            perfect_sessions = c.fetchone()[0]
        except:
            perfect_sessions = 0
        
        conn.close()

        if progress:
            level = user_info[0] if user_info else 1
            xp = user_info[1] if user_info else 0
            xp_for_next_level = (level * 1000) - xp
            
            return {
                'Total Hours': progress[0],
                'Current Streak': progress[1],
                'Badges Earned': badge_count,
                'Level': level,
                'XP': xp,
                'XP to Next Level': xp_for_next_level,
                'Perfect Sessions': perfect_sessions,
                "Total Hours": progress[0],
                "Current Streak": progress[1],
                "Badges": progress[2] or "None"
            }
        return {}

    def get_students_for_parent(self, parent_username):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT username FROM users WHERE parent_username = ? AND role = 'student'", (parent_username,))
        students = [row[0] for row in c.fetchall()]
        conn.close()
        return students

    def get_student_report(self, student_username):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT total_hours, current_streak, badges FROM progress WHERE username = ?", (student_username,))
        progress = c.fetchone()

        c.execute("SELECT COUNT(*) FROM study_sessions WHERE username = ? AND completed = 1", (student_username,))
        completed_sessions = c.fetchone()[0]

        conn.close()

        if progress:
            return {
                "Total Hours Studied": progress[0],
                "Current Streak": progress[1],
                "Badges Earned": progress[2] or "None",
                "Completed Sessions": completed_sessions
            }
    
    def update_profile_photo(self, username, photo_path):
        """Update user's profile photo path"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("UPDATE users SET profile_photo = ? WHERE username = ?", (photo_path, username))
        conn.commit()
        conn.close()
    
    def get_profile_photo(self, username):
        """Get user's profile photo path"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT profile_photo FROM users WHERE username = ?", (username,))
        result = c.fetchone()
        conn.close()
        return result[0] if result and result[0] else None
        return {}
