import sqlite3
from datetime import datetime, timedelta
import json

class AnalyticsEngine:
    def __init__(self, db_name='study_tracker.db'):
        self.db_name = db_name
    
    def get_study_patterns(self, username, days=30):
        """Analyze study patterns"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        # Get hourly distribution
        c.execute('''SELECT strftime('%H', end_time) as hour, COUNT(*), AVG(focus_score)
                     FROM study_sessions 
                     WHERE username=? AND end_time IS NOT NULL
                     GROUP BY hour
                     ORDER BY hour''', (username,))
        hourly_data = c.fetchall()
        
        # Best and worst study times
        best_time = max(hourly_data, key=lambda x: x[2]) if hourly_data else None
        worst_time = min(hourly_data, key=lambda x: x[2]) if hourly_data else None
        
        conn.close()
        
        return {
            'hourly_distribution': hourly_data,
            'best_time': f"{best_time[0]}:00" if best_time else "N/A",
            'worst_time': f"{worst_time[0]}:00" if worst_time else "N/A",
            'best_focus': round(best_time[2], 1) if best_time else 0,
            'worst_focus': round(worst_time[2], 1) if worst_time else 0
        }
    
    def get_productivity_heatmap(self, username, weeks=4):
        """Generate productivity heatmap data"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        end_date = datetime.now()
        start_date = end_date - timedelta(weeks=weeks)
        
        c.execute('''SELECT date, SUM(hours), AVG(focus_score)
                     FROM study_sessions
                     WHERE username=? AND date >= ?
                     GROUP BY date
                     ORDER BY date''', (username, start_date.strftime('%Y-%m-%d')))
        
        heatmap_data = {}
        for row in c.fetchall():
            date, hours, focus = row
            heatmap_data[date] = {
                'hours': hours,
                'focus': round(focus, 1) if focus else 0,
                'productivity': round((hours * focus) / 100, 2) if focus else 0
            }
        
        conn.close()
        return heatmap_data
    
    def get_focus_trends(self, username, days=7):
        """Get focus score trends"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        c.execute('''SELECT date, AVG(focus_score), COUNT(*)
                     FROM study_sessions
                     WHERE username=? AND date >= ?
                     GROUP BY date
                     ORDER BY date''', (username, start_date.strftime('%Y-%m-%d')))
        
        trends = c.fetchall()
        conn.close()
        
        return trends
    
    def get_distraction_analysis(self, username):
        """Analyze common distractions"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        c.execute('''SELECT app_name, COUNT(*) as count
                     FROM activity_log
                     WHERE username=? AND activity_type='APP_USAGE'
                     GROUP BY app_name
                     ORDER BY count DESC
                     LIMIT 10''', (username,))
        
        top_apps = c.fetchall()
        conn.close()
        
        return top_apps
    
    def predict_best_study_time(self, username):
        """AI prediction for best study time"""
        patterns = self.get_study_patterns(username)
        
        # Simple prediction based on historical data
        best_hour = int(patterns['best_time'].split(':')[0]) if patterns['best_time'] != "N/A" else 9
        
        recommendations = []
        
        if 6 <= best_hour <= 9:
            recommendations.append("You're a morning person! Study between 6-9 AM")
        elif 10 <= best_hour <= 14:
            recommendations.append("You focus best in late morning. Study 10 AM - 2 PM")
        elif 15 <= best_hour <= 19:
            recommendations.append("Afternoon is your peak time. Study 3-7 PM")
        else:
            recommendations.append("You're a night owl! Study after 8 PM")
        
        return recommendations
    
    def generate_weekly_report(self, username):
        """Generate comprehensive weekly report"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        week_start = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        
        c.execute('''SELECT 
                        COUNT(*) as sessions,
                        SUM(hours) as total_hours,
                        AVG(focus_score) as avg_focus,
                        SUM(warnings) as total_warnings
                     FROM study_sessions
                     WHERE username=? AND date >= ?''', (username, week_start))
        
        stats = c.fetchone()
        conn.close()
        
        return {
            'sessions': stats[0] or 0,
            'total_hours': round(stats[1] or 0, 1),
            'avg_focus': round(stats[2] or 0, 1),
            'total_warnings': stats[3] or 0,
            'grade': self._calculate_grade(stats[2] or 0, stats[3] or 0)
        }
    
    def _calculate_grade(self, avg_focus, warnings):
        """Calculate performance grade"""
        if avg_focus >= 90 and warnings < 5:
            return "A+"
        elif avg_focus >= 80 and warnings < 10:
            return "A"
        elif avg_focus >= 70 and warnings < 15:
            return "B"
        elif avg_focus >= 60:
            return "C"
        else:
            return "D"
