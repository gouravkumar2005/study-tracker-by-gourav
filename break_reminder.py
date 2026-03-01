import time
from datetime import datetime, timedelta

class BreakReminder:
    def __init__(self):
        self.break_interval = 25 * 60  # 25 minutes (Pomodoro)
        self.break_duration = 5 * 60   # 5 minutes
        self.long_break_interval = 4   # After 4 pomodoros
        self.long_break_duration = 15 * 60  # 15 minutes
        self.pomodoro_count = 0
        self.last_break_time = None
        
    def should_take_break(self, session_start_time, current_focus_score):
        """Determine if break is needed"""
        elapsed = time.time() - session_start_time
        
        # Time-based break (every 25 min)
        if elapsed % self.break_interval < 60:
            return True, "Time for a break! You've been studying for 25 minutes."
        
        # Focus-based break (if focus drops below 40%)
        if current_focus_score < 40:
            return True, "Your focus is dropping. Take a quick break!"
        
        return False, ""
    
    def get_break_exercises(self):
        """Get random break exercise"""
        exercises = [
            {
                'name': '👀 Eye Exercise',
                'duration': 2,
                'steps': [
                    'Look at something 20 feet away',
                    'Blink 10 times slowly',
                    'Roll your eyes clockwise',
                    'Roll your eyes counter-clockwise'
                ]
            },
            {
                'name': '🧘 Breathing Exercise',
                'duration': 3,
                'steps': [
                    'Breathe in for 4 seconds',
                    'Hold for 4 seconds',
                    'Breathe out for 4 seconds',
                    'Repeat 5 times'
                ]
            },
            {
                'name': '💪 Stretch Exercise',
                'duration': 3,
                'steps': [
                    'Stand up and stretch arms',
                    'Touch your toes',
                    'Neck rolls (left and right)',
                    'Shoulder shrugs'
                ]
            },
            {
                'name': '💧 Hydration Break',
                'duration': 2,
                'steps': [
                    'Drink a glass of water',
                    'Walk around for 1 minute',
                    'Splash water on face',
                    'Take deep breaths'
                ]
            }
        ]
        
        import random
        return random.choice(exercises)
    
    def start_break_timer(self, duration_minutes):
        """Start break countdown"""
        return time.time() + (duration_minutes * 60)
