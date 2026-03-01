"""
Desktop Activity Monitor - Multi-Signal Fusion Component
Detects study vs distraction based on active applications and user behavior
"""

import time
import threading
from collections import deque
from datetime import datetime

# Platform-specific imports
try:
    import win32gui
    import win32process
    import psutil
    WINDOWS_AVAILABLE = True
except ImportError:
    WINDOWS_AVAILABLE = False
    print("Warning: win32gui not available. Activity monitoring will be simulated.")

try:
    from pynput import mouse, keyboard
    PYNPUT_AVAILABLE = True
except ImportError:
    PYNPUT_AVAILABLE = False
    print("Warning: pynput not available. Input pattern detection will be simulated.")


class ActivityMonitor:
    """
    Monitors desktop activity to detect study vs distraction
    PRIMARY SIGNAL (50% weight) in focus scoring
    """
    
    def __init__(self):
        self.running = False
        self.current_app = None
        self.app_history = deque(maxlen=30)  # Last 30 app samples
        
        # Input pattern tracking
        self.key_presses = deque(maxlen=100)
        self.mouse_clicks = deque(maxlen=50)
        self.mouse_movements = deque(maxlen=50)
        self.scroll_events = deque(maxlen=30)
        
        # Whitelists and blacklists
        self.study_apps = {
            # Browsers (need URL checking for true study detection)
            'chrome.exe', 'firefox.exe', 'msedge.exe', 'brave.exe',
            # Document editors
            'winword.exe', 'excel.exe', 'powerpnt.exe',  # MS Office
            'acrord32.exe', 'acrobat.exe',  # PDF readers
            'onenote.exe', 'notion.exe',
            # Code editors
            'code.exe', 'pycharm64.exe', 'devenv.exe', 'sublime_text.exe',
            # Study-specific
            'anki.exe', 'obsidian.exe', 'evernote.exe',
            'calibre.exe',  # E-book reader
            # Note-taking
            'notepad.exe', 'notepad++.exe'
        }
        
        self.distraction_apps = {
            # Social media
            'discord.exe', 'telegram.exe', 'whatsapp.exe', 'slack.exe',
            # Gaming
            'steam.exe', 'epicgameslauncher.exe', 'riotclientservices.exe',
            'leagueclient.exe', 'valorant.exe', 'gta5.exe', 'minecraft.exe',
            # Entertainment
            'spotify.exe', 'netflix.exe', 'vlc.exe', 'wmplayer.exe',
            # Streaming
            'obs64.exe', 'streamlabs obs.exe'
        }
        
        # Browser distraction detection (for URL analysis if available)
        self.distraction_keywords = [
            'youtube', 'netflix', 'instagram', 'facebook', 'twitter',
            'tiktok', 'reddit', 'twitch', 'gaming', 'shorts', 'reels'
        ]
        
        self.study_keywords = [
            'docs.google', 'github', 'stackoverflow', 'coursera',
            'udemy', 'khan', 'edx', 'wikipedia', 'scholar.google'
        ]
        
        # Listeners
        self.keyboard_listener = None
        self.mouse_listener = None
        
    def start_monitoring(self):
        """Start background monitoring"""
        self.running = True
        
        if PYNPUT_AVAILABLE:
            # Start input listeners
            self.keyboard_listener = keyboard.Listener(
                on_press=self._on_key_press
            )
            self.mouse_listener = mouse.Listener(
                on_click=self._on_mouse_click,
                on_move=self._on_mouse_move,
                on_scroll=self._on_mouse_scroll
            )
            self.keyboard_listener.start()
            self.mouse_listener.start()
        
        # Start app monitoring thread
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop all monitoring"""
        self.running = False
        
        if self.keyboard_listener:
            self.keyboard_listener.stop()
        if self.mouse_listener:
            self.mouse_listener.stop()
    
    def _monitor_loop(self):
        """Continuous monitoring loop - runs every 2 seconds"""
        while self.running:
            self.current_app = self._get_active_application()
            self.app_history.append({
                'app': self.current_app,
                'timestamp': time.time()
            })
            time.sleep(2)  # Check every 2 seconds (efficiency)
    
    def _get_active_application(self):
        """Get currently active application name"""
        if not WINDOWS_AVAILABLE:
            return 'simulated.exe'
        
        try:
            window = win32gui.GetForegroundWindow()
            _, pid = win32process.GetWindowThreadProcessId(window)
            process = psutil.Process(pid)
            return process.name().lower()
        except:
            return 'unknown.exe'
    
    def _on_key_press(self, key):
        """Track keyboard activity"""
        self.key_presses.append({
            'timestamp': time.time(),
            'key': str(key)
        })
    
    def _on_mouse_click(self, x, y, button, pressed):
        """Track mouse clicks"""
        if pressed:
            self.mouse_clicks.append({
                'timestamp': time.time(),
                'x': x,
                'y': y
            })
    
    def _on_mouse_move(self, x, y):
        """Track mouse movement"""
        self.mouse_movements.append({
            'timestamp': time.time(),
            'x': x,
            'y': y
        })
    
    def _on_mouse_scroll(self, x, y, dx, dy):
        """Track scroll events"""
        self.scroll_events.append({
            'timestamp': time.time(),
            'dy': dy
        })
    
    def get_app_usage_score(self):
        """
        Calculate app usage score (0-100)
        100 = Definitely studying
        0 = Definitely distracted
        
        This is the PRIMARY SIGNAL (50% weight)
        """
        if not self.app_history:
            return 50  # Unknown
        
        recent_apps = list(self.app_history)[-10:]  # Last 20 seconds
        
        study_count = 0
        distraction_count = 0
        unknown_count = 0
        
        for record in recent_apps:
            app = record['app']
            
            if app in self.distraction_apps:
                distraction_count += 1
            elif app in self.study_apps:
                study_count += 1
            else:
                unknown_count += 1
        
        total = len(recent_apps)
        
        # Calculate weighted score
        if distraction_count > total * 0.5:  # More than 50% distraction apps
            return 20  # Clearly distracted
        elif distraction_count > total * 0.3:  # 30-50% distraction
            return 40
        elif study_count > total * 0.7:  # More than 70% study apps
            return 90
        elif study_count > total * 0.5:  # 50-70% study apps
            return 70
        else:  # Mixed or unknown
            return 50
    
    def get_interaction_pattern_score(self):
        """
        Analyze keyboard/mouse patterns (25% weight)
        Study patterns: Steady typing, slow scrolling, focused clicks
        Distraction: Rapid clicks, fast scrolling, erratic movement
        """
        if not PYNPUT_AVAILABLE:
            return 50  # Unknown
        
        now = time.time()
        recent_window = 30  # Last 30 seconds
        
        # Get recent events
        recent_keys = [k for k in self.key_presses if now - k['timestamp'] < recent_window]
        recent_clicks = [c for c in self.mouse_clicks if now - c['timestamp'] < recent_window]
        recent_scrolls = [s for s in self.scroll_events if now - s['timestamp'] < recent_window]
        
        score = 50  # Start neutral
        
        # 1. Typing analysis
        if len(recent_keys) > 0:
            # Steady typing (15-60 keys/min) = studying
            keys_per_min = len(recent_keys) / (recent_window / 60)
            
            if 15 <= keys_per_min <= 60:
                score += 15  # Good study typing
            elif keys_per_min < 5:
                score -= 10  # Too little typing (watching/idle)
            elif keys_per_min > 100:
                score -= 15  # Gaming-like rapid typing
        
        # 2. Click analysis
        if len(recent_clicks) > 0:
            # Calculate click rate
            clicks_per_min = len(recent_clicks) / (recent_window / 60)
            
            if clicks_per_min < 10:
                score += 10  # Normal clicking
            elif clicks_per_min > 30:
                score -= 20  # Gaming/rapid clicking
        
        # 3. Scroll analysis
        if len(recent_scrolls) > 2:
            # Calculate scroll speed
            scroll_speeds = []
            for i in range(1, len(recent_scrolls)):
                time_diff = recent_scrolls[i]['timestamp'] - recent_scrolls[i-1]['timestamp']
                if time_diff > 0:
                    scroll_speeds.append(abs(recent_scrolls[i]['dy']) / time_diff)
            
            if scroll_speeds:
                avg_speed = sum(scroll_speeds) / len(scroll_speeds)
                
                # Slow scrolling (reading) = studying
                # Fast scrolling (reels/shorts) = distraction
                if avg_speed < 5:
                    score += 15  # Slow, careful scrolling (reading)
                elif avg_speed > 20:
                    score -= 20  # Rapid scrolling (reels/entertainment)
        
        return max(0, min(100, score))
    
    def get_session_stability(self):
        """
        Measure how stable the user has been in study apps
        Returns 0-100 where higher = more stable/focused
        """
        if len(self.app_history) < 5:
            return 50
        
        # Count app switches in last 60 seconds
        recent = [r for r in self.app_history if time.time() - r['timestamp'] < 60]
        
        if not recent:
            return 50
        
        app_switches = 0
        last_app = recent[0]['app']
        
        for record in recent[1:]:
            if record['app'] != last_app:
                app_switches += 1
                last_app = record['app']
        
        # Fewer switches = more stable
        if app_switches == 0:
            return 100
        elif app_switches < 3:
            return 75
        elif app_switches < 6:
            return 50
        else:
            return 25  # Too many switches = distraction
    
    def get_activity_summary(self):
        """Get human-readable summary of current activity"""
        app_score = self.get_app_usage_score()
        pattern_score = self.get_interaction_pattern_score()
        
        if app_score > 70 and pattern_score > 60:
            return "Actively studying"
        elif app_score < 40:
            return "Distracted - non-study application"
        elif pattern_score < 40:
            return "Distracted - entertainment pattern detected"
        else:
            return "Mixed activity"