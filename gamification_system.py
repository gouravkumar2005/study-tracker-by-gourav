import sqlite3
from datetime import datetime, timedelta
import random

class GamificationSystem:
    def __init__(self, db_name='study_tracker.db'):
        self.db_name = db_name
        self._init_tables()
    
    def _init_tables(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        # Coins/points table
        c.execute('''CREATE TABLE IF NOT EXISTS user_coins (
                        username TEXT PRIMARY KEY,
                        coins INTEGER DEFAULT 0,
                        total_earned INTEGER DEFAULT 0
                     )''')
        
        # Daily challenges table
        c.execute('''CREATE TABLE IF NOT EXISTS daily_challenges (
                        id INTEGER PRIMARY KEY,
                        username TEXT,
                        date TEXT,
                        challenge_type TEXT,
                        target INTEGER,
                        progress INTEGER DEFAULT 0,
                        completed BOOLEAN DEFAULT 0,
                        reward INTEGER,
                        UNIQUE(username, date, challenge_type)
                     )''')
        
        # Leaderboard table
        c.execute('''CREATE TABLE IF NOT EXISTS leaderboard (
                        username TEXT,
                        week_start TEXT,
                        total_hours REAL,
                        avg_focus REAL,
                        score INTEGER,
                        PRIMARY KEY(username, week_start)
                     )''')
        
        conn.commit()
        conn.close()
    
    def award_coins(self, username, amount, reason):
        """Award coins to user"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        c.execute('''INSERT INTO user_coins (username, coins, total_earned)
                     VALUES (?, ?, ?)
                     ON CONFLICT(username) DO UPDATE SET
                     coins = coins + ?,
                     total_earned = total_earned + ?''',
                  (username, amount, amount, amount, amount))
        
        conn.commit()
        conn.close()
        
        return f"🪙 +{amount} coins! {reason}"
    
    def get_user_coins(self, username):
        """Get user's coin balance"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        c.execute('SELECT coins, total_earned FROM user_coins WHERE username=?', (username,))
        result = c.fetchone()
        conn.close()
        
        return result if result else (0, 0)
    
    def generate_daily_challenges(self, username):
        """Generate daily challenges"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        challenges = [
            {'type': 'study_hours', 'target': 2, 'reward': 50, 'desc': 'Study for 2 hours'},
            {'type': 'perfect_session', 'target': 1, 'reward': 100, 'desc': 'Complete 1 session with 0 warnings'},
            {'type': 'early_bird', 'target': 1, 'reward': 75, 'desc': 'Study before 8 AM'},
            {'type': 'focus_master', 'target': 90, 'reward': 150, 'desc': 'Maintain 90%+ focus'},
            {'type': 'streak_keeper', 'target': 1, 'reward': 50, 'desc': 'Keep your streak alive'}
        ]
        
        # Pick 3 random challenges
        daily_challenges = random.sample(challenges, 3)
        
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        for challenge in daily_challenges:
            c.execute('''INSERT OR IGNORE INTO daily_challenges 
                         (username, date, challenge_type, target, reward)
                         VALUES (?, ?, ?, ?, ?)''',
                      (username, today, challenge['type'], challenge['target'], challenge['reward']))
        
        conn.commit()
        conn.close()
        
        return daily_challenges
    
    def check_challenge_completion(self, username, challenge_type, progress):
        """Check and complete challenges"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        c.execute('''UPDATE daily_challenges 
                     SET progress = ?, completed = CASE WHEN progress >= target THEN 1 ELSE 0 END
                     WHERE username=? AND date=? AND challenge_type=?''',
                  (progress, username, today, challenge_type))
        
        # Check if just completed
        c.execute('''SELECT reward FROM daily_challenges 
                     WHERE username=? AND date=? AND challenge_type=? AND completed=1''',
                  (username, today, challenge_type))
        
        result = c.fetchone()
        conn.commit()
        conn.close()
        
        if result:
            reward = result[0]
            self.award_coins(username, reward, f"Challenge completed: {challenge_type}")
            return True, reward
        
        return False, 0
    
    def get_leaderboard(self, week_start=None):
        """Get weekly leaderboard"""
        if not week_start:
            today = datetime.now()
            week_start = (today - timedelta(days=today.weekday())).strftime('%Y-%m-%d')
        
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        c.execute('''SELECT username, total_hours, avg_focus, score
                     FROM leaderboard
                     WHERE week_start=?
                     ORDER BY score DESC
                     LIMIT 10''', (week_start,))
        
        leaderboard = c.fetchall()
        conn.close()
        
        return leaderboard
    
    def update_leaderboard(self, username, hours, focus_score):
        """Update user's leaderboard score"""
        today = datetime.now()
        week_start = (today - timedelta(days=today.weekday())).strftime('%Y-%m-%d')
        
        # Calculate score: hours * focus_score
        score = int(hours * focus_score)
        
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        c.execute('''INSERT INTO leaderboard (username, week_start, total_hours, avg_focus, score)
                     VALUES (?, ?, ?, ?, ?)
                     ON CONFLICT(username, week_start) DO UPDATE SET
                     total_hours = total_hours + ?,
                     avg_focus = (avg_focus + ?) / 2,
                     score = score + ?''',
                  (username, week_start, hours, focus_score, score, hours, focus_score, score))
        
        conn.commit()
        conn.close()
    
    def get_available_rewards(self):
        """Get list of rewards that can be purchased"""
        return [
            {'name': '🎨 Ocean Theme', 'cost': 0, 'type': 'theme'},
            {'name': '🌲 Forest Theme', 'cost': 0, 'type': 'theme'},
            {'name': '🌅 Sunset Theme', 'cost': 0, 'type': 'theme'},
            {'name': '💜 Purple Theme', 'cost': 0, 'type': 'theme'},
            {'name': '👤 Custom Avatar', 'cost': 1000, 'type': 'avatar'},
            {'name': '🏆 Gold Badge', 'cost': 2000, 'type': 'badge'},
            {'name': '⭐ Premium Features (1 week)', 'cost': 5000, 'type': 'premium'}
        ]
    
    def purchase_reward(self, username, reward_name, cost):
        """Purchase reward with coins"""
        coins, _ = self.get_user_coins(username)
        
        if coins >= cost:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            
            c.execute('UPDATE user_coins SET coins = coins - ? WHERE username=?', (cost, username))
            conn.commit()
            conn.close()
            
            return True, f"✅ Purchased {reward_name}!"
        
        return False, f"❌ Not enough coins! Need {cost - coins} more."
