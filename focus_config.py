"""
Configuration for Focus Monitoring System
Adjust these values to tune sensitivity and behavior
"""

class FocusConfig:
    """
    Production-grade configuration for study monitoring
    """
    
    # ===== SIGNAL WEIGHTS =====
    # These must sum to 1.0 (100%)
    WEIGHT_APP_USAGE = 0.50        # Desktop application detection (PRIMARY)
    WEIGHT_INTERACTION = 0.25       # Keyboard/mouse patterns
    WEIGHT_EYE_GAZE = 0.15         # Camera eye tracking  
    WEIGHT_HEAD_POSE = 0.10        # Camera head posture
    
    # ===== FOCUS SCORE THRESHOLDS =====
    THRESHOLD_FOCUSED = 80          # 80-100: Student is focused (SILENT)
    THRESHOLD_MILD_DRIFT = 60       # 60-79: Mild distraction (monitor only)
    THRESHOLD_DISTRACTED = 40       # 40-59: Distraction detected
    THRESHOLD_HIGH_DISTRACTION = 0  # 0-39: High distraction
    
    # ===== WARNING SYSTEM =====
    WARNING_COOLDOWN = 60           # Seconds between warnings (avoid spam)
    SUSTAINED_DISTRACTION_DURATION = 60   # Seconds of continuous distraction before warning
    HIGH_DISTRACTION_DURATION = 180       # Seconds for high distraction warning (3 min)
    WARNING_DECAY_TIME = 300        # Focused time to remove 1 warning (5 min)
    
    # ===== CAMERA EFFICIENCY =====
    CAMERA_CHECK_INTERVAL = 3       # Check camera every N seconds (not every frame)
    CAMERA_RESOLUTION = (640, 480)  # 480p for efficiency
    CAMERA_FPS = 15                 # Lower FPS to reduce CPU
    
    # ===== APP MONITORING =====
    APP_CHECK_INTERVAL = 2          # Check active app every N seconds
    APP_HISTORY_SIZE = 30           # Keep last 30 app samples (60 seconds)
    
    # ===== INPUT PATTERN ANALYSIS =====
    INPUT_HISTORY_WINDOW = 30       # Analyze last 30 seconds of input
    KEYPRESS_HISTORY_SIZE = 100
    MOUSE_CLICK_HISTORY_SIZE = 50
    MOUSE_MOVE_HISTORY_SIZE = 50
    SCROLL_HISTORY_SIZE = 30
    
    # Typing patterns
    STUDY_TYPING_MIN_WPM = 15       # Minimum typing for study
    STUDY_TYPING_MAX_WPM = 60       # Maximum typing for study
    GAMING_TYPING_WPM = 100         # Rapid typing = likely gaming
    
    # Click patterns
    NORMAL_CLICKS_PER_MIN = 10
    GAMING_CLICKS_PER_MIN = 30
    
    # Scroll patterns
    READING_SCROLL_SPEED = 5        # Slow scroll = reading
    REELS_SCROLL_SPEED = 20         # Fast scroll = entertainment
    
    # ===== STUDY APP WHITELIST =====
    STUDY_APPS = {
        # Browsers (requires content analysis for true detection)
        'chrome.exe', 'firefox.exe', 'msedge.exe', 'brave.exe', 'opera.exe',
        
        # Document editors
        'winword.exe', 'excel.exe', 'powerpnt.exe',  # MS Office
        'acrord32.exe', 'acrobat.exe',  # Adobe PDF
        'foxitreader.exe', 'sumatrapdf.exe',  # PDF readers
        
        # Note-taking
        'onenote.exe', 'notion.exe', 'evernote.exe',
        'obsidian.exe', 'joplin.exe',
        'notepad.exe', 'notepad++.exe',
        
        # Code editors
        'code.exe', 'pycharm64.exe', 'devenv.exe',
        'sublime_text.exe', 'atom.exe', 'webstorm64.exe',
        
        # Study tools
        'anki.exe', 'calibre.exe', 'zotero.exe',
        'mathematica.exe', 'matlab.exe',
    }
    
    # ===== DISTRACTION APP BLACKLIST =====
    DISTRACTION_APPS = {
        # Social media
        'discord.exe', 'telegram.exe', 'whatsapp.exe',
        'slack.exe', 'teams.exe',  # Work chat can be distraction
        
        # Gaming platforms
        'steam.exe', 'epicgameslauncher.exe',
        'riotclientservices.exe', 'battle.net.exe',
        'origin.exe', 'uplay.exe',
        
        # Games
        'leagueclient.exe', 'valorant.exe', 'minecraft.exe',
        'gta5.exe', 'fortnite.exe',
        
        # Entertainment
        'spotify.exe', 'vlc.exe', 'wmplayer.exe',
        'netflix.exe', 'primevideo.exe',
        
        # Streaming
        'obs64.exe', 'streamlabs obs.exe', 'xsplit.exe',
    }
    
    # ===== BROWSER CONTENT ANALYSIS =====
    # Keywords in URL/title that suggest study
    STUDY_URL_KEYWORDS = [
        'docs.google', 'github', 'stackoverflow',
        'coursera', 'udemy', 'khan', 'edx',
        'wikipedia', 'scholar.google', 'arxiv',
        'leetcode', 'hackerrank', 'w3schools',
        'mdn.', 'documentation', '/docs/',
    ]
    
    # Keywords that suggest distraction
    DISTRACTION_URL_KEYWORDS = [
        'youtube.com/shorts', 'youtube.com/watch',  # Unless educational
        'netflix', 'instagram', 'facebook', 'twitter',
        'tiktok', 'reddit.com/r/', 'twitch',
        '/gaming', '/games', 'reels', 'shorts',
    ]
    
    # ===== UI/UX SETTINGS =====
    SILENT_MODE = True              # Default to silent (no interruptions for good behavior)
    GENTLE_WARNINGS = True          # Use calm, supportive language
    MAX_WARNINGS_BEFORE_ESCALATION = 5
    
    # Warning messages (calm and supportive)
    MESSAGES = {
        'gentle_nudge': '💭 Taking a break? Ready to refocus?',
        'mild_warning': '📚 Time to get back to studying',
        'moderate_warning': '⚠️ Multiple distractions detected. Please refocus.',
        'strong_warning': '🚨 Consistent distraction. Consider taking a scheduled break.',
    }
    
    # ===== PARENT REPORTING =====
    REPORT_FOCUS_TRENDS = True
    REPORT_TIME_BREAKDOWN = True
    REPORT_IMPROVEMENT_SUGGESTIONS = True
    REPORT_SCREENSHOTS = False      # Privacy-first: NO screenshots
    REPORT_RAW_DATA = False         # Privacy-first: NO raw camera data
    
    @classmethod
    def get_config_dict(cls):
        """Return configuration as dictionary"""
        return {
            'weights': {
                'app_usage': cls.WEIGHT_APP_USAGE,
                'interaction': cls.WEIGHT_INTERACTION,
                'eye_gaze': cls.WEIGHT_EYE_GAZE,
                'head_pose': cls.WEIGHT_HEAD_POSE,
            },
            'thresholds': {
                'focused': cls.THRESHOLD_FOCUSED,
                'mild_drift': cls.THRESHOLD_MILD_DRIFT,
                'distracted': cls.THRESHOLD_DISTRACTED,
                'high_distraction': cls.THRESHOLD_HIGH_DISTRACTION,
            },
            'warnings': {
                'cooldown': cls.WARNING_COOLDOWN,
                'sustained_duration': cls.SUSTAINED_DISTRACTION_DURATION,
                'high_distraction_duration': cls.HIGH_DISTRACTION_DURATION,
                'decay_time': cls.WARNING_DECAY_TIME,
            },
            'camera': {
                'check_interval': cls.CAMERA_CHECK_INTERVAL,
                'resolution': cls.CAMERA_RESOLUTION,
                'fps': cls.CAMERA_FPS,
            }
        }