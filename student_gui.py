import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from database import Database
from face_detection import FaceDetector
from activity_monitor import ActivityMonitor
from focus_scorer import FocusScorer
from activity_logger import ActivityLogger
from focus_config import FocusConfig
from website_blocker import WebsiteBlocker
from notification_system import NotificationSystem
from break_reminder import BreakReminder
from analytics_engine import AnalyticsEngine
from gamification_system import GamificationSystem
from notes_todo_system import NotesAndTodoSystem
from voice_commands import VoiceCommandSystem
from music_player import StudyMusicPlayer
from youtube_music_player import YouTubeMusicPlayer
from theme_manager import ThemeManager
from report_generator import ReportGenerator
from study_groups import StudyGroupsSystem
from group_thumbnail_manager import GroupThumbnailManager
import time
import threading
import sqlite3
import math
import random
import datetime
from PIL import Image, ImageTk
import os
import shutil

class StudentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("✨ Study Tracker - Student Dashboard")
        self.root.geometry("900x700")

        # Default colors (before any UI creation)
        self.colors = {
            'primary': '#6366F1',
            'secondary': '#8B5CF6',
            'success': '#10B981',
            'warning': '#F59E0B',
            'danger': '#EF4444',
            'bg_light': '#F9FAFB',
            'bg_card': '#FFFFFF',
            'text_primary': '#111827',
            'text_secondary': '#6B7280',
            'border': '#E5E7EB',
            'success_light': '#D1FAE5',
            'primary_dark': '#4F46E5'
        }

        self.root.resizable(True, True)
        
        # Modern color scheme
        self.colors = {
            'primary': '#6366F1',      # Indigo
            'primary_dark': '#4F46E5',
            'secondary': '#8B5CF6',    # Purple
            'success': '#10B981',      # Green
            'success_light': '#D1FAE5',
            'warning': '#F59E0B',      # Amber
            'danger': '#EF4444',       # Red
            'bg_light': '#F9FAFB',     # Very light gray
            'bg_card': '#FFFFFF',
            'text_primary': '#111827',
            'text_secondary': '#6B7280',
            'border': '#E5E7EB'
        }

        self.db = Database()
        self.face_detector = FaceDetector()
        
        # Multi-signal fusion system
        self.activity_monitor = ActivityMonitor()
        self.focus_scorer = FocusScorer(self.activity_monitor, self.face_detector)
        self.activity_logger = ActivityLogger()
        
        # All advanced features
        self.website_blocker = WebsiteBlocker()
        self.notification_system = NotificationSystem()
        self.break_reminder = BreakReminder()
        self.analytics_engine = AnalyticsEngine()
        self.gamification = GamificationSystem()
        self.notes_todo = NotesAndTodoSystem()
        self.voice_commands = VoiceCommandSystem()
        self.music_player = StudyMusicPlayer()
        self.youtube_player = YouTubeMusicPlayer()
        self.theme_manager = ThemeManager()
        self.report_generator = ReportGenerator()
        self.study_groups = StudyGroupsSystem()
        self.thumbnail_manager = GroupThumbnailManager()
        
        self.current_user = None
        self.animation_id = None
        self.current_session_id = None
        self.session_running = False
        self.websites_blocked = False
        self.current_theme = 'light'
        self.profile_photo_image = None
        
        # Create profile photos directory if not exists
        if not os.path.exists('profile_photos'):
            os.makedirs('profile_photos')
        
        # Load theme
        self.colors = self.theme_manager.get_theme(self.current_theme)

        self.create_login_screen()

    def create_login_screen(self):
        self.clear_screen()

        # Gradient-inspired background
        main_frame = tk.Frame(self.root, bg=self.colors['bg_light'])
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Center container with card effect
        center_frame = tk.Frame(main_frame, bg=self.colors['bg_light'])
        center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Card container
        card_frame = tk.Frame(center_frame, bg=self.colors['bg_card'], highlightbackground=self.colors['border'], highlightthickness=2)
        card_frame.pack(padx=40, pady=40)

        # Header with icon
        header_frame = tk.Frame(card_frame, bg=self.colors['bg_card'])
        header_frame.pack(pady=(30, 10))
        
        tk.Label(header_frame, text="📚", font=("Arial", 48), bg=self.colors['bg_card']).pack()
        tk.Label(header_frame, text="Student Login", font=("Segoe UI", 24, "bold"), 
                bg=self.colors['bg_card'], fg=self.colors['text_primary']).pack(pady=(10, 5))
        tk.Label(header_frame, text="Welcome back! Continue your learning journey", 
                font=("Segoe UI", 10), bg=self.colors['bg_card'], fg=self.colors['text_secondary']).pack()

        # Form container
        form_frame = tk.Frame(card_frame, bg=self.colors['bg_card'])
        form_frame.pack(pady=30, padx=40)

        # Username field
        tk.Label(form_frame, text="Username", font=("Segoe UI", 11, "bold"), 
                bg=self.colors['bg_card'], fg=self.colors['text_primary']).grid(row=0, column=0, sticky="w", pady=(0, 5))
        self.username_entry = tk.Entry(form_frame, font=("Segoe UI", 12), width=30, 
                                      relief=tk.FLAT, highlightbackground=self.colors['border'], 
                                      highlightthickness=2, bd=8)
        self.username_entry.grid(row=1, column=0, pady=(0, 20))

        # Password field
        tk.Label(form_frame, text="Password", font=("Segoe UI", 11, "bold"), 
                bg=self.colors['bg_card'], fg=self.colors['text_primary']).grid(row=2, column=0, sticky="w", pady=(0, 5))
        self.password_entry = tk.Entry(form_frame, show="●", font=("Segoe UI", 12), width=30, 
                                      relief=tk.FLAT, highlightbackground=self.colors['border'], 
                                      highlightthickness=2, bd=8)
        self.password_entry.grid(row=3, column=0, pady=(0, 10))

        # Buttons
        button_frame = tk.Frame(card_frame, bg=self.colors['bg_card'])
        button_frame.pack(pady=(10, 30), padx=40, fill=tk.X)

        login_btn = tk.Button(button_frame, text="🔐 Login", command=self.login,
                            font=("Segoe UI", 12, "bold"), width=28, height=2,
                            bg=self.colors['primary'], fg="white", relief=tk.FLAT,
                            cursor="hand2", activebackground=self.colors['primary_dark'])
        login_btn.pack(pady=8, fill=tk.X)
        self.add_hover_effect(login_btn, self.colors['primary'], self.colors['primary_dark'])

        register_btn = tk.Button(button_frame, text="✨ Create New Account", command=self.create_register_screen,
                               font=("Segoe UI", 11, "bold"), width=28, height=2,
                               bg=self.colors['success'], fg="white", 
                               relief=tk.FLAT, cursor="hand2")
        register_btn.pack(pady=8, fill=tk.X)
        self.add_hover_effect(register_btn, self.colors['success'], '#059669')

    def create_register_screen(self):
        self.clear_screen()

        main_frame = tk.Frame(self.root, bg=self.colors['bg_light'])
        main_frame.pack(fill=tk.BOTH, expand=True)

        center_frame = tk.Frame(main_frame, bg=self.colors['bg_light'])
        center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        card_frame = tk.Frame(center_frame, bg=self.colors['bg_card'], 
                             highlightbackground=self.colors['border'], highlightthickness=2)
        card_frame.pack(padx=40, pady=40)

        # Header
        header_frame = tk.Frame(card_frame, bg=self.colors['bg_card'])
        header_frame.pack(pady=(30, 10))
        
        tk.Label(header_frame, text="🎓", font=("Arial", 48), bg=self.colors['bg_card']).pack()
        tk.Label(header_frame, text="Create Account", font=("Segoe UI", 24, "bold"), 
                bg=self.colors['bg_card'], fg=self.colors['text_primary']).pack(pady=(10, 5))
        tk.Label(header_frame, text="Join the learning community today", 
                font=("Segoe UI", 10), bg=self.colors['bg_card'], fg=self.colors['text_secondary']).pack()

        # Form
        form_frame = tk.Frame(card_frame, bg=self.colors['bg_card'])
        form_frame.pack(pady=30, padx=40)

        tk.Label(form_frame, text="Username", font=("Segoe UI", 11, "bold"), 
                bg=self.colors['bg_card'], fg=self.colors['text_primary']).grid(row=0, column=0, sticky="w", pady=(0, 5))
        self.reg_username_entry = tk.Entry(form_frame, font=("Segoe UI", 12), width=30, 
                                          relief=tk.FLAT, highlightbackground=self.colors['border'], 
                                          highlightthickness=2, bd=8)
        self.reg_username_entry.grid(row=1, column=0, pady=(0, 15))

        tk.Label(form_frame, text="Password", font=("Segoe UI", 11, "bold"), 
                bg=self.colors['bg_card'], fg=self.colors['text_primary']).grid(row=2, column=0, sticky="w", pady=(0, 5))
        self.reg_password_entry = tk.Entry(form_frame, show="●", font=("Segoe UI", 12), width=30, 
                                          relief=tk.FLAT, highlightbackground=self.colors['border'], 
                                          highlightthickness=2, bd=8)
        self.reg_password_entry.grid(row=3, column=0, pady=(0, 15))

        tk.Label(form_frame, text="Parent Username", font=("Segoe UI", 11, "bold"), 
                bg=self.colors['bg_card'], fg=self.colors['text_primary']).grid(row=4, column=0, sticky="w", pady=(0, 5))
        self.parent_username_entry = tk.Entry(form_frame, font=("Segoe UI", 12), width=30, 
                                             relief=tk.FLAT, highlightbackground=self.colors['border'], 
                                             highlightthickness=2, bd=8)
        self.parent_username_entry.grid(row=5, column=0, pady=(0, 10))

        # Buttons
        button_frame = tk.Frame(card_frame, bg=self.colors['bg_card'])
        button_frame.pack(pady=(10, 30), padx=40)

        register_btn = tk.Button(button_frame, text="Create Account", command=self.register,
                               font=("Segoe UI", 12, "bold"), width=28, height=2,
                               bg=self.colors['primary'], fg="white", relief=tk.FLAT,
                               cursor="hand2", activebackground=self.colors['primary_dark'])
        register_btn.pack(pady=5)
        self.add_hover_effect(register_btn, self.colors['primary'], self.colors['primary_dark'])

        back_btn = tk.Button(button_frame, text="← Back to Login", command=self.create_login_screen,
                           font=("Segoe UI", 11), width=28, height=2,
                           bg=self.colors['bg_light'], fg=self.colors['text_primary'], 
                           relief=tk.FLAT, cursor="hand2")
        back_btn.pack(pady=5)
        self.add_hover_effect(back_btn, self.colors['bg_light'], self.colors['border'])

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        try:
            if self.db.authenticate_user(username, password, 'student'):
                self.current_user = username
                self.db.update_streak_on_login(username)
                self.create_main_screen()
            else:
                messagebox.showerror("Error", "Invalid credentials")
        except Exception as e:
            messagebox.showerror("Error", f"Login failed: {str(e)}\nPlease restart the app.")
            print(f"Login error: {e}")
            import traceback
            traceback.print_exc()

    def register(self):
        username = self.reg_username_entry.get()
        password = self.reg_password_entry.get()
        parent_username = self.parent_username_entry.get()

        if self.db.register_user(username, password, 'student', parent_username):
            messagebox.showinfo("Success", "Registration successful")
            self.create_login_screen()
        else:
            messagebox.showerror("Error", "Username already exists")


    def create_main_screen(self):
        try:
            self.clear_screen()
            
            # Initialize sidebar state
            self.sidebar_visible = True
            self.current_view = "Dashboard"
            
            # Main container
            self.main_container = tk.Frame(self.root, bg=self.colors['bg_light'])
            self.main_container.pack(fill=tk.BOTH, expand=True)
            
            # Create sidebar
            self.create_sidebar()
            
            # Create content area
            self.content_frame = tk.Frame(self.main_container, bg=self.colors['bg_light'])
            self.content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            # Hamburger button (always visible, on top of content)
            self.hamburger_btn = tk.Button(self.root, text="☰", command=self.toggle_sidebar,
                                font=("Segoe UI", 18, "bold"), bg=self.colors['primary'],
                                fg="white", relief=tk.FLAT, cursor="hand2", width=3, height=1)
            self.hamburger_btn.place(x=10, y=10)
            
            # Load default view
            self.switch_view("Dashboard")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create dashboard: {str(e)}\nPlease restart the app.")
            print(f"Dashboard error: {e}")
            import traceback
            traceback.print_exc()
            self.create_login_screen()
    
    def create_sidebar(self):
        """Create collapsible sidebar navigation"""
        self.sidebar = tk.Frame(self.main_container, bg=self.colors['bg_card'], 
                               width=250, highlightbackground=self.colors['border'], 
                               highlightthickness=1)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)
        
        # User info section
        user_section = tk.Frame(self.sidebar, bg=self.colors['primary'])
        user_section.pack(fill=tk.X, pady=(50, 0))
        
        # Profile photo
        photo_frame = tk.Frame(user_section, bg=self.colors['primary'])
        photo_frame.pack(pady=(15, 5))
        
        self.profile_photo_label = tk.Label(photo_frame, bg=self.colors['primary'], cursor="hand2")
        self.profile_photo_label.pack()
        self.profile_photo_label.bind("<Button-1>", lambda e: self.upload_profile_photo())
        
        # Load and display profile photo
        self.load_profile_photo()
        
        tk.Label(user_section, text=self.current_user, font=("Segoe UI", 14, "bold"), 
                bg=self.colors['primary'], fg="white").pack(pady=(0, 5))
        
        # Get coins
        coins, _ = self.gamification.get_user_coins(self.current_user)
        tk.Label(user_section, text=f"🪙 {coins} Coins", font=("Segoe UI", 11), 
                bg=self.colors['primary'], fg="#FCD34D").pack(pady=(0, 10))
        
        # Change photo hint
        tk.Label(user_section, text="(Click photo to change)", font=("Segoe UI", 8), 
                bg=self.colors['primary'], fg="#E0E7FF").pack(pady=(0, 15))
        
        # Navigation items
        nav_frame = tk.Frame(self.sidebar, bg=self.colors['bg_card'])
        nav_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        nav_items = [
            ("📊 Dashboard", "Dashboard"),
            ("📚 Study Session", "Study"),
            ("📋 Activities", "Activities"),
            ("📊 Analytics", "Analytics"),
            ("🎮 Rewards", "Rewards"),
            ("📝 Notes & Tasks", "Notes"),
            ("👥 Study Groups", "Groups"),
            ("👤 Profile", "Profile"),
        ]
        
        self.nav_buttons = {}
        for text, view_name in nav_items:
            btn = tk.Button(nav_frame, text=text, 
                           command=lambda v=view_name: self.switch_view(v),
                           font=("Segoe UI", 11), bg=self.colors['bg_card'], 
                           fg=self.colors['text_primary'], relief=tk.FLAT, 
                           anchor='w', padx=20, height=2, cursor="hand2")
            btn.pack(fill=tk.X, pady=2, padx=5)
            self.nav_buttons[view_name] = btn
            self.add_hover_effect(btn, self.colors['bg_card'], self.colors['bg_light'])
        
        # Separator
        tk.Frame(nav_frame, height=2, bg=self.colors['border']).pack(fill=tk.X, pady=10, padx=10)
        
        # Night mode toggle button
        night_mode_icon = "🌙" if self.current_theme == 'light' else "☀️"
        night_mode_text = "Night Mode" if self.current_theme == 'light' else "Day Mode"
        self.night_mode_btn = tk.Button(nav_frame, text=f"{night_mode_icon} {night_mode_text}", 
                                        command=self.toggle_night_mode,
                                        font=("Segoe UI", 11, "bold"), bg=self.colors['secondary'], 
                                        fg="white", relief=tk.FLAT, height=2, cursor="hand2")
        self.night_mode_btn.pack(fill=tk.X, pady=5, padx=10, side=tk.BOTTOM)
        self.add_hover_effect(self.night_mode_btn, self.colors['secondary'], '#7C3AED')
        
        # Logout button
        logout_btn = tk.Button(nav_frame, text="🚪 Logout", command=self.logout,
                              font=("Segoe UI", 11, "bold"), bg=self.colors['danger'], 
                              fg="white", relief=tk.FLAT, height=2, cursor="hand2")
        logout_btn.pack(fill=tk.X, pady=5, padx=10, side=tk.BOTTOM)
        self.add_hover_effect(logout_btn, self.colors['danger'], '#DC2626')
    
    def toggle_sidebar(self):
        """Toggle sidebar visibility"""
        if self.sidebar_visible:
            self.sidebar.pack_forget()
            self.sidebar_visible = False
        else:
            self.sidebar.pack(side=tk.LEFT, fill=tk.Y, before=self.content_frame)
            self.sidebar_visible = True
    
    def switch_view(self, view_name):
        """Switch between different views"""
        self.current_view = view_name
        
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Highlight active button
        for name, btn in self.nav_buttons.items():
            if name == view_name:
                btn.configure(bg=self.colors['primary'], fg="white")
            else:
                btn.configure(bg=self.colors['bg_card'], fg=self.colors['text_primary'])
        
        # Create a wrapper class that mimics notebook behavior but creates frames directly
        class NotebookWrapper:
            def __init__(self, parent):
                self.parent = parent
                self.current_frame = None
            
            def add(self, frame, text=""):
                # Just store the frame, it's already created with correct parent
                self.current_frame = frame
        
        # Set notebook to our wrapper - this allows tab methods to work without modification
        self.notebook = NotebookWrapper(self.content_frame)
        
        # Load appropriate content - methods will create frames with self.notebook as parent
        # which is actually content_frame through our wrapper
        if view_name == "Dashboard":
            self.create_monitor_content()
        elif view_name == "Study":
            self.create_study_content()
        elif view_name == "Activities":
            self.create_activities_content()
        elif view_name == "Analytics":
            self.create_analytics_content()
        elif view_name == "Rewards":
            self.create_rewards_content()
        elif view_name == "Notes":
            self.create_notes_content()
        elif view_name == "Groups":
            self.create_groups_content()
        elif view_name == "Profile":
            self.create_profile_content()
    
    def create_monitor_content(self):
        """Create monitor/dashboard content directly"""
        monitor_frame = tk.Frame(self.content_frame, bg=self.colors['bg_light'])
        monitor_frame.pack(fill=tk.BOTH, expand=True)
        self.notebook.add(monitor_frame, text="📊 Dashboard")
        
        # Copy the content creation from create_monitor_tab
        self._build_monitor_ui(monitor_frame)
    
    def create_study_content(self):
        """Create study session content directly"""
        study_frame = tk.Frame(self.content_frame, bg=self.colors['bg_light'])
        study_frame.pack(fill=tk.BOTH, expand=True)
        self.notebook.add(study_frame, text="📚 Study")
        
        self._build_study_ui(study_frame)
    
    def create_activities_content(self):
        """Create activities content directly"""
        activities_frame = tk.Frame(self.content_frame, bg=self.colors['bg_light'])
        activities_frame.pack(fill=tk.BOTH, expand=True)
        self.notebook.add(activities_frame, text="📋 Activities")
        
        self._build_activities_ui(activities_frame)
    
    def create_analytics_content(self):
        """Create analytics content directly"""
        analytics_frame = tk.Frame(self.content_frame, bg=self.colors['bg_light'])
        analytics_frame.pack(fill=tk.BOTH, expand=True)
        self.notebook.add(analytics_frame, text="📊 Analytics")
        
        self._build_analytics_ui(analytics_frame)
    
    def create_rewards_content(self):
        """Create rewards content directly"""
        rewards_frame = tk.Frame(self.content_frame, bg=self.colors['bg_light'])
        rewards_frame.pack(fill=tk.BOTH, expand=True)
        self.notebook.add(rewards_frame, text="🎮 Rewards")
        
        self._build_rewards_ui(rewards_frame)
    
    def create_notes_content(self):
        """Create notes content directly"""
        notes_frame = tk.Frame(self.content_frame, bg=self.colors['bg_light'])
        notes_frame.pack(fill=tk.BOTH, expand=True)
        self.notebook.add(notes_frame, text="📝 Notes")
        
        self._build_notes_ui(notes_frame)
    
    def create_groups_content(self):
        """Create groups content directly"""
        groups_frame = tk.Frame(self.content_frame, bg=self.colors['bg_light'])
        groups_frame.pack(fill=tk.BOTH, expand=True)
        self.notebook.add(groups_frame, text="👥 Groups")
        
        self._build_groups_ui(groups_frame)
    
    def create_profile_content(self):
        """Create profile content directly"""
        profile_frame = tk.Frame(self.content_frame, bg=self.colors['bg_light'])
        profile_frame.pack(fill=tk.BOTH, expand=True)
        self.notebook.add(profile_frame, text="👤 Profile")
        
        self._build_profile_ui(profile_frame)

    def create_monitor_tab(self):
        monitor_frame = tk.Frame(self.notebook, bg=self.colors['bg_light'])
        self.notebook.add(monitor_frame, text="📊 Dashboard")
        self._build_monitor_ui(monitor_frame)
    
    def _build_monitor_ui(self, monitor_frame):
        # Scrollable frame
        canvas = tk.Canvas(monitor_frame, bg=self.colors['bg_light'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(monitor_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg_light'])

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Header with welcome and streak
        header_frame = tk.Frame(scrollable_frame, bg=self.colors['bg_card'], 
                               highlightbackground=self.colors['border'], highlightthickness=1)
        header_frame.pack(fill=tk.X, pady=20, padx=20)

        welcome_container = tk.Frame(header_frame, bg=self.colors['bg_card'])
        welcome_container.pack(fill=tk.X, padx=20, pady=20)

        tk.Label(welcome_container, text=f"Welcome back, {self.current_user}! 👋", 
                font=("Segoe UI", 22, "bold"), bg=self.colors['bg_card'], 
                fg=self.colors['text_primary']).pack(side=tk.LEFT)
        
        streak_frame = tk.Frame(welcome_container, bg=self.colors['warning'], 
                               highlightbackground=self.colors['warning'], highlightthickness=2)
        streak_frame.pack(side=tk.RIGHT, padx=10)
        self.streak_label = tk.Label(streak_frame, text=f"🔥 {self.get_study_streak()} Day Streak", 
                                     font=("Segoe UI", 13, "bold"), bg=self.colors['warning'], 
                                     fg="white", padx=15, pady=8)
        self.streak_label.pack()

        # Motivational Quote Card
        quote_frame = tk.Frame(scrollable_frame, bg=self.colors['success_light'], 
                              highlightbackground=self.colors['success'], highlightthickness=2)
        quote_frame.pack(fill=tk.X, pady=(0, 20), padx=20)
        
        tk.Label(quote_frame, text="💡", font=("Arial", 24), bg=self.colors['success_light']).pack(pady=(15, 5))
        self.quote_label = tk.Label(quote_frame, text=self.get_random_quote(), 
                                    font=("Segoe UI", 12, "italic"), bg=self.colors['success_light'], 
                                    fg=self.colors['text_primary'], wraplength=700)
        self.quote_label.pack(pady=(0, 15), padx=20)

        # Stats Cards Row
        stats_container = tk.Frame(scrollable_frame, bg=self.colors['bg_light'])
        stats_container.pack(fill=tk.X, pady=(0, 20), padx=20)

        # Progress Card
        progress_card = tk.Frame(stats_container, bg=self.colors['bg_card'], 
                                highlightbackground=self.colors['border'], highlightthickness=1)
        progress_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        tk.Label(progress_card, text="Today's Progress", font=("Segoe UI", 14, "bold"), 
                bg=self.colors['bg_card'], fg=self.colors['text_primary']).pack(pady=(20, 10))
        
        self.progress_canvas = tk.Canvas(progress_card, width=180, height=180, 
                                        bg=self.colors['bg_card'], highlightthickness=0)
        self.progress_canvas.pack(pady=10)
        self.progress_canvas.bind("<Button-1>", lambda e: self.show_daily_tasks())
        
        tk.Label(progress_card, text="Click for tasks", font=("Segoe UI", 9), 
                bg=self.colors['bg_card'], fg=self.colors['text_secondary']).pack(pady=(0, 20))

        self.draw_progress_circle()

        # Weekly Chart Card
        weekly_card = tk.Frame(scrollable_frame, bg=self.colors['bg_card'], 
                              highlightbackground=self.colors['border'], highlightthickness=1)
        weekly_card.pack(fill=tk.X, pady=(0, 20), padx=20)

        tk.Label(weekly_card, text="📈 This Week's Progress", font=("Segoe UI", 16, "bold"), 
                bg=self.colors['bg_card'], fg=self.colors['text_primary']).pack(pady=(20, 15), padx=20, anchor="w")
        
        self.weekly_canvas = tk.Canvas(weekly_card, height=150, bg=self.colors['bg_card'], highlightthickness=0)
        self.weekly_canvas.pack(fill=tk.X, padx=30, pady=(0, 20))
        self.draw_weekly_chart()

        # Quick Actions Card
        actions_card = tk.Frame(scrollable_frame, bg=self.colors['bg_card'], 
                               highlightbackground=self.colors['border'], highlightthickness=1)
        actions_card.pack(fill=tk.X, pady=(0, 20), padx=20)

        tk.Label(actions_card, text="⚡ Quick Actions", font=("Segoe UI", 16, "bold"), 
                bg=self.colors['bg_card'], fg=self.colors['text_primary']).pack(pady=(20, 15), padx=20, anchor="w")

        quick_buttons_frame = tk.Frame(actions_card, bg=self.colors['bg_card'])
        quick_buttons_frame.pack(pady=(0, 20), padx=20)

        goals_btn = tk.Button(quick_buttons_frame, text="🎯 Set Goals", command=self.set_goals,
                             font=("Segoe UI", 11, "bold"), width=20, height=2,
                             bg=self.colors['secondary'], fg="white", relief=tk.FLAT, cursor="hand2")
        goals_btn.grid(row=0, column=0, padx=10, pady=5)
        self.add_hover_effect(goals_btn, self.colors['secondary'], '#7C3AED')

        progress_btn = tk.Button(quick_buttons_frame, text="📊 View Progress", command=self.view_progress,
                                font=("Segoe UI", 11, "bold"), width=20, height=2,
                                bg=self.colors['primary'], fg="white", relief=tk.FLAT, cursor="hand2")
        progress_btn.grid(row=0, column=1, padx=10, pady=5)
        self.add_hover_effect(progress_btn, self.colors['primary'], self.colors['primary_dark'])

    def create_study_tab(self):
        study_frame = tk.Frame(self.notebook, bg=self.colors['bg_light'])
        self.notebook.add(study_frame, text="📚 Study Session")
        self._build_study_ui(study_frame)
    
    def _build_study_ui(self, study_frame):
        # Center container
        center_frame = tk.Frame(study_frame, bg=self.colors['bg_light'])
        center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Header Card
        header_card = tk.Frame(center_frame, bg=self.colors['bg_card'], 
                              highlightbackground=self.colors['border'], highlightthickness=1)
        header_card.pack(pady=(0, 20))

        tk.Label(header_card, text="🚀", font=("Arial", 48), bg=self.colors['bg_card']).pack(pady=(30, 10))
        tk.Label(header_card, text="Ready to Learn?", font=("Segoe UI", 24, "bold"), 
                bg=self.colors['bg_card'], fg=self.colors['text_primary']).pack(pady=(0, 10), padx=40)
        tk.Label(header_card, text="Choose a study session or start a custom one", 
                font=("Segoe UI", 11), bg=self.colors['bg_card'], 
                fg=self.colors['text_secondary']).pack(pady=(0, 30), padx=40)

        # Quick Session Buttons Card
        sessions_card = tk.Frame(center_frame, bg=self.colors['bg_card'], 
                                highlightbackground=self.colors['border'], highlightthickness=1)
        sessions_card.pack(pady=(0, 20))

        tk.Label(sessions_card, text="⚡ Quick Sessions", font=("Segoe UI", 16, "bold"), 
                bg=self.colors['bg_card'], fg=self.colors['text_primary']).pack(pady=(20, 15), padx=40)

        quick_buttons_frame = tk.Frame(sessions_card, bg=self.colors['bg_card'])
        quick_buttons_frame.pack(pady=(0, 20), padx=40)

        focus_btn = tk.Button(quick_buttons_frame, text="⏱️ 25min Focus", 
                             command=lambda: self.quick_session(0.5),
                             font=("Segoe UI", 12, "bold"), width=18, height=3,
                             bg=self.colors['success'], fg="white", relief=tk.FLAT, cursor="hand2")
        focus_btn.grid(row=0, column=0, padx=10, pady=10)
        self.add_hover_effect(focus_btn, self.colors['success'], '#059669')

        deep_btn = tk.Button(quick_buttons_frame, text="📖 1hr Deep Study", 
                            command=lambda: self.quick_session(1),
                            font=("Segoe UI", 12, "bold"), width=18, height=3,
                            bg=self.colors['primary'], fg="white", relief=tk.FLAT, cursor="hand2")
        deep_btn.grid(row=0, column=1, padx=10, pady=10)
        self.add_hover_effect(deep_btn, self.colors['primary'], self.colors['primary_dark'])

        challenge_btn = tk.Button(quick_buttons_frame, text="🏆 Study Challenge", 
                                 command=self.start_study_challenge,
                                 font=("Segoe UI", 12, "bold"), width=38, height=3,
                                 bg=self.colors['secondary'], fg="white", relief=tk.FLAT, cursor="hand2")
        challenge_btn.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        self.add_hover_effect(challenge_btn, self.colors['secondary'], '#7C3AED')

        # Custom Session Card
        custom_card = tk.Frame(center_frame, bg=self.colors['bg_card'], 
                              highlightbackground=self.colors['border'], highlightthickness=1)
        custom_card.pack()

        tk.Label(custom_card, text="⚙️ Custom Session", font=("Segoe UI", 16, "bold"), 
                bg=self.colors['bg_card'], fg=self.colors['text_primary']).pack(pady=(20, 15), padx=40)

        tk.Label(custom_card, text="Set your own duration and monitoring preferences", 
                font=("Segoe UI", 10), bg=self.colors['bg_card'], 
                fg=self.colors['text_secondary']).pack(padx=40)

        custom_btn = tk.Button(custom_card, text="🎯 Configure & Start", 
                              command=self.start_study_session,
                              font=("Segoe UI", 12, "bold"), width=30, height=3,
                              bg=self.colors['warning'], fg="white", relief=tk.FLAT, cursor="hand2")
        custom_btn.pack(pady=20, padx=40)
        self.add_hover_effect(custom_btn, self.colors['warning'], '#D97706')

    def create_activities_tab(self):
        activities_frame = tk.Frame(self.notebook, bg=self.colors['bg_light'])
        self.notebook.add(activities_frame, text="📋 Activities")
        self._build_activities_ui(activities_frame)
    
    def _build_activities_ui(self, activities_frame):
        # Scrollable frame
        canvas = tk.Canvas(activities_frame, bg=self.colors['bg_light'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(activities_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg_light'])

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Header
        header_card = tk.Frame(scrollable_frame, bg=self.colors['bg_card'], 
                              highlightbackground=self.colors['border'], highlightthickness=1)
        header_card.pack(fill=tk.X, pady=20, padx=20)

        tk.Label(header_card, text="📋 Session Activities", font=("Segoe UI", 20, "bold"), 
                bg=self.colors['bg_card'], fg=self.colors['text_primary']).pack(pady=20)

        # Get recent sessions
        conn = sqlite3.connect(self.db.db_name)
        c = conn.cursor()
        c.execute('''SELECT id, date, hours, warnings, focus_score 
                     FROM study_sessions 
                     WHERE username=? 
                     ORDER BY id DESC LIMIT 10''', (self.current_user,))
        sessions = c.fetchall()
        conn.close()

        if not sessions:
            tk.Label(scrollable_frame, text="No sessions yet. Start studying to see activities!", 
                    font=("Segoe UI", 14), bg=self.colors['bg_light'], 
                    fg=self.colors['text_secondary']).pack(pady=50)
            return

        # Session cards
        for session_id, date, hours, warnings, focus_score in sessions:
            session_card = tk.Frame(scrollable_frame, bg=self.colors['bg_card'], 
                                   highlightbackground=self.colors['border'], highlightthickness=1)
            session_card.pack(fill=tk.X, pady=10, padx=20)

            # Session header
            header = tk.Frame(session_card, bg=self.colors['primary'])
            header.pack(fill=tk.X)
            
            tk.Label(header, text=f"Session #{session_id} - {date}", 
                    font=("Segoe UI", 14, "bold"), bg=self.colors['primary'], 
                    fg="white").pack(side=tk.LEFT, padx=15, pady=10)
            
            tk.Label(header, text=f"{hours}h | Focus: {focus_score}%", 
                    font=("Segoe UI", 11), bg=self.colors['primary'], 
                    fg="white").pack(side=tk.RIGHT, padx=15)

            # Activity log
            activities = self.activity_logger.get_session_activity_log(self.current_user, session_id)
            
            if activities:
                log_frame = tk.Frame(session_card, bg=self.colors['bg_card'])
                log_frame.pack(fill=tk.X, padx=15, pady=10)
                
                tk.Label(log_frame, text="Activities:", font=("Segoe UI", 11, "bold"), 
                        bg=self.colors['bg_card']).pack(anchor='w', pady=5)
                
                # Show first 5 activities
                for i, activity in enumerate(activities[:5]):
                    timestamp, activity_type, app_name, window_title, url = activity
                    
                    activity_row = tk.Frame(log_frame, bg=self.colors['bg_light'])
                    activity_row.pack(fill=tk.X, pady=2)
                    
                    time_str = timestamp.split()[1][:5]  # HH:MM
                    tk.Label(activity_row, text=f"[{time_str}]", font=("Consolas", 9), 
                            bg=self.colors['bg_light'], fg=self.colors['text_secondary']).pack(side=tk.LEFT, padx=5)
                    
                    tk.Label(activity_row, text=f"{app_name}", font=("Segoe UI", 9, "bold"), 
                            bg=self.colors['bg_light']).pack(side=tk.LEFT, padx=5)
                    
                    if window_title and len(window_title) > 50:
                        window_title = window_title[:50] + "..."
                    tk.Label(activity_row, text=window_title or "", font=("Segoe UI", 9), 
                            bg=self.colors['bg_light'], fg=self.colors['text_secondary']).pack(side=tk.LEFT, padx=5)
                
                if len(activities) > 5:
                    tk.Label(log_frame, text=f"... and {len(activities)-5} more activities", 
                            font=("Segoe UI", 9, "italic"), bg=self.colors['bg_card'], 
                            fg=self.colors['text_secondary']).pack(anchor='w', pady=5)
            
            # Screenshots
            screenshots = self.activity_logger.get_session_screenshots(self.current_user, session_id)
            
            if screenshots:
                ss_frame = tk.Frame(session_card, bg=self.colors['bg_card'])
                ss_frame.pack(fill=tk.X, padx=15, pady=10)
                
                tk.Label(ss_frame, text=f"📸 {len(screenshots)} Screenshots Captured", 
                        font=("Segoe UI", 10, "bold"), bg=self.colors['bg_card'], 
                        fg=self.colors['success']).pack(anchor='w')
            
            # View details button
            btn_frame = tk.Frame(session_card, bg=self.colors['bg_card'])
            btn_frame.pack(pady=10)
            
            view_btn = tk.Button(btn_frame, text="View Full Report", 
                               command=lambda sid=session_id: self.show_session_details(sid),
                               font=("Segoe UI", 10, "bold"), width=20, height=1,
                               bg=self.colors['primary'], fg="white", relief=tk.FLAT, cursor="hand2")
            view_btn.pack()
            self.add_hover_effect(view_btn, self.colors['primary'], self.colors['primary_dark'])

    def show_session_details(self, session_id):
        details_window = tk.Toplevel(self.root)
        details_window.title(f"Session #{session_id} Details")
        details_window.geometry("900x600")
        details_window.configure(bg=self.colors['bg_light'])
        
        main_frame = tk.Frame(details_window, bg=self.colors['bg_card'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(main_frame, text=f"📊 Session #{session_id} - Complete Report", 
                font=("Segoe UI", 18, "bold"), bg=self.colors['bg_card']).pack(pady=15)
        
        # Activity log
        activities = self.activity_logger.get_session_activity_log(self.current_user, session_id)
        
        log_frame = tk.Frame(main_frame, bg=self.colors['bg_card'])
        log_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        tk.Label(log_frame, text="Complete Activity Log:", font=("Segoe UI", 12, "bold"), 
                bg=self.colors['bg_card']).pack(anchor='w', pady=5)
        
        log_text = tk.Text(log_frame, height=20, width=100, font=("Consolas", 9), wrap=tk.WORD)
        log_scroll = ttk.Scrollbar(log_frame, command=log_text.yview)
        log_text.config(yscrollcommand=log_scroll.set)
        
        log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        log_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        for activity in activities:
            timestamp, activity_type, app_name, window_title, url = activity
            log_text.insert(tk.END, f"[{timestamp}] {activity_type}\n", "header")
            log_text.insert(tk.END, f"  App: {app_name}\n")
            if window_title:
                log_text.insert(tk.END, f"  Window: {window_title}\n")
            if url:
                log_text.insert(tk.END, f"  URL: {url}\n")
            log_text.insert(tk.END, "\n")
        
        log_text.tag_config("header", foreground=self.colors['primary'], font=("Consolas", 9, "bold"))
        log_text.config(state=tk.DISABLED)
        
        # Close button
        tk.Button(main_frame, text="Close", command=details_window.destroy,
                 font=("Segoe UI", 12, "bold"), width=20, height=2,
                 bg=self.colors['danger'], fg="white", relief=tk.FLAT).pack(pady=15)


    def create_analytics_tab(self):
        analytics_frame = tk.Frame(self.notebook, bg=self.colors['bg_light'])
        self.notebook.add(analytics_frame, text="📊 Analytics")
        self._build_analytics_ui(analytics_frame)
    
    def _build_analytics_ui(self, analytics_frame):
        canvas = tk.Canvas(analytics_frame, bg=self.colors['bg_light'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(analytics_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg_light'])

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Header
        header_card = tk.Frame(scrollable_frame, bg=self.colors['bg_card'], 
                              highlightbackground=self.colors['border'], highlightthickness=1)
        header_card.pack(fill=tk.X, pady=20, padx=20)
        tk.Label(header_card, text="📊 Advanced Analytics", font=("Segoe UI", 20, "bold"), 
                bg=self.colors['bg_card']).pack(pady=20)

        # Study Patterns
        patterns = self.analytics_engine.get_study_patterns(self.current_user)
        
        patterns_card = tk.Frame(scrollable_frame, bg=self.colors['bg_card'], 
                                highlightbackground=self.colors['border'], highlightthickness=1)
        patterns_card.pack(fill=tk.X, pady=10, padx=20)
        
        tk.Label(patterns_card, text="⏰ Your Study Patterns", font=("Segoe UI", 16, "bold"), 
                bg=self.colors['bg_card']).pack(pady=15, padx=20, anchor='w')
        
        info_frame = tk.Frame(patterns_card, bg=self.colors['bg_card'])
        info_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(info_frame, text=f"🌟 Best Time: {patterns['best_time']} (Focus: {patterns['best_focus']}%)", 
                font=("Segoe UI", 12), bg=self.colors['bg_card'], fg=self.colors['success']).pack(anchor='w', pady=5)
        tk.Label(info_frame, text=f"⚠️ Worst Time: {patterns['worst_time']} (Focus: {patterns['worst_focus']}%)", 
                font=("Segoe UI", 12), bg=self.colors['bg_card'], fg=self.colors['danger']).pack(anchor='w', pady=5)

        # AI Recommendations
        recommendations = self.analytics_engine.predict_best_study_time(self.current_user)
        
        ai_card = tk.Frame(scrollable_frame, bg=self.colors['secondary'], 
                          highlightbackground=self.colors['secondary'], highlightthickness=2)
        ai_card.pack(fill=tk.X, pady=10, padx=20)
        
        tk.Label(ai_card, text="🤖 AI Recommendations", font=("Segoe UI", 14, "bold"), 
                bg=self.colors['secondary'], fg="white").pack(pady=10, padx=20, anchor='w')
        
        for rec in recommendations:
            tk.Label(ai_card, text=f"• {rec}", font=("Segoe UI", 11), 
                    bg=self.colors['secondary'], fg="white").pack(anchor='w', padx=30, pady=3)
        
        tk.Label(ai_card, text="", bg=self.colors['secondary']).pack(pady=5)

        # Weekly Report
        report = self.analytics_engine.generate_weekly_report(self.current_user)
        
        report_card = tk.Frame(scrollable_frame, bg=self.colors['bg_card'], 
                              highlightbackground=self.colors['border'], highlightthickness=1)
        report_card.pack(fill=tk.X, pady=10, padx=20)
        
        tk.Label(report_card, text="📈 This Week's Report", font=("Segoe UI", 16, "bold"), 
                bg=self.colors['bg_card']).pack(pady=15, padx=20, anchor='w')
        
        stats_grid = tk.Frame(report_card, bg=self.colors['bg_card'])
        stats_grid.pack(fill=tk.X, padx=20, pady=10)
        
        stats = [
            ("Sessions", report['sessions'], self.colors['primary']),
            ("Total Hours", f"{report['total_hours']}h", self.colors['success']),
            ("Avg Focus", f"{report['avg_focus']}%", self.colors['warning']),
            ("Grade", report['grade'], self.colors['danger'])
        ]
        
        for i, (label, value, color) in enumerate(stats):
            stat_box = tk.Frame(stats_grid, bg=color)
            stat_box.grid(row=i//2, column=i%2, padx=10, pady=10, sticky="ew")
            stats_grid.columnconfigure(i%2, weight=1)
            
            tk.Label(stat_box, text=str(value), font=("Segoe UI", 24, "bold"), 
                    bg=color, fg="white").pack(pady=10)
            tk.Label(stat_box, text=label, font=("Segoe UI", 11), 
                    bg=color, fg="white").pack(pady=(0, 10))

    def create_rewards_tab(self):
        rewards_frame = tk.Frame(self.notebook, bg=self.colors['bg_light'])
        self.notebook.add(rewards_frame, text="🎮 Rewards & Shop")
        self._build_rewards_ui(rewards_frame)
    
    def _build_rewards_ui(self, rewards_frame):
        canvas = tk.Canvas(rewards_frame, bg=self.colors['bg_light'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(rewards_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg_light'])

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Header with coins
        header_card = tk.Frame(scrollable_frame, bg=self.colors['warning'])
        header_card.pack(fill=tk.X, pady=20, padx=20)
        
        coins, total_earned = self.gamification.get_user_coins(self.current_user)
        
        tk.Label(header_card, text="🎮 Rewards & Shop", font=("Segoe UI", 20, "bold"), 
                bg=self.colors['warning'], fg="white").pack(pady=15)
        tk.Label(header_card, text=f"🪙 {coins} Coins | Total Earned: {total_earned}", 
                font=("Segoe UI", 14, "bold"), bg=self.colors['warning'], fg="white").pack(pady=(0, 15))

        # Themes Section
        themes_card = tk.Frame(scrollable_frame, bg=self.colors['bg_card'], 
                              highlightbackground=self.colors['border'], highlightthickness=1)
        themes_card.pack(fill=tk.X, pady=10, padx=20)
        
        tk.Label(themes_card, text="🎨 Themes", font=("Segoe UI", 16, "bold"), 
                bg=self.colors['bg_card']).pack(pady=15, padx=20, anchor='w')
        
        themes = self.theme_manager.get_available_themes()
        theme_var = tk.StringVar(value=self.current_theme)
        
        theme_grid = tk.Frame(themes_card, bg=self.colors['bg_card'])
        theme_grid.pack(fill=tk.X, padx=20, pady=10)
        
        for i, theme in enumerate(themes):
            theme_box = tk.Frame(theme_grid, bg=self.colors['bg_light'])
            theme_box.grid(row=i//2, column=i%2, padx=10, pady=5, sticky="ew")
            theme_grid.columnconfigure(i%2, weight=1)
            
            tk.Radiobutton(theme_box, text=theme.capitalize(), variable=theme_var, 
                          value=theme, command=lambda t=theme: self.change_theme(t),
                          font=("Segoe UI", 11), bg=self.colors['bg_light']).pack(side=tk.LEFT, padx=10, pady=8)
            
            if theme in ['light', 'dark']:
                tk.Label(theme_box, text="FREE", font=("Segoe UI", 9, "bold"), 
                        bg=self.colors['bg_light'], fg=self.colors['success']).pack(side=tk.RIGHT, padx=10)
            else:
                tk.Label(theme_box, text=f"🪙 750", font=("Segoe UI", 9, "bold"), 
                        bg=self.colors['bg_light'], fg=self.colors['warning']).pack(side=tk.RIGHT, padx=10)

        # Music Player Section
        music_card = tk.Frame(scrollable_frame, bg=self.colors['bg_card'], 
                             highlightbackground=self.colors['border'], highlightthickness=1)
        music_card.pack(fill=tk.X, pady=10, padx=20)
        
        tk.Label(music_card, text="🎵 Study Music Player", font=("Segoe UI", 16, "bold"), 
                bg=self.colors['bg_card']).pack(pady=15, padx=20, anchor='w')
        
        music_btn_frame = tk.Frame(music_card, bg=self.colors['bg_card'])
        music_btn_frame.pack(pady=10, padx=20)
        
        tk.Button(music_btn_frame, text="🎵 YouTube Music", command=self.open_youtube_music,
                 font=("Segoe UI", 11, "bold"), width=20, bg=self.colors['success'], 
                 fg="white", relief=tk.FLAT, cursor="hand2").grid(row=0, column=0, padx=5, pady=5)
        
        tk.Button(music_btn_frame, text="🎧 Spotify Music", command=lambda: self.play_music('spotify'),
                 font=("Segoe UI", 11, "bold"), width=20, bg=self.colors['primary'], 
                 fg="white", relief=tk.FLAT, cursor="hand2").grid(row=0, column=1, padx=5, pady=5)

        # Daily Challenges
        challenges = self.gamification.generate_daily_challenges(self.current_user)
        
        challenges_card = tk.Frame(scrollable_frame, bg=self.colors['bg_card'], 
                                   highlightbackground=self.colors['border'], highlightthickness=1)
        challenges_card.pack(fill=tk.X, pady=10, padx=20)
        
        tk.Label(challenges_card, text="🎯 Today's Challenges", font=("Segoe UI", 16, "bold"), 
                bg=self.colors['bg_card']).pack(pady=15, padx=20, anchor='w')
        
        for challenge in challenges:
            challenge_box = tk.Frame(challenges_card, bg=self.colors['success_light'], 
                                    highlightbackground=self.colors['success'], highlightthickness=2)
            challenge_box.pack(fill=tk.X, padx=20, pady=5)
            
            tk.Label(challenge_box, text=challenge['desc'], font=("Segoe UI", 12, "bold"), 
                    bg=self.colors['success_light']).pack(side=tk.LEFT, padx=15, pady=10)
            tk.Label(challenge_box, text=f"🪙 {challenge['reward']}", font=("Segoe UI", 11, "bold"), 
                    bg=self.colors['success_light'], fg=self.colors['success']).pack(side=tk.RIGHT, padx=15)

        # Leaderboard
        leaderboard = self.gamification.get_leaderboard()
        
        leaderboard_card = tk.Frame(scrollable_frame, bg=self.colors['bg_card'], 
                                    highlightbackground=self.colors['border'], highlightthickness=1)
        leaderboard_card.pack(fill=tk.X, pady=10, padx=20)
        
        tk.Label(leaderboard_card, text="🏆 Weekly Leaderboard", font=("Segoe UI", 16, "bold"), 
                bg=self.colors['bg_card']).pack(pady=15, padx=20, anchor='w')
        
        if leaderboard:
            for i, (username, hours, focus, score) in enumerate(leaderboard[:5], 1):
                rank_color = self.colors['warning'] if i <= 3 else self.colors['bg_light']
                rank_box = tk.Frame(leaderboard_card, bg=rank_color)
                rank_box.pack(fill=tk.X, padx=20, pady=3)
                
                tk.Label(rank_box, text=f"#{i}", font=("Segoe UI", 12, "bold"), 
                        bg=rank_color, width=3).pack(side=tk.LEFT, padx=10, pady=5)
                tk.Label(rank_box, text=username, font=("Segoe UI", 11), 
                        bg=rank_color).pack(side=tk.LEFT, padx=10)
                tk.Label(rank_box, text=f"{hours}h | {score} pts", font=("Segoe UI", 10), 
                        bg=rank_color, fg=self.colors['text_secondary']).pack(side=tk.RIGHT, padx=10)

        # Shop
        shop_card = tk.Frame(scrollable_frame, bg=self.colors['bg_card'], 
                            highlightbackground=self.colors['border'], highlightthickness=1)
        shop_card.pack(fill=tk.X, pady=10, padx=20)
        
        tk.Label(shop_card, text="🛒 Rewards Shop", font=("Segoe UI", 16, "bold"), 
                bg=self.colors['bg_card']).pack(pady=15, padx=20, anchor='w')
        
        rewards = self.gamification.get_available_rewards()
        
        for reward in rewards[:5]:
            reward_box = tk.Frame(shop_card, bg=self.colors['bg_light'])
            reward_box.pack(fill=tk.X, padx=20, pady=5)
            
            tk.Label(reward_box, text=reward['name'], font=("Segoe UI", 11), 
                    bg=self.colors['bg_light']).pack(side=tk.LEFT, padx=15, pady=8)
            
            buy_btn = tk.Button(reward_box, text=f"Buy ({reward['cost']} 🪙)", 
                              command=lambda r=reward: self.purchase_reward(r),
                              font=("Segoe UI", 9, "bold"), bg=self.colors['primary'], 
                              fg="white", relief=tk.FLAT, cursor="hand2")
            buy_btn.pack(side=tk.RIGHT, padx=15)

        # Export Report Section
        export_card = tk.Frame(scrollable_frame, bg=self.colors['bg_card'], 
                              highlightbackground=self.colors['border'], highlightthickness=1)
        export_card.pack(fill=tk.X, pady=10, padx=20)
        
        tk.Label(export_card, text="📄 Export Report", font=("Segoe UI", 16, "bold"), 
                bg=self.colors['bg_card']).pack(pady=15, padx=20, anchor='w')
        
        tk.Button(export_card, text="📥 Generate PDF Report", command=self.export_pdf,
                 font=("Segoe UI", 12, "bold"), width=25, height=2,
                 bg=self.colors['secondary'], fg="white", relief=tk.FLAT).pack(pady=10)

    def play_music(self, genre='lofi'):
        self.music_player.load_playlist(genre)
        messagebox.showinfo("Music", f"Playing {genre.capitalize()} study music!")
    
    def stop_music(self):
        self.music_player.stop()
        messagebox.showinfo("Music", "Music stopped")

    def create_notes_tab(self):
        notes_frame = tk.Frame(self.notebook, bg=self.colors['bg_light'])
        self.notebook.add(notes_frame, text="📝 Notes & Tasks")
        self._build_notes_ui(notes_frame)
    
    def _build_notes_ui(self, notes_frame):
        # Split into two sections
        left_frame = tk.Frame(notes_frame, bg=self.colors['bg_light'])
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        right_frame = tk.Frame(notes_frame, bg=self.colors['bg_light'])
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Notes section
        tk.Label(left_frame, text="📝 Study Notes", font=("Segoe UI", 16, "bold"), 
                bg=self.colors['bg_light']).pack(pady=10)
        
        tk.Button(left_frame, text="+ Add Note", command=self.add_note,
                 font=("Segoe UI", 11, "bold"), bg=self.colors['primary'], 
                 fg="white", relief=tk.FLAT).pack(pady=5)

        # Tasks section
        tk.Label(right_frame, text="✅ To-Do Tasks", font=("Segoe UI", 16, "bold"), 
                bg=self.colors['bg_light']).pack(pady=10)
        
        tk.Button(right_frame, text="+ Add Task", command=self.add_task,
                 font=("Segoe UI", 11, "bold"), bg=self.colors['success'], 
                 fg="white", relief=tk.FLAT).pack(pady=5)

    def create_groups_tab(self):
        groups_frame = tk.Frame(self.notebook, bg=self.colors['bg_light'])
        self.notebook.add(groups_frame, text="👥 Groups")
        self._build_groups_ui(groups_frame)
    
    def _build_groups_ui(self, groups_frame):
        tk.Label(groups_frame, text="👥 Study Groups", font=("Segoe UI", 20, "bold"), 
                bg=self.colors['bg_light']).pack(pady=20)

        btn_frame = tk.Frame(groups_frame, bg=self.colors['bg_light'])
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Create Group", command=self.create_group,
                 font=("Segoe UI", 12, "bold"), width=15, height=2,
                 bg=self.colors['primary'], fg="white", relief=tk.FLAT).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="Join Group", command=self.join_group,
                 font=("Segoe UI", 12, "bold"), width=15, height=2,
                 bg=self.colors['success'], fg="white", relief=tk.FLAT).pack(side=tk.LEFT, padx=5)

        # My groups
        groups = self.study_groups.get_user_groups(self.current_user)
        
        if groups:
            tk.Label(groups_frame, text="My Groups:", font=("Segoe UI", 14, "bold"), 
                    bg=self.colors['bg_light']).pack(pady=10)
            
            for group_id, name, desc, members, role in groups:
                group_card = tk.Frame(groups_frame, bg=self.colors['bg_card'], 
                                     highlightbackground=self.colors['border'], highlightthickness=1)
                group_card.pack(fill=tk.X, padx=20, pady=5)
                
                # Thumbnail
                group_info = self.study_groups.get_group_info(group_id)
                thumbnail_path = group_info[6] if group_info and len(group_info) > 6 else None
                
                thumbnail_widget = self.thumbnail_manager.create_thumbnail_widget(
                    group_card, thumbnail_path, size=(60, 60))
                thumbnail_widget.pack(side=tk.LEFT, padx=10, pady=10)
                
                info_frame = tk.Frame(group_card, bg=self.colors['bg_card'])
                info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15, pady=10)
                
                tk.Label(info_frame, text=f"{name}", 
                        font=("Segoe UI", 12, "bold"), bg=self.colors['bg_card']).pack(anchor='w')
                
                tk.Label(info_frame, text=f"Group ID: {group_id} | {members} members | Role: {role}", 
                        font=("Segoe UI", 9), bg=self.colors['bg_card'], 
                        fg=self.colors['text_secondary']).pack(anchor='w')
                
                tk.Button(group_card, text="View", command=lambda gid=group_id: self.view_group(gid),
                         font=("Segoe UI", 10), bg=self.colors['primary'], 
                         fg="white", relief=tk.FLAT).pack(side=tk.RIGHT, padx=15)
        else:
            no_groups_frame = tk.Frame(groups_frame, bg=self.colors['bg_card'],
                                      highlightbackground=self.colors['border'], highlightthickness=1)
            no_groups_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
            
            tk.Label(no_groups_frame, text="📚", font=("Arial", 48),
                    bg=self.colors['bg_card']).pack(pady=(40, 10))
            tk.Label(no_groups_frame, text="No Study Groups Yet", 
                    font=("Segoe UI", 16, "bold"), bg=self.colors['bg_card']).pack(pady=10)
            tk.Label(no_groups_frame, text="Create or join a study group to collaborate with others!",
                    font=("Segoe UI", 11), bg=self.colors['bg_card'], 
                    fg=self.colors['text_secondary']).pack(pady=(0, 40))

    def add_note(self):
        messagebox.showinfo("Add Note", "Note feature - Add your study notes here!")
    
    def add_task(self):
        messagebox.showinfo("Add Task", "Task feature - Add your to-do tasks here!")
    
    def create_group(self):
        """Create a new study group"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Create Study Group")
        dialog.geometry("450x400")
        dialog.configure(bg=self.colors['bg_light'])
        
        tk.Label(dialog, text="Create New Study Group", font=("Segoe UI", 16, "bold"),
                bg=self.colors['bg_light']).pack(pady=20)
        
        form_frame = tk.Frame(dialog, bg=self.colors['bg_light'])
        form_frame.pack(pady=10, padx=30)
        
        tk.Label(form_frame, text="Group Name:", font=("Segoe UI", 11),
                bg=self.colors['bg_light']).grid(row=0, column=0, sticky="w", pady=5)
        name_entry = tk.Entry(form_frame, font=("Segoe UI", 12), width=30)
        name_entry.grid(row=0, column=1, pady=5, padx=10)
        
        tk.Label(form_frame, text="Description:", font=("Segoe UI", 11),
                bg=self.colors['bg_light']).grid(row=1, column=0, sticky="w", pady=5)
        desc_entry = tk.Entry(form_frame, font=("Segoe UI", 12), width=30)
        desc_entry.grid(row=1, column=1, pady=5, padx=10)
        
        # Thumbnail section
        thumbnail_frame = tk.Frame(dialog, bg=self.colors['bg_light'])
        thumbnail_frame.pack(pady=15)
        
        thumbnail_path = [None]
        thumbnail_label = tk.Label(thumbnail_frame, text="[Photo]", font=("Arial", 20),
                                   bg=self.colors['bg_card'], width=3, height=1)
        thumbnail_label.pack()
        
        def upload_thumbnail():
            path = self.thumbnail_manager.upload_thumbnail(0)
            if path:
                thumbnail_path[0] = path
                thumbnail_label.config(text="[Uploaded]")
        
        tk.Button(thumbnail_frame, text="Upload Group Photo", command=upload_thumbnail,
                 font=("Segoe UI", 10, "bold"), bg=self.colors['secondary'],
                 fg="white", relief=tk.FLAT).pack(pady=5)
        
        def submit():
            name = name_entry.get().strip()
            description = desc_entry.get().strip()
            
            if not name:
                messagebox.showerror("Error", "Please enter a group name!")
                return
            
            try:
                group_id = self.study_groups.create_group(name, description, self.current_user, thumbnail_path[0])
                if thumbnail_path[0]:
                    final_path = thumbnail_path[0].replace('group_0', f'group_{group_id}')
                    os.rename(thumbnail_path[0], final_path)
                    self.study_groups.update_group_thumbnail(group_id, final_path)
                messagebox.showinfo("Success", f"Study group '{name}' created successfully!")
                dialog.destroy()
                self.refresh_groups_tab()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create group: {str(e)}")
        
        tk.Button(dialog, text="Create Group", command=submit,
                 font=("Segoe UI", 12, "bold"), width=20, height=2,
                 bg=self.colors['primary'], fg="white", relief=tk.FLAT).pack(pady=20)
    
    def join_group(self):
        """Join an existing study group"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Join Study Group")
        dialog.geometry("400x300")
        dialog.configure(bg=self.colors['bg_light'])
        
        tk.Label(dialog, text="Join Study Group", font=("Segoe UI", 16, "bold"),
                bg=self.colors['bg_light']).pack(pady=20)
        
        tk.Label(dialog, text="Enter Group ID:", font=("Segoe UI", 11),
                bg=self.colors['bg_light']).pack(pady=10)
        
        group_id_entry = tk.Entry(dialog, font=("Segoe UI", 12), width=20)
        group_id_entry.pack(pady=10)
        
        def submit():
            group_id = group_id_entry.get().strip()
            
            if not group_id:
                messagebox.showerror("Error", "Please enter a group ID!")
                return
            
            try:
                group_id = int(group_id)
                success = self.study_groups.join_group(group_id, self.current_user)
                if success:
                    messagebox.showinfo("Success", "You have joined the group successfully!")
                    dialog.destroy()
                    self.refresh_groups_tab()
                else:
                    messagebox.showerror("Error", "Failed to join group. You may already be a member.")
            except ValueError:
                messagebox.showerror("Error", "Invalid group ID!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to join group: {str(e)}")
        
        tk.Button(dialog, text="Join Group", command=submit,
                 font=("Segoe UI", 12, "bold"), width=20, height=2,
                 bg=self.colors['primary'], fg="white", relief=tk.FLAT).pack(pady=20)
    
    def refresh_groups_tab(self):
        """Refresh the groups tab to show updated data"""
        try:
            # Find and recreate the groups tab
            for i in range(self.notebook.index("end")):
                if self.notebook.tab(i, "text") == "👥 Groups":
                    self.notebook.forget(i)
                    break
            self.create_groups_tab()
        except:
            pass
    
    def view_group(self, group_id):
        """Open Telegram-style group chat window"""
        group_window = tk.Toplevel(self.root)
        group_window.title("Study Group Chat")
        group_window.geometry("800x600")
        group_window.configure(bg=self.colors['bg_light'])
        
        # Get group info
        group_info = self.study_groups.get_group_info(group_id)
        if not group_info:
            messagebox.showerror("Error", "Group not found!")
            group_window.destroy()
            return
        
        group_name = group_info[1]
        
        # Main container
        main_container = tk.Frame(group_window, bg=self.colors['bg_light'])
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header = tk.Frame(main_container, bg=self.colors['primary'], height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text=f"👥 {group_name}", font=("Segoe UI", 16, "bold"),
                bg=self.colors['primary'], fg="white").pack(side=tk.LEFT, padx=20, pady=15)
        
        members_btn = tk.Button(header, text="👥 Members", 
                               command=lambda: self.show_group_members(group_id),
                               font=("Segoe UI", 10, "bold"), bg=self.colors['success'],
                               fg="white", relief=tk.FLAT, cursor="hand2")
        members_btn.pack(side=tk.RIGHT, padx=10)
        self.add_hover_effect(members_btn, self.colors['success'], '#059669')
        
        # Chat area
        chat_container = tk.Frame(main_container, bg=self.colors['bg_card'])
        chat_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Messages display
        canvas = tk.Canvas(chat_container, bg=self.colors['bg_light'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(chat_container, orient="vertical", command=canvas.yview)
        messages_frame = tk.Frame(canvas, bg=self.colors['bg_light'])
        
        messages_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=messages_frame, anchor="nw", width=750)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        def load_messages():
            """Load and display messages"""
            for widget in messages_frame.winfo_children():
                widget.destroy()
            
            messages = self.study_groups.get_messages(group_id)
            
            if not messages:
                tk.Label(messages_frame, text="💬 No messages yet. Start the conversation!",
                        font=("Segoe UI", 12), bg=self.colors['bg_light'],
                        fg=self.colors['text_secondary']).pack(pady=50)
            else:
                for username, message, timestamp in messages:
                    is_own = username == self.current_user
                    
                    msg_container = tk.Frame(messages_frame, bg=self.colors['bg_light'])
                    msg_container.pack(fill=tk.X, pady=5, padx=10)
                    
                    if is_own:
                        # Own message (right side)
                        msg_frame = tk.Frame(msg_container, bg=self.colors['primary'],
                                           highlightbackground=self.colors['primary'], highlightthickness=1)
                        msg_frame.pack(side=tk.RIGHT, anchor='e', padx=5)
                        
                        tk.Label(msg_frame, text=message, font=("Segoe UI", 11),
                                bg=self.colors['primary'], fg="white",
                                wraplength=400, justify=tk.LEFT).pack(padx=15, pady=8)
                        
                        time_label = tk.Label(msg_container, text=timestamp.split()[1][:5],
                                            font=("Segoe UI", 8), bg=self.colors['bg_light'],
                                            fg=self.colors['text_secondary'])
                        time_label.pack(side=tk.RIGHT, padx=5)
                    else:
                        # Other's message (left side)
                        name_frame = tk.Frame(msg_container, bg=self.colors['bg_light'])
                        name_frame.pack(side=tk.LEFT, anchor='w')
                        
                        tk.Label(name_frame, text=username, font=("Segoe UI", 9, "bold"),
                                bg=self.colors['bg_light'], fg=self.colors['primary']).pack(anchor='w', padx=5)
                        
                        msg_frame = tk.Frame(msg_container, bg=self.colors['bg_card'],
                                           highlightbackground=self.colors['border'], highlightthickness=1)
                        msg_frame.pack(side=tk.LEFT, anchor='w', padx=5)
                        
                        tk.Label(msg_frame, text=message, font=("Segoe UI", 11),
                                bg=self.colors['bg_card'], fg=self.colors['text_primary'],
                                wraplength=400, justify=tk.LEFT).pack(padx=15, pady=8)
                        
                        time_label = tk.Label(msg_container, text=timestamp.split()[1][:5],
                                            font=("Segoe UI", 8), bg=self.colors['bg_light'],
                                            fg=self.colors['text_secondary'])
                        time_label.pack(side=tk.LEFT, padx=5)
            
            # Auto scroll to bottom
            canvas.update_idletasks()
            canvas.yview_moveto(1.0)
        
        # Input area
        input_frame = tk.Frame(main_container, bg=self.colors['bg_card'], height=80)
        input_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        input_frame.pack_propagate(False)
        
        input_container = tk.Frame(input_frame, bg=self.colors['bg_card'])
        input_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        message_entry = tk.Text(input_container, font=("Segoe UI", 11), height=2,
                               wrap=tk.WORD, relief=tk.FLAT,
                               highlightbackground=self.colors['border'], highlightthickness=2)
        message_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        def send_message(event=None):
            message = message_entry.get("1.0", tk.END).strip()
            if message:
                self.study_groups.send_message(group_id, self.current_user, message)
                message_entry.delete("1.0", tk.END)
                load_messages()
            return "break"  # Prevent default Enter behavior
        
        send_btn = tk.Button(input_container, text="➤ Send", command=send_message,
                            font=("Segoe UI", 12, "bold"), width=10, height=2,
                            bg=self.colors['primary'], fg="white",
                            relief=tk.FLAT, cursor="hand2")
        send_btn.pack(side=tk.RIGHT)
        self.add_hover_effect(send_btn, self.colors['primary'], self.colors['primary_dark'])
        
        # Bind Enter to send (Shift+Enter for new line)
        message_entry.bind('<Return>', send_message)
        message_entry.bind('<Shift-Return>', lambda e: None)  # Allow Shift+Enter for newline
        
        # Refresh button
        refresh_btn = tk.Button(header, text="🔄 Refresh", command=load_messages,
                               font=("Segoe UI", 10, "bold"), bg=self.colors['warning'],
                               fg="white", relief=tk.FLAT, cursor="hand2")
        refresh_btn.pack(side=tk.RIGHT, padx=5)
        self.add_hover_effect(refresh_btn, self.colors['warning'], '#D97706')
        
        # Load initial messages
        load_messages()
    
    def show_group_members(self, group_id):
        """Show group members list"""
        members_window = tk.Toplevel(self.root)
        members_window.title("Group Members")
        members_window.geometry("400x500")
        members_window.configure(bg=self.colors['bg_light'])
        
        main_frame = tk.Frame(members_window, bg=self.colors['bg_card'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(main_frame, text="👥 Group Members", font=("Segoe UI", 18, "bold"),
                bg=self.colors['bg_card']).pack(pady=15)
        
        members = self.study_groups.get_group_members(group_id)
        
        for username, role, joined_at in members:
            member_frame = tk.Frame(main_frame, bg=self.colors['bg_light'],
                                   highlightbackground=self.colors['border'], highlightthickness=1)
            member_frame.pack(fill=tk.X, pady=5, padx=10)
            
            tk.Label(member_frame, text="👤", font=("Arial", 20),
                    bg=self.colors['bg_light']).pack(side=tk.LEFT, padx=10, pady=10)
            
            info_frame = tk.Frame(member_frame, bg=self.colors['bg_light'])
            info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=10)
            
            tk.Label(info_frame, text=username, font=("Segoe UI", 12, "bold"),
                    bg=self.colors['bg_light']).pack(anchor='w')
            
            role_text = f"👑 {role.upper()}" if role == 'admin' else f"✅ {role}"
            tk.Label(info_frame, text=role_text, font=("Segoe UI", 9),
                    bg=self.colors['bg_light'], fg=self.colors['success']).pack(anchor='w')
        
        close_btn = tk.Button(main_frame, text="Close", command=members_window.destroy,
                             font=("Segoe UI", 11, "bold"), width=15, height=2,
                             bg=self.colors['primary'], fg="white", relief=tk.FLAT, cursor="hand2")
        close_btn.pack(pady=15)
        self.add_hover_effect(close_btn, self.colors['primary'], self.colors['primary_dark'])
    
    def toggle_night_mode(self):
        """Toggle between light and dark mode (FREE)"""
        new_theme = 'dark' if self.current_theme == 'light' else 'light'
        self.current_theme = new_theme
        self.colors = self.theme_manager.get_theme(new_theme)
        self.create_main_screen()
    
    def change_theme(self, theme):
        """Change application theme (requires coins for premium themes)"""
        # Light and Dark are FREE
        if theme in ['light', 'dark']:
            self.current_theme = theme
            self.colors = self.theme_manager.get_theme(theme)
            self.create_main_screen()
            return
        
        # Other themes require coins
        coins, _ = self.gamification.get_user_coins(self.current_user)
        cost = 750  # Cost for premium themes
        
        if coins >= cost:
            # Deduct coins
            self.gamification.deduct_coins(self.current_user, cost, f"Purchased {theme} theme")
            self.current_theme = theme
            self.colors = self.theme_manager.get_theme(theme)
            self.create_main_screen()
            messagebox.showinfo("Success", f"{theme.capitalize()} theme activated! {cost} coins deducted.")
        else:
            messagebox.showerror("Insufficient Coins", f"You need {cost} coins to unlock this theme. You have {coins} coins.")
    
    def play_music(self, genre='lofi'):
        """Show Spotify music player dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("🎵 Spotify Music Player")
        dialog.geometry("650x600")
        dialog.configure(bg=self.colors['bg_light'])
        
        main_frame = tk.Frame(dialog, bg=self.colors['bg_card'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(main_frame, text="🎵 Spotify Study Music", font=("Segoe UI", 18, "bold"),
                bg=self.colors['bg_card']).pack(pady=15)
        
        # Connection status
        if not self.music_player.spotify_enabled:
            tk.Label(main_frame, text="⚠️ Spotify not connected", font=("Segoe UI", 12),
                    bg=self.colors['bg_card'], fg=self.colors['danger']).pack(pady=10)
            
            # Connect to Spotify section
            connect_frame = tk.Frame(main_frame, bg=self.colors['bg_light'])
            connect_frame.pack(pady=20, padx=20, fill=tk.X)
            
            tk.Label(connect_frame, text="Connect to Spotify:", font=("Segoe UI", 12, "bold"),
                    bg=self.colors['bg_light']).pack(pady=10)
            
            tk.Label(connect_frame, text="Client ID:", font=("Segoe UI", 10),
                    bg=self.colors['bg_light']).pack(anchor='w', padx=10)
            client_id_entry = tk.Entry(connect_frame, font=("Segoe UI", 10), width=50)
            client_id_entry.pack(pady=5, padx=10)
            
            tk.Label(connect_frame, text="Client Secret:", font=("Segoe UI", 10),
                    bg=self.colors['bg_light']).pack(anchor='w', padx=10)
            client_secret_entry = tk.Entry(connect_frame, font=("Segoe UI", 10), width=50, show="*")
            client_secret_entry.pack(pady=5, padx=10)
            
            def connect_spotify():
                client_id = client_id_entry.get().strip()
                client_secret = client_secret_entry.get().strip()
                if client_id and client_secret:
                    success, msg = self.music_player.connect_spotify(client_id, client_secret)
                    if success:
                        messagebox.showinfo("Success", msg)
                        dialog.destroy()
                        self.play_music()  # Reopen with connected state
                    else:
                        messagebox.showerror("Error", msg)
                else:
                    messagebox.showwarning("Warning", "Please enter both Client ID and Secret")
            
            tk.Button(connect_frame, text="Connect to Spotify", command=connect_spotify,
                     font=("Segoe UI", 11, "bold"), bg=self.colors['success'], 
                     fg="white", relief=tk.FLAT, width=20, height=2).pack(pady=15)
            
            tk.Label(main_frame, text="Or use Spotify Web Player:", font=("Segoe UI", 11),
                    bg=self.colors['bg_card']).pack(pady=10)
            
            tk.Button(main_frame, text="🌐 Open Spotify Web Player", 
                     command=self.music_player.open_spotify_web,
                     font=("Segoe UI", 11, "bold"), bg=self.colors['primary'], 
                     fg="white", relief=tk.FLAT, width=25, height=2).pack(pady=10)
            
            tk.Label(main_frame, text="\nGet API credentials from:\ndeveloper.spotify.com/dashboard", 
                    font=("Segoe UI", 9), bg=self.colors['bg_card'], 
                    fg=self.colors['text_secondary']).pack(pady=10)
        else:
            # Search box
            search_frame = tk.Frame(main_frame, bg=self.colors['bg_card'])
            search_frame.pack(fill=tk.X, pady=10, padx=10)
            
            tk.Label(search_frame, text="🔍 Search Songs:", font=("Segoe UI", 11, "bold"),
                    bg=self.colors['bg_card']).pack(anchor='w', pady=5)
            
            search_input_frame = tk.Frame(search_frame, bg=self.colors['bg_card'])
            search_input_frame.pack(fill=tk.X, pady=5)
            
            search_entry = tk.Entry(search_input_frame, font=("Segoe UI", 11), width=40)
            search_entry.pack(side=tk.LEFT, padx=5)
            
            # Results frame with scrollbar
            results_container = tk.Frame(main_frame, bg=self.colors['bg_card'])
            results_container.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)
            
            canvas = tk.Canvas(results_container, bg=self.colors['bg_light'], highlightthickness=0)
            scrollbar = ttk.Scrollbar(results_container, orient="vertical", command=canvas.yview)
            results_frame = tk.Frame(canvas, bg=self.colors['bg_light'])
            
            results_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
            canvas.create_window((0, 0), window=results_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            def search_music():
                query = search_entry.get().strip()
                if query:
                    # Clear previous results
                    for widget in results_frame.winfo_children():
                        widget.destroy()
                    
                    tk.Label(results_frame, text="Searching...", font=("Segoe UI", 10),
                            bg=self.colors['bg_light']).pack(pady=10)
                    results_frame.update()
                    
                    tracks = self.music_player.search_tracks(query, limit=15)
                    
                    # Clear searching message
                    for widget in results_frame.winfo_children():
                        widget.destroy()
                    
                    if tracks:
                        tk.Label(results_frame, text=f"Found {len(tracks)} songs:", 
                                font=("Segoe UI", 11, "bold"), bg=self.colors['bg_light']).pack(pady=5)
                        
                        for track in tracks:
                            track_frame = tk.Frame(results_frame, bg=self.colors['bg_card'],
                                                  highlightbackground=self.colors['border'], highlightthickness=1)
                            track_frame.pack(fill=tk.X, pady=3, padx=5)
                            
                            info_frame = tk.Frame(track_frame, bg=self.colors['bg_card'])
                            info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=8)
                            
                            tk.Label(info_frame, text=track['name'], font=("Segoe UI", 10, "bold"),
                                    bg=self.colors['bg_card'], anchor='w').pack(anchor='w')
                            tk.Label(info_frame, text=track['artist'], font=("Segoe UI", 9),
                                    bg=self.colors['bg_card'], fg=self.colors['text_secondary'], anchor='w').pack(anchor='w')
                            
                            play_btn = tk.Button(track_frame, text="▶️ Play",
                                               command=lambda t=track['uri']: self.play_spotify_track(t),
                                               font=("Segoe UI", 9, "bold"), bg=self.colors['success'],
                                               fg="white", relief=tk.FLAT, width=8, cursor="hand2")
                            play_btn.pack(side=tk.RIGHT, padx=10)
                            self.add_hover_effect(play_btn, self.colors['success'], '#059669')
                    else:
                        tk.Label(results_frame, text="No songs found. Try a different search.",
                                font=("Segoe UI", 10), bg=self.colors['bg_light'],
                                fg=self.colors['text_secondary']).pack(pady=20)
                else:
                    messagebox.showwarning("Warning", "Please enter a song name to search")
            
            search_btn = tk.Button(search_input_frame, text="🔍 Search", command=search_music,
                                  font=("Segoe UI", 10, "bold"), bg=self.colors['primary'],
                                  fg="white", relief=tk.FLAT, width=12, cursor="hand2")
            search_btn.pack(side=tk.LEFT, padx=5)
            self.add_hover_effect(search_btn, self.colors['primary'], self.colors['primary_dark'])
            
            # Bind Enter key to search
            search_entry.bind('<Return>', lambda e: search_music())
            
            # Playlists button
            def show_playlists():
                for widget in results_frame.winfo_children():
                    widget.destroy()
                
                tk.Label(results_frame, text="Loading playlists...", font=("Segoe UI", 10),
                        bg=self.colors['bg_light']).pack(pady=10)
                results_frame.update()
                
                playlists = self.music_player.get_playlists()
                
                for widget in results_frame.winfo_children():
                    widget.destroy()
                
                if playlists:
                    tk.Label(results_frame, text="Your Playlists:", font=("Segoe UI", 11, "bold"),
                            bg=self.colors['bg_light']).pack(pady=5)
                    
                    for playlist in playlists:
                        pl_frame = tk.Frame(results_frame, bg=self.colors['bg_card'],
                                           highlightbackground=self.colors['border'], highlightthickness=1)
                        pl_frame.pack(fill=tk.X, pady=3, padx=5)
                        
                        info_frame = tk.Frame(pl_frame, bg=self.colors['bg_card'])
                        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=8)
                        
                        tk.Label(info_frame, text=playlist['name'], font=("Segoe UI", 10, "bold"),
                                bg=self.colors['bg_card'], anchor='w').pack(anchor='w')
                        tk.Label(info_frame, text=f"{playlist['tracks']} tracks", font=("Segoe UI", 9),
                                bg=self.colors['bg_card'], fg=self.colors['text_secondary'], anchor='w').pack(anchor='w')
                        
                        play_btn = tk.Button(pl_frame, text="▶️ Play",
                                           command=lambda pid=playlist['id']: self.play_spotify_playlist(pid),
                                           font=("Segoe UI", 9, "bold"), bg=self.colors['secondary'],
                                           fg="white", relief=tk.FLAT, width=8, cursor="hand2")
                        play_btn.pack(side=tk.RIGHT, padx=10)
                        self.add_hover_effect(play_btn, self.colors['secondary'], '#7C3AED')
                else:
                    tk.Label(results_frame, text="No playlists found.", font=("Segoe UI", 10),
                            bg=self.colors['bg_light'], fg=self.colors['text_secondary']).pack(pady=20)
            
            playlist_btn = tk.Button(search_input_frame, text="📋 My Playlists", command=show_playlists,
                                    font=("Segoe UI", 10, "bold"), bg=self.colors['secondary'],
                                    fg="white", relief=tk.FLAT, width=15, cursor="hand2")
            playlist_btn.pack(side=tk.LEFT, padx=5)
            self.add_hover_effect(playlist_btn, self.colors['secondary'], '#7C3AED')
            
            # Playback controls
            controls_frame = tk.Frame(main_frame, bg=self.colors['bg_card'])
            controls_frame.pack(pady=15)
            
            tk.Label(controls_frame, text="Playback Controls:", font=("Segoe UI", 10, "bold"),
                    bg=self.colors['bg_card']).pack(pady=5)
            
            buttons_frame = tk.Frame(controls_frame, bg=self.colors['bg_card'])
            buttons_frame.pack()
            
            prev_btn = tk.Button(buttons_frame, text="⏮️", command=self.music_player.previous_track,
                                font=("Segoe UI", 14), width=4, bg=self.colors['primary'],
                                fg="white", relief=tk.FLAT, cursor="hand2")
            prev_btn.pack(side=tk.LEFT, padx=3)
            self.add_hover_effect(prev_btn, self.colors['primary'], self.colors['primary_dark'])
            
            pause_btn = tk.Button(buttons_frame, text="⏸️", command=self.music_player.pause,
                                 font=("Segoe UI", 14), width=4, bg=self.colors['warning'],
                                 fg="white", relief=tk.FLAT, cursor="hand2")
            pause_btn.pack(side=tk.LEFT, padx=3)
            self.add_hover_effect(pause_btn, self.colors['warning'], '#D97706')
            
            resume_btn = tk.Button(buttons_frame, text="▶️", command=self.music_player.resume,
                                  font=("Segoe UI", 14), width=4, bg=self.colors['success'],
                                  fg="white", relief=tk.FLAT, cursor="hand2")
            resume_btn.pack(side=tk.LEFT, padx=3)
            self.add_hover_effect(resume_btn, self.colors['success'], '#059669')
            
            next_btn = tk.Button(buttons_frame, text="⏭️", command=self.music_player.next_track,
                                font=("Segoe UI", 14), width=4, bg=self.colors['primary'],
                                fg="white", relief=tk.FLAT, cursor="hand2")
            next_btn.pack(side=tk.LEFT, padx=3)
            self.add_hover_effect(next_btn, self.colors['primary'], self.colors['primary_dark'])
        
        close_btn = tk.Button(main_frame, text="Close", command=dialog.destroy,
                             font=("Segoe UI", 11, "bold"), width=15, height=2,
                             bg=self.colors['danger'], fg="white", relief=tk.FLAT, cursor="hand2")
        close_btn.pack(pady=10)
        self.add_hover_effect(close_btn, self.colors['danger'], '#DC2626')
    
    def play_spotify_track(self, track_uri):
        """Play a Spotify track"""
        success, msg = self.music_player.play_track(track_uri)
        if success:
            messagebox.showinfo("Playing", "🎵 Track is now playing on Spotify!")
        else:
            messagebox.showerror("Error", msg)
    
    def play_spotify_playlist(self, playlist_id):
        """Play a Spotify playlist"""
        success, msg = self.music_player.play_playlist(playlist_id)
        if success:
            messagebox.showinfo("Playing", "🎵 Playlist is now playing on Spotify!")
        else:
            messagebox.showerror("Error", msg)
    
    def pause_music(self):
        if not self.music_player.enabled:
            messagebox.showwarning("Music Player", "Music player is not available.")
            return
        self.music_player.pause()
        messagebox.showinfo("Music", "Music paused")
    
    def open_youtube_music(self):
        """Open YouTube music player with embedded player"""
        dialog = tk.Toplevel(self.root)
        dialog.title("🎵 YouTube Music Player")
        dialog.geometry("900x700")
        dialog.configure(bg=self.colors['bg_light'])
        
        main_frame = tk.Frame(dialog, bg=self.colors['bg_card'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        header_frame = tk.Frame(main_frame, bg=self.colors['danger'])
        header_frame.pack(fill=tk.X)
        tk.Label(header_frame, text="🎵 YouTube Study Music Player", font=("Segoe UI", 18, "bold"),
                bg=self.colors['danger'], fg="white").pack(pady=15)
        
        # Player frame (embedded YouTube)
        player_frame = tk.Frame(main_frame, bg='black', height=400)
        player_frame.pack(fill=tk.X, pady=10, padx=15)
        player_frame.pack_propagate(False)
        
        player_label = tk.Label(player_frame, text="🎵 Select a song to play", 
                               font=("Segoe UI", 16), bg='black', fg='white')
        player_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Search section
        search_frame = tk.Frame(main_frame, bg=self.colors['bg_card'])
        search_frame.pack(fill=tk.X, pady=10, padx=15)
        
        tk.Label(search_frame, text="🔍 Search:", font=("Segoe UI", 11, "bold"),
                bg=self.colors['bg_card']).pack(side=tk.LEFT, padx=5)
        
        search_entry = tk.Entry(search_frame, font=("Segoe UI", 11), width=40)
        search_entry.pack(side=tk.LEFT, padx=5)
        search_entry.insert(0, "lofi")
        
        # Results container
        results_container = tk.Frame(main_frame, bg=self.colors['bg_card'])
        results_container.pack(fill=tk.BOTH, expand=True, pady=5, padx=15)
        
        canvas = tk.Canvas(results_container, bg=self.colors['bg_light'], highlightthickness=0, height=150)
        scrollbar = ttk.Scrollbar(results_container, orient="vertical", command=canvas.yview)
        results_frame = tk.Frame(canvas, bg=self.colors['bg_light'])
        
        results_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=results_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        def play_in_app(video_id, title):
            """Play video in embedded player"""
            player_label.config(text=f"▶️ Now Playing: {title}")
            # Open in browser for actual playback
            self.youtube_player.play_video(video_id)
        
        def show_results(query=""):
            for widget in results_frame.winfo_children():
                widget.destroy()
            
            results = self.youtube_player.search_songs(query)
            
            for item in results:
                item_frame = tk.Frame(results_frame, bg=self.colors['bg_card'],
                                     highlightbackground=self.colors['border'], highlightthickness=1)
                item_frame.pack(fill=tk.X, pady=3, padx=5)
                
                info_frame = tk.Frame(item_frame, bg=self.colors['bg_card'])
                info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=8)
                
                tk.Label(info_frame, text=item['title'], font=("Segoe UI", 10, "bold"),
                        bg=self.colors['bg_card'], anchor='w').pack(anchor='w')
                
                details = f"⏱️ {item['duration']}"
                if 'channel' in item:
                    details += f" | 📺 {item['channel']}"
                    
                tk.Label(info_frame, text=details, font=("Segoe UI", 8),
                        bg=self.colors['bg_card'], fg=self.colors['text_secondary'], anchor='w').pack(anchor='w')
                
                play_btn = tk.Button(item_frame, text="▶️ Play",
                                   command=lambda vid=item['id'], t=item['title']: play_in_app(vid, t),
                                   font=("Segoe UI", 9, "bold"), bg=self.colors['danger'],
                                   fg="white", relief=tk.FLAT, width=8, cursor="hand2")
                play_btn.pack(side=tk.RIGHT, padx=10)
                self.add_hover_effect(play_btn, self.colors['danger'], '#DC2626')
        
        def search_music():
            query = search_entry.get().strip()
            show_results(query if query else "lofi")
        
        search_btn = tk.Button(search_frame, text="🔍 Search", command=search_music,
                              font=("Segoe UI", 10, "bold"), bg=self.colors['primary'],
                              fg="white", relief=tk.FLAT, width=10, cursor="hand2")
        search_btn.pack(side=tk.LEFT, padx=5)
        self.add_hover_effect(search_btn, self.colors['primary'], self.colors['primary_dark'])
        
        search_entry.bind('<Return>', lambda e: search_music())
        
        def show_playlists():
            for widget in results_frame.winfo_children():
                widget.destroy()
            
            playlists = self.youtube_player.get_study_playlists()
            
            for pl in playlists:
                pl_frame = tk.Frame(results_frame, bg=self.colors['bg_card'],
                                   highlightbackground=self.colors['success'], highlightthickness=2)
                pl_frame.pack(fill=tk.X, pady=3, padx=5)
                
                info_frame = tk.Frame(pl_frame, bg=self.colors['bg_card'])
                info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=8)
                
                tk.Label(info_frame, text=pl['name'], font=("Segoe UI", 10, "bold"),
                        bg=self.colors['bg_card'], anchor='w').pack(anchor='w')
                tk.Label(info_frame, text=f"🕒 {pl['type']}", font=("Segoe UI", 8),
                        bg=self.colors['bg_card'], fg=self.colors['text_secondary'], anchor='w').pack(anchor='w')
                
                play_btn = tk.Button(pl_frame, text="▶️ Play",
                                   command=lambda vid=pl['id'], t=pl['name']: play_in_app(vid, t),
                                   font=("Segoe UI", 9, "bold"), bg=self.colors['success'],
                                   fg="white", relief=tk.FLAT, width=8, cursor="hand2")
                play_btn.pack(side=tk.RIGHT, padx=10)
                self.add_hover_effect(play_btn, self.colors['success'], '#059669')
        
        playlist_btn = tk.Button(search_frame, text="🎧 Playlists", command=show_playlists,
                                font=("Segoe UI", 10, "bold"), bg=self.colors['secondary'],
                                fg="white", relief=tk.FLAT, width=10, cursor="hand2")
        playlist_btn.pack(side=tk.LEFT, padx=5)
        self.add_hover_effect(playlist_btn, self.colors['secondary'], '#7C3AED')
        
        show_results("lofi")
        
        info_frame = tk.Frame(main_frame, bg=self.colors['success_light'])
        info_frame.pack(fill=tk.X, pady=5, padx=15)
        tk.Label(info_frame, text="💡 Music opens in browser. Keep tab in background while studying!",
                font=("Segoe UI", 9), bg=self.colors['success_light']).pack(pady=5)
        
        close_btn = tk.Button(main_frame, text="Close", command=dialog.destroy,
                             font=("Segoe UI", 11, "bold"), width=15, height=2,
                             bg=self.colors['danger'], fg="white", relief=tk.FLAT, cursor="hand2")
        close_btn.pack(pady=5)
        self.add_hover_effect(close_btn, self.colors['danger'], '#DC2626')
    
    def play_youtube_video(self, video_id):
        """Play YouTube video"""
        success = self.youtube_player.play_video(video_id)
        if success:
            messagebox.showinfo("Playing", "🎵 Music is now playing in your browser!\n\nKeep the tab open in background while studying.")
    
    def enable_voice(self):
        messagebox.showinfo("Voice Commands", "Voice commands enabled! Say 'start session' to begin.")
    
    def export_pdf(self):
        try:
            filename = f"{self.current_user}_report.pdf"
            self.report_generator.generate_student_report(self.current_user, filename)
            messagebox.showinfo("Success", f"Report saved as {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {e}")


    def create_profile_tab(self):
        profile_frame = tk.Frame(self.notebook, bg=self.colors['bg_light'])
        self.notebook.add(profile_frame, text="👤 Profile")
        self._build_profile_ui(profile_frame)
    
    def _build_profile_ui(self, profile_frame):
        # Scrollable frame
        canvas = tk.Canvas(profile_frame, bg=self.colors['bg_light'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(profile_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg_light'])

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Get user progress
        progress = self.db.get_student_progress(self.current_user)
        
        # Profile Header Card
        header_card = tk.Frame(scrollable_frame, bg=self.colors['bg_card'], 
                              highlightbackground=self.colors['border'], highlightthickness=1)
        header_card.pack(fill=tk.X, pady=20, padx=20)

        header_content = tk.Frame(header_card, bg=self.colors['bg_card'])
        header_content.pack(pady=25, padx=25)

        # Profile photo section
        photo_section = tk.Frame(header_content, bg=self.colors['bg_card'])
        photo_section.pack(side=tk.LEFT, padx=20)
        
        # Profile avatar
        avatar_frame = tk.Frame(photo_section, bg=self.colors['primary'], 
                               width=120, height=120)
        avatar_frame.pack()
        avatar_frame.pack_propagate(False)
        
        self.profile_avatar_label = tk.Label(avatar_frame, bg=self.colors['primary'])
        self.profile_avatar_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Load profile photo for profile tab
        self.load_profile_avatar()
        
        # Change photo button
        change_photo_btn = tk.Button(photo_section, text="📷 Change Photo", 
                                     command=self.upload_profile_photo,
                                     font=("Segoe UI", 10, "bold"), width=15,
                                     bg=self.colors['primary'], fg="white", 
                                     relief=tk.FLAT, cursor="hand2")
        change_photo_btn.pack(pady=(10, 0))
        self.add_hover_effect(change_photo_btn, self.colors['primary'], self.colors['primary_dark'])

        # Profile info
        info_container = tk.Frame(header_content, bg=self.colors['bg_card'])
        info_container.pack(side=tk.LEFT, padx=20)

        tk.Label(info_container, text=self.current_user, font=("Segoe UI", 24, "bold"), 
                bg=self.colors['bg_card'], fg=self.colors['text_primary']).pack(anchor="w")
        
        # Level and XP
        level = progress.get('Level', 1)
        xp = progress.get('XP', 0)
        xp_next = progress.get('XP to Next Level', 1000)
        
        level_frame = tk.Frame(info_container, bg=self.colors['warning'])
        level_frame.pack(anchor="w", pady=5)
        tk.Label(level_frame, text=f"⭐ Level {level}", font=("Segoe UI", 14, "bold"), 
                bg=self.colors['warning'], fg="white", padx=15, pady=5).pack()
        
        tk.Label(info_container, text=f"XP: {xp} / {xp + xp_next} ({xp_next} to next level)", 
                font=("Segoe UI", 11), bg=self.colors['bg_card'], 
                fg=self.colors['text_secondary']).pack(anchor="w", pady=5)

        # Stats Grid
        stats_card = tk.Frame(scrollable_frame, bg=self.colors['bg_card'], 
                             highlightbackground=self.colors['border'], highlightthickness=1)
        stats_card.pack(fill=tk.X, pady=(0, 20), padx=20)

        tk.Label(stats_card, text="📊 Your Statistics", font=("Segoe UI", 18, "bold"), 
                bg=self.colors['bg_card'], fg=self.colors['text_primary']).pack(pady=(20, 15), padx=20, anchor="w")

        stats_grid = tk.Frame(stats_card, bg=self.colors['bg_card'])
        stats_grid.pack(pady=(0, 20), padx=20, fill=tk.X)

        stats = [
            ("📚", "Total Hours", f"{progress.get('Total Hours', 0):.1f}h", self.colors['primary']),
            ("🔥", "Current Streak", f"{progress.get('Current Streak', 0)} days", self.colors['danger']),
            ("🏆", "Badges Earned", str(progress.get('Badges Earned', 0)), self.colors['warning']),
            ("✅", "Perfect Sessions", str(progress.get('Perfect Sessions', 0)), self.colors['success'])
        ]

        for i, (emoji, label, value, color) in enumerate(stats):
            stat_box = tk.Frame(stats_grid, bg=color, highlightbackground=color, highlightthickness=2)
            stat_box.grid(row=i//2, column=i%2, padx=10, pady=10, sticky="ew")
            stats_grid.columnconfigure(i%2, weight=1)
            
            tk.Label(stat_box, text=emoji, font=("Arial", 32), bg=color).pack(pady=(15, 5))
            tk.Label(stat_box, text=value, font=("Segoe UI", 20, "bold"), 
                    bg=color, fg="white").pack()
            tk.Label(stat_box, text=label, font=("Segoe UI", 11), 
                    bg=color, fg="white").pack(pady=(0, 15))

        # All Badges Button
        view_badges_btn = tk.Button(stats_card, text="🏆 View All Badges", 
                                    command=self.show_all_badges,
                                    font=("Segoe UI", 12, "bold"), width=25, height=2,
                                    bg=self.colors['secondary'], fg="white", relief=tk.FLAT, cursor="hand2")
        view_badges_btn.pack(pady=(0, 20))
        self.add_hover_effect(view_badges_btn, self.colors['secondary'], '#7C3AED')

        # Recent Badges Preview
        badges_preview_card = tk.Frame(scrollable_frame, bg=self.colors['bg_card'], 
                                      highlightbackground=self.colors['border'], highlightthickness=1)
        badges_preview_card.pack(fill=tk.X, pady=(0, 20), padx=20)

        tk.Label(badges_preview_card, text="🏆 Recent Achievements", font=("Segoe UI", 18, "bold"), 
                bg=self.colors['bg_card'], fg=self.colors['text_primary']).pack(pady=(20, 15), padx=20, anchor="w")

        # Learning Roadmap
        roadmap_frame = tk.Frame(badges_preview_card, bg=self.colors['bg_card'])
        roadmap_frame.pack(pady=(0, 20), padx=20, fill=tk.X)

        self.roadmap_canvas = tk.Canvas(roadmap_frame, height=100, bg=self.colors['bg_card'], highlightthickness=0)
        self.roadmap_canvas.pack(fill=tk.X)
        self.draw_roadmap()

        # Actions Card
        actions_card = tk.Frame(scrollable_frame, bg=self.colors['bg_card'], 
                               highlightbackground=self.colors['border'], highlightthickness=1)
        actions_card.pack(fill=tk.X, pady=(0, 20), padx=20)

        tk.Label(actions_card, text="⚙️ Account Actions", font=("Segoe UI", 18, "bold"), 
                bg=self.colors['bg_card'], fg=self.colors['text_primary']).pack(pady=(20, 15), padx=20, anchor="w")

        button_frame = tk.Frame(actions_card, bg=self.colors['bg_card'])
        button_frame.pack(pady=(0, 20), padx=20)

        logout_btn = tk.Button(button_frame, text="🚪 Logout", command=self.logout,
                              font=("Segoe UI", 12, "bold"), width=25, height=2,
                              bg=self.colors['danger'], fg="white", relief=tk.FLAT, cursor="hand2")
        logout_btn.pack(pady=5)
        self.add_hover_effect(logout_btn, self.colors['danger'], '#DC2626')

    def show_all_badges(self):
        """Show comprehensive badge collection window"""
        badges_window = tk.Toplevel(self.root)
        badges_window.title("🏆 Your Badge Collection")
        badges_window.geometry("700x600")
        badges_window.configure(bg=self.colors['bg_light'])

        # Header
        header = tk.Frame(badges_window, bg=self.colors['primary'])
        header.pack(fill=tk.X)
        tk.Label(header, text="🏆 Badge Collection", font=("Segoe UI", 22, "bold"), 
                bg=self.colors['primary'], fg="white").pack(pady=20)

        # Get all earned badges
        earned_badges = self.db.get_earned_badges(self.current_user)
        earned_ids = [b['id'] for b in earned_badges]

        # Scrollable frame for badges
        canvas = tk.Canvas(badges_window, bg=self.colors['bg_light'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(badges_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg_light'])

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        scrollbar.pack(side="right", fill="y")

        # Badge categories
        categories = {
            "Milestones": [
                ("first_steps", "🎯 First Steps", "1 hour"),
                ("getting_started", "📚 Getting Started", "5 hours"),
                ("dedicated_learner", "💪 Dedicated Learner", "10 hours"),
                ("study_enthusiast", "⭐ Study Enthusiast", "25 hours"),
                ("knowledge_seeker", "🔍 Knowledge Seeker", "50 hours"),
                ("study_master", "🏆 Study Master", "100 hours")
            ],
            "Streaks": [
                ("consistent_starter", "🔥 Consistent Starter", "3 day streak"),
                ("week_warrior", "⚡ Week Warrior", "7 day streak"),
                ("fortnight_champion", "💥 Fortnight Champion", "14 day streak"),
                ("monthly_master", "🌙 Monthly Master", "30 day streak")
            ],
            "Special": [
                ("early_bird", "🌅 Early Bird", "Study before 8 AM"),
                ("night_owl", "🦉 Night Owl", "Study after 10 PM"),
                ("weekend_warrior", "🎮 Weekend Warrior", "Study on weekends"),
                ("marathon", "🏃 Marathon", "5+ hour session"),
                ("focus_master", "💎 Focus Master", "50 perfect sessions")
            ]
        }

        for category, badges_list in categories.items():
            # Category header
            cat_header = tk.Frame(scrollable_frame, bg=self.colors['bg_card'], 
                                 highlightbackground=self.colors['border'], highlightthickness=1)
            cat_header.pack(fill=tk.X, pady=(0, 10))
            tk.Label(cat_header, text=category, font=("Segoe UI", 16, "bold"), 
                    bg=self.colors['bg_card'], fg=self.colors['text_primary']).pack(pady=10, padx=15, anchor="w")

            # Badges grid
            badges_grid = tk.Frame(scrollable_frame, bg=self.colors['bg_light'])
            badges_grid.pack(fill=tk.X, pady=(0, 20))

            for i, (badge_id, badge_name, requirement) in enumerate(badges_list):
                unlocked = badge_id in earned_ids
                
                badge_card = tk.Frame(badges_grid, 
                                     bg=self.colors['success'] if unlocked else self.colors['border'],
                                     highlightbackground=self.colors['primary'] if unlocked else self.colors['border'],
                                     highlightthickness=2, cursor="hand2" if unlocked else "")
                badge_card.grid(row=i//3, column=i%3, padx=5, pady=5, sticky="ew")
                badges_grid.columnconfigure(i%3, weight=1)

                # Badge content
                emoji = badge_name.split()[0]
                name = ' '.join(badge_name.split()[1:])
                
                tk.Label(badge_card, text=emoji if unlocked else "🔒", font=("Arial", 32),
                        bg=self.colors['success'] if unlocked else self.colors['border']).pack(pady=(10, 5))
                tk.Label(badge_card, text=name, font=("Segoe UI", 11, "bold"),
                        bg=self.colors['success'] if unlocked else self.colors['border'],
                        fg="white" if unlocked else self.colors['text_secondary']).pack()
                tk.Label(badge_card, text=requirement, font=("Segoe UI", 9),
                        bg=self.colors['success'] if unlocked else self.colors['border'],
                        fg="white" if unlocked else self.colors['text_secondary']).pack(pady=(0, 10))

        # Close button
        close_btn = tk.Button(badges_window, text="Close", command=badges_window.destroy,
                             font=("Segoe UI", 12, "bold"), width=20, height=2,
                             bg=self.colors['primary'], fg="white", relief=tk.FLAT, cursor="hand2")
        close_btn.pack(pady=10)
        self.add_hover_effect(close_btn, self.colors['primary'], self.colors['primary_dark'])

    def start_study_session(self):
        session_window = tk.Toplevel(self.root)
        session_window.title("Start Study Session")
        session_window.geometry("350x300")

        main_frame = tk.Frame(session_window, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        tk.Label(main_frame, text="Select Study Hours (0-24):", font=("Arial", 14), bg="#f0f0f0").pack(pady=20)
        self.hours_var = tk.DoubleVar()
        hours_spin = tk.Spinbox(main_frame, from_=0, to=24, increment=0.5, textvariable=self.hours_var, font=("Arial", 12))
        hours_spin.pack(pady=10)

        # Camera monitoring option
        self.camera_var = tk.BooleanVar(value=True)
        camera_check = tk.Checkbutton(main_frame, text="Enable Camera Monitoring (Detect if student is present)", variable=self.camera_var, font=("Arial", 12), bg="#f0f0f0")
        camera_check.pack(pady=10)

        # Study detection option (only shown if camera is enabled)
        self.study_detect_var = tk.BooleanVar(value=False)
        study_check = tk.Checkbutton(main_frame, text="Enable Study Activity Detection (Advanced monitoring)", variable=self.study_detect_var, font=("Arial", 12), bg="#f0f0f0")
        study_check.pack(pady=5)

        button_style = {"font": ("Arial", 12), "width": 15, "height": 1, "bg": "#4CAF50", "fg": "white", "relief": tk.RAISED}
        tk.Button(main_frame, text="Start Session", command=lambda: self.begin_session(session_window), **button_style).pack(pady=20)

    def begin_session(self, window):
        hours = self.hours_var.get()
        camera_enabled = self.camera_var.get()
        study_detect_enabled = self.study_detect_var.get()
        if hours <= 0:
            messagebox.showerror("Error", "Please select valid hours")
            return

        if window:
            window.destroy()

        # Get session ID
        conn = sqlite3.connect(self.db.db_name)
        c_db = conn.cursor()
        c_db.execute("SELECT MAX(id) FROM study_sessions WHERE username=?", (self.current_user,))
        result = c_db.fetchone()
        self.current_session_id = (result[0] if result[0] else 0) + 1
        conn.close()
        self.session_running = True

        # Initialize session tracking
        self.session_warnings = 0
        self.session_start_time = time.time()

        # Start monitoring in a thread to avoid blocking UI
        self.monitor_thread = threading.Thread(target=self.run_session, args=(hours, camera_enabled, study_detect_enabled))
        self.monitor_thread.start()

        # Show enhanced monitoring window
        self.monitor_window = tk.Toplevel(self.root)
        self.monitor_window.title("🎯 Study Session in Progress")
        self.monitor_window.geometry("600x450")
        self.monitor_window.configure(bg=self.colors['bg_light'])

        main_frame = tk.Frame(self.monitor_window, bg=self.colors['bg_card'], 
                             highlightbackground=self.colors['border'], highlightthickness=2)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header
        header_frame = tk.Frame(main_frame, bg=self.colors['success'], 
                               highlightbackground=self.colors['success'], highlightthickness=2)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        monitoring_text = f"📚 Studying for {hours} hours"
        if camera_enabled and study_detect_enabled:
            monitoring_text += " (Advanced Monitoring Active)"
        elif camera_enabled:
            monitoring_text += " (Face Detection Active)"
        else:
            monitoring_text += " (Manual Session)"
            
        tk.Label(header_frame, text=monitoring_text, font=("Segoe UI", 14, "bold"), 
                bg=self.colors['success'], fg="white").pack(pady=15)

        # Status display
        status_container = tk.Frame(main_frame, bg=self.colors['bg_card'])
        status_container.pack(fill=tk.BOTH, expand=True, pady=10)

        self.status_label = tk.Label(status_container, text="✅ Session Active", 
                                     font=("Segoe UI", 16, "bold"), 
                                     bg=self.colors['bg_card'], fg=self.colors['success'])
        self.status_label.pack(pady=10)

        # NEW: Focus Score display
        self.focus_score_label = tk.Label(status_container, text="Focus Score: --", 
                                         font=("Segoe UI", 14, "bold"), 
                                         bg=self.colors['bg_card'], fg=self.colors['primary'])
        self.focus_score_label.pack(pady=5)
        
        # NEW: Current App display
        self.app_label = tk.Label(status_container, text="App: Initializing...", 
                                 font=("Segoe UI", 11), bg=self.colors['bg_card'], 
                                 fg=self.colors['text_secondary'])
        self.app_label.pack(pady=5)

        # Warnings display
        self.warning_label = tk.Label(status_container, text="⚠️ Warnings: 0", 
                                       font=("Segoe UI", 14), bg=self.colors['bg_card'], 
                                       fg=self.colors['text_secondary'])
        self.warning_label.pack(pady=5)

        # Time display
        self.time_label = tk.Label(status_container, text="⏱️ Time: 0:00 / 0:00", 
                                   font=("Segoe UI", 12), bg=self.colors['bg_card'], 
                                   fg=self.colors['text_secondary'])
        self.time_label.pack(pady=5)

        # Warning message area
        self.warning_text = tk.Text(status_container, height=6, width=50, 
                                   font=("Segoe UI", 10), bg=self.colors['bg_light'],
                                   relief=tk.FLAT, state=tk.DISABLED)
        self.warning_text.pack(pady=15, padx=20, fill=tk.X)

        # Progress indicator
        self.session_progress = ttk.Progressbar(status_container, orient="horizontal", 
                                               length=400, mode="determinate")
        self.session_progress.pack(pady=10)

        # Motivational message
        self.motivation_label = tk.Label(status_container, 
                                        text="💪 Stay focused! You're doing great!", 
                                        font=("Segoe UI", 11, "italic"), 
                                        bg=self.colors['bg_card'], fg=self.colors['primary'])
        self.motivation_label.pack(pady=10)

        # Buttons
        button_frame = tk.Frame(main_frame, bg=self.colors['bg_card'])
        button_frame.pack(pady=10)

        stop_btn = tk.Button(button_frame, text="⏸️ Stop Session", command=self.stop_session,
                            font=("Segoe UI", 12, "bold"), width=20, height=2,
                            bg=self.colors['danger'], fg="white", relief=tk.FLAT, cursor="hand2")
        stop_btn.pack()
        self.add_hover_effect(stop_btn, self.colors['danger'], '#DC2626')

        # Start updating the UI
        self.update_session_ui(hours)

    def update_session_ui(self, total_hours):
        """Update session UI with elapsed time and progress"""
        if not hasattr(self, 'monitor_window') or not self.monitor_window.winfo_exists():
            return

        elapsed = time.time() - self.session_start_time
        elapsed_minutes = int(elapsed // 60)
        elapsed_seconds = int(elapsed % 60)
        
        total_seconds = total_hours * 3600
        remaining = max(0, total_seconds - elapsed)
        remaining_minutes = int(remaining // 60)
        remaining_seconds = int(remaining % 60)

        # Update time label
        self.time_label.config(
            text=f"⏱️ Time: {elapsed_minutes}:{elapsed_seconds:02d} / {int(total_hours*60)}:{0:02d}"
        )

        # Update progress bar
        progress = min(100, (elapsed / total_seconds) * 100)
        self.session_progress['value'] = progress

        # Update motivational messages based on progress
        if progress < 25:
            motivation = "💪 Great start! Keep going!"
        elif progress < 50:
            motivation = "🌟 You're making progress! Stay focused!"
        elif progress < 75:
            motivation = "🔥 More than halfway there! Amazing!"
        else:
            motivation = "🎉 Almost done! Finish strong!"
        
        self.motivation_label.config(text=motivation)

        # Schedule next update
        self.root.after(1000, lambda: self.update_session_ui(total_hours))

    def handle_monitoring_update(self, update_data):
        """Handle monitoring updates from face detector"""
        if not hasattr(self, 'monitor_window') or not self.monitor_window.winfo_exists():
            return

        if update_data['status'] == 'warning':
            self.session_warnings = update_data['warnings']
            self.warnings_label.config(text=f"⚠️ Warnings: {self.session_warnings}")
            
            # Add warning message
            self.warning_text.config(state=tk.NORMAL)
            self.warning_text.insert(tk.END, f"\n{update_data['message']}")
            self.warning_text.see(tk.END)
            self.warning_text.config(state=tk.DISABLED)
            
            # Change status color if too many warnings
            if self.session_warnings > 3:
                self.status_label.config(text="⚠️ Multiple Warnings!", fg=self.colors['warning'])
            if self.session_warnings > 5:
                self.status_label.config(text="❌ Too Many Warnings!", fg=self.colors['danger'])

    def run_session(self, hours, camera_enabled, study_detect_enabled=False):
        try:
            # Activity logging already initialized in begin_session
            self.activity_monitor.start_monitoring()
            self.focus_scorer.reset_warnings()
            
            # Log session start
            self.activity_logger.log_activity(self.current_user, self.current_session_id, 
                                             'SESSION_START', 'Study Tracker', 'Session Started')
            
            # Start screenshot thread
            import random
            def take_random_screenshots():
                import time as time_module
                while self.session_running:
                    time_module.sleep(random.randint(120, 300))
                    if self.session_running:
                        app_name, window_title = self.activity_logger.get_active_window_info()
                        self.activity_logger.take_screenshot(self.current_user, self.current_session_id, 
                                                            f"{app_name}: {window_title}")
                        self.activity_logger.log_activity(self.current_user, self.current_session_id,
                                                         'APP_USAGE', app_name, window_title)
            
            screenshot_thread = threading.Thread(target=take_random_screenshots, daemon=True)
            screenshot_thread.start()
            
            if camera_enabled:
                camera_ok = self.face_detector.start_camera()
                if camera_ok:
                    result = self.monitor_with_fusion(hours)
                else:
                    print("Camera failed - using desktop monitoring only")
                    result = self.monitor_desktop_only(hours)
            else:
                result = self.monitor_desktop_only(hours)
            
            self.session_running = False
            self.activity_monitor.stop_monitoring()
            
            # Unblock websites
            if self.websites_blocked:
                self.website_blocker.unblock_websites()
                self.websites_blocked = False
            
            # Award coins
            coins_earned = int(hours * 50)
            self.gamification.award_coins(self.current_user, coins_earned, "Session completed")
            
            # Update leaderboard
            self.gamification.update_leaderboard(self.current_user, hours, result.get("focus_score", 100))
            
            # Log session end
            self.activity_logger.log_activity(self.current_user, self.current_session_id,
                                             'SESSION_END', 'Study Tracker', 'Session Completed')
            
            self.root.after(0, lambda: self.end_session(result))
        except Exception as e:
            self.session_running = False
            self.activity_monitor.stop_monitoring()
            
            # Unblock websites
            if self.websites_blocked:
                self.website_blocker.unblock_websites()
                self.websites_blocked = False
            
            # Award coins
            coins_earned = int(hours * 50)
            self.gamification.award_coins(self.current_user, coins_earned, "Session completed")
            
            # Update leaderboard
            self.gamification.update_leaderboard(self.current_user, hours, result.get("focus_score", 100))
            self.root.after(0, lambda: messagebox.showerror("Error", f"Session failed: {str(e)}"))
    
    def monitor_with_fusion(self, hours):
        """NEW: Monitor using multi-signal fusion (app + camera)"""
        start_time = time.time()
        end_time = start_time + (hours * 3600)
        
        last_update = start_time
        update_interval = 1  # Update every second
        
        while time.time() < end_time:
            current_time = time.time()
            
            # Calculate focus score every second
            if current_time - last_update >= update_interval:
                score, breakdown, recommendation = self.focus_scorer.calculate_focus_score()
                last_update = current_time
                
                # Update UI
                self.root.after(0, lambda s=score, b=breakdown, r=recommendation: 
                               self.handle_focus_update(s, b, r, current_time - start_time, end_time - current_time))
                
                # Show warning if needed
                if recommendation['should_warn']:
                    self.root.after(0, lambda r=recommendation, b=breakdown: 
                                   self.show_focus_warning(r, b))
            
            time.sleep(0.1)  # Small sleep to prevent CPU overload
        
        # Get session summary
        summary = self.focus_scorer.get_session_summary()
        
        return {
            'success': True,
            'warnings': summary['warnings_issued'],
            'focus_score': summary['average_focus'],
            'peak_focus': summary.get('peak_focus', 100),
            'time_focused': summary.get('time_focused', 0),
            'time_distracted': summary.get('time_distracted', 0)
        }
    
    def monitor_desktop_only(self, hours):
        """NEW: Monitor desktop activity only (no camera)"""
        start_time = time.time()
        end_time = start_time + (hours * 3600)
        
        last_update = start_time
        update_interval = 2  # Update every 2 seconds
        
        warning_count = 0
        focus_scores = []
        
        while time.time() < end_time:
            current_time = time.time()
            
            if current_time - last_update >= update_interval:
                # Get app and pattern scores
                app_score = self.activity_monitor.get_app_usage_score()
                pattern_score = self.activity_monitor.get_interaction_pattern_score()
                
                # Simple fusion (75% app, 25% pattern)
                focus_score = app_score * 0.75 + pattern_score * 0.25
                focus_scores.append(focus_score)
                
                last_update = current_time
                
                # Show warning if distracted
                if focus_score < 40 and len(focus_scores) > 30:  # Sustained low score
                    recent_avg = sum(focus_scores[-30:]) / 30
                    if recent_avg < 40:
                        warning_count += 1
                        app_summary = self.activity_monitor.get_activity_summary()
                        self.root.after(0, lambda: self.show_desktop_warning(app_summary))
                        focus_scores = []  # Reset
                
                # Update UI
                self.root.after(0, lambda s=focus_score: self.update_desktop_monitor(s))
            
            time.sleep(0.5)
        
        avg_score = sum(focus_scores) / len(focus_scores) if focus_scores else 50
        
        return {
            'success': True,
            'warnings': warning_count,
            'focus_score': round(avg_score, 2)
        }
    
    def handle_focus_update(self, score, breakdown, recommendation, elapsed, remaining):
        """NEW: Handle focus score updates"""
        if not self.monitor_window or not self.monitor_window.winfo_exists():
            return
        
        # Update focus score display
        if hasattr(self, 'focus_score_label'):
            status_text = "✅ FOCUSED" if score >= 80 else "💭 DRIFTING" if score >= 60 else "⚠️ DISTRACTED" if score >= 40 else "🚨 HIGH DISTRACTION"
            color = self.colors['success'] if score >= 80 else self.colors['warning'] if score >= 60 else self.colors['danger']
            
            self.focus_score_label.config(text=f"Focus Score: {score:.0f}%", fg=color)
            self.status_label.config(text=status_text, fg=color)
        
        # Update app info
        current_app = self.activity_monitor.current_app or "Unknown"
        app_summary = self.activity_monitor.get_activity_summary()
        
        if hasattr(self, 'app_label'):
            self.app_label.config(text=f"App: {current_app} | {app_summary}")
    
    def show_focus_warning(self, recommendation, breakdown):
        """NEW: Show focus warning"""
        if not self.monitor_window or not self.monitor_window.winfo_exists():
            return
        
        # Increment warning counter
        self.session_warnings += 1
        
        # Update warning display
        if hasattr(self, 'warning_label'):
            self.warning_label.config(text=f"Warnings: {self.session_warnings}")
        
        # Show popup warning
        current_app = self.activity_monitor.current_app or "Unknown app"
        message = recommendation.get('message', 'Please refocus on your studies')
        
        # Make the warning more specific based on detected app
        if 'chrome' in current_app.lower() or 'firefox' in current_app.lower():
            message = "🌐 Browser detected - Are you studying or watching YouTube/entertainment?"
        elif breakdown['app_usage'] < 30:
            message = f"📱 Distraction app detected: {current_app}\nPlease return to studying!"
        
        messagebox.showwarning("Focus Warning", message)
    
    def show_desktop_warning(self, app_summary):
        """NEW: Show desktop-only warning"""
        if not self.monitor_window or not self.monitor_window.winfo_exists():
            return
        
        self.session_warnings += 1
        
        if hasattr(self, 'warning_label'):
            self.warning_label.config(text=f"Warnings: {self.session_warnings}")
        
        current_app = self.activity_monitor.current_app or "Unknown"
        messagebox.showwarning("Study Alert", 
                              f"Distraction detected!\n\nCurrent activity: {app_summary}\nApp: {current_app}\n\nPlease refocus on your studies.")
    
    def update_desktop_monitor(self, score):
        """NEW: Update desktop monitoring display"""
        if not self.monitor_window or not self.monitor_window.winfo_exists():
            return
        
        if hasattr(self, 'focus_score_label'):
            status = "✅ GOOD" if score >= 70 else "⚠️ DISTRACTED" if score >= 40 else "🚨 HIGH DISTRACTION"
            color = self.colors['success'] if score >= 70 else self.colors['warning'] if score >= 40 else self.colors['danger']
            
            self.focus_score_label.config(text=f"Focus: {score:.0f}%", fg=color)
            self.status_label.config(text=status, fg=color)

    def end_session(self, result):
        if self.monitor_window:
            self.monitor_window.destroy()

        if result['success']:
            # Update study hours with detailed tracking
            warnings = result.get('warnings', 0)
            focus_score = result.get('focus_score', 100)
            self.db.update_study_hours(self.current_user, self.hours_var.get(), 
                                      warnings=warnings, focus_score=focus_score)
            
            # Get newly earned badges
            newly_earned = self.db.check_and_award_badges(self.current_user)
            
            # Show detailed completion popup
            self.show_session_complete_popup(result, newly_earned)
        else:
            messagebox.showwarning("Session Incomplete", 
                                  f"Session ended with {result.get('warnings', 0)} warnings. " +
                                  "Time was not fully counted.")

        self.create_main_screen()

    def show_session_complete_popup(self, result, newly_earned_badges):
        """Show detailed session completion with stats and new badges"""
        popup = tk.Toplevel(self.root)
        popup.title("🎉 Session Complete!")
        popup.geometry("500x600")
        popup.configure(bg=self.colors['bg_light'])

        main_frame = tk.Frame(popup, bg=self.colors['bg_card'], 
                             highlightbackground=self.colors['border'], highlightthickness=2)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Success header
        header = tk.Frame(main_frame, bg=self.colors['success'])
        header.pack(fill=tk.X)
        tk.Label(header, text="🎉", font=("Arial", 48), bg=self.colors['success']).pack(pady=10)
        tk.Label(header, text="Study Session Complete!", font=("Segoe UI", 20, "bold"), 
                bg=self.colors['success'], fg="white").pack(pady=(0, 15))

        # Stats container
        stats_frame = tk.Frame(main_frame, bg=self.colors['bg_card'])
        stats_frame.pack(fill=tk.BOTH, expand=True, pady=20, padx=20)

        # Performance stats
        tk.Label(stats_frame, text="📊 Session Performance", font=("Segoe UI", 16, "bold"), 
                bg=self.colors['bg_card'], fg=self.colors['text_primary']).pack(pady=(0, 15))

        stats = [
            ("⏱️ Duration", f"{self.hours_var.get()} hours"),
            ("⚠️ Warnings", str(result.get('warnings', 0))),
            ("🎯 Focus Score", f"{result.get('focus_score', 100)}%"),
            ("✅ Status", "Perfect!" if result.get('warnings', 0) == 0 else "Good" if result.get('warnings', 0) < 3 else "Needs Improvement")
        ]

        for label, value in stats:
            stat_frame = tk.Frame(stats_frame, bg=self.colors['bg_light'])
            stat_frame.pack(fill=tk.X, pady=5)
            tk.Label(stat_frame, text=label, font=("Segoe UI", 12), 
                    bg=self.colors['bg_light'], fg=self.colors['text_secondary']).pack(side=tk.LEFT, padx=10)
            tk.Label(stat_frame, text=value, font=("Segoe UI", 12, "bold"), 
                    bg=self.colors['bg_light'], fg=self.colors['text_primary']).pack(side=tk.RIGHT, padx=10)

        # New badges
        if newly_earned_badges:
            badges_frame = tk.Frame(main_frame, bg=self.colors['bg_card'])
            badges_frame.pack(fill=tk.X, pady=(20, 10), padx=20)
            
            tk.Label(badges_frame, text="🏆 New Badges Earned!", font=("Segoe UI", 16, "bold"), 
                    bg=self.colors['bg_card'], fg=self.colors['primary']).pack(pady=(0, 10))
            
            for badge in newly_earned_badges[:3]:  # Show top 3 new badges
                badge_label = tk.Label(badges_frame, text=badge, font=("Segoe UI", 13, "bold"), 
                                      bg=self.colors['warning'], fg="white", padx=15, pady=8)
                badge_label.pack(pady=5)

        # Close button
        close_btn = tk.Button(main_frame, text="✨ Awesome!", command=popup.destroy,
                             font=("Segoe UI", 14, "bold"), width=20, height=2,
                             bg=self.colors['primary'], fg="white", relief=tk.FLAT, cursor="hand2")
        close_btn.pack(pady=20)
        self.add_hover_effect(close_btn, self.colors['primary'], self.colors['primary_dark'])

    def show_achievement_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title("Achievement Unlocked!")
        popup.geometry("300x150")
        popup.attributes("-topmost", True)

        main_frame = tk.Frame(popup, bg="#FFF3E0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        tk.Label(main_frame, text="🎉 Achievement Unlocked!", font=("Arial", 14, "bold"), bg="#FFF3E0").pack(pady=10)
        tk.Label(main_frame, text="Great study session!", font=("Arial", 12), bg="#FFF3E0").pack(pady=5)

        tk.Button(main_frame, text="Awesome!", command=popup.destroy, bg="#4CAF50", fg="white").pack(pady=10)


    def stop_session(self):
        self.session_running = False
        self.face_detector.stop_camera()
        self.activity_monitor.stop_monitoring()
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=2)
        if self.monitor_window:
            self.monitor_window.destroy()
        self.show_activity_report()
        messagebox.showinfo("Session Stopped", "Session stopped. Check activity report!")
        self.create_main_screen()

    def show_activity_report(self):
        if not self.current_session_id:
            return
        
        report_window = tk.Toplevel(self.root)
        report_window.title("Session Activity Report")
        report_window.geometry("900x600")
        report_window.configure(bg=self.colors['bg_light'])
        
        main_frame = tk.Frame(report_window, bg=self.colors['bg_card'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(main_frame, text="📊 Session Activity Report", 
                font=("Segoe UI", 20, "bold"), bg=self.colors['bg_card']).pack(pady=20)
        
        # Activity log
        activities = self.activity_logger.get_session_activity_log(self.current_user, self.current_session_id)
        
        log_frame = tk.Frame(main_frame, bg=self.colors['bg_card'])
        log_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        tk.Label(log_frame, text="Activity Log:", font=("Segoe UI", 14, "bold"), 
                bg=self.colors['bg_card']).pack(anchor='w', pady=5)
        
        log_text = tk.Text(log_frame, height=15, width=100, font=("Consolas", 9))
        log_text.pack(fill=tk.BOTH, expand=True)
        
        for activity in activities:
            timestamp, activity_type, app_name, window_title, url = activity
            log_text.insert(tk.END, f"[{timestamp}] {activity_type}\n")
            log_text.insert(tk.END, f"  App: {app_name}\n")
            if window_title:
                log_text.insert(tk.END, f"  Window: {window_title}\n")
            if url:
                log_text.insert(tk.END, f"  URL: {url}\n")
            log_text.insert(tk.END, "\n")
        
        log_text.config(state=tk.DISABLED)
        
        # Screenshots
        screenshots = self.activity_logger.get_session_screenshots(self.current_user, self.current_session_id)
        
        tk.Label(main_frame, text=f"📸 Screenshots Captured: {len(screenshots)}", 
                font=("Segoe UI", 12, "bold"), bg=self.colors['bg_card']).pack(pady=10)
        
        tk.Button(main_frame, text="Close", command=report_window.destroy,
                 font=("Segoe UI", 12, "bold"), width=20, height=2,
                 bg=self.colors['primary'], fg="white").pack(pady=10)


    def view_progress(self):
        progress = self.db.get_student_progress(self.current_user)
        progress_window = tk.Toplevel(self.root)
        progress_window.title("Your Progress")
        progress_window.geometry("400x300")

        tk.Label(progress_window, text="Your Study Progress", font=("Arial", 14)).pack(pady=10)

        for key, value in progress.items():
            tk.Label(progress_window, text=f"{key}: {value}").pack()

        tk.Button(progress_window, text="Close", command=progress_window.destroy).pack(pady=10)

    def logout(self):
        self.current_user = None
        self.create_login_screen()

    def draw_progress_circle(self, animated_percentage=None):
        canvas = self.progress_canvas
        canvas.delete("all")

        center_x, center_y = 90, 90
        radius = 70

        # Get progress data
        try:
            progress = self.db.get_student_progress(self.current_user)
            total_hours = progress.get('Total Hours', 0)
        except:
            total_hours = 0
        
        daily_goal = 2  # Assume 2 hours daily goal
        target_percentage = min(total_hours / daily_goal * 100, 100)

        if animated_percentage is None:
            animated_percentage = target_percentage

        # Background circle (light gray)
        canvas.create_oval(center_x - radius, center_y - radius, center_x + radius, center_y + radius, 
                          fill=self.colors['bg_light'], outline=self.colors['border'], width=8)

        # Progress arc
        if animated_percentage > 0:
            angle = animated_percentage / 100 * 360
            if animated_percentage >= 100:
                color = self.colors['success']
            elif animated_percentage >= 50:
                color = self.colors['warning']
            else:
                color = self.colors['danger']
            
            canvas.create_arc(center_x - radius, center_y - radius, center_x + radius, center_y + radius,
                            start=90, extent=-angle, fill="", outline=color, width=8, style=tk.ARC)

        # Center circle
        inner_radius = radius - 20
        canvas.create_oval(center_x - inner_radius, center_y - inner_radius, 
                          center_x + inner_radius, center_y + inner_radius, 
                          fill=self.colors['bg_card'], outline="")

        # Percentage text
        canvas.create_text(center_x, center_y - 10, text=f"{int(animated_percentage)}%", 
                          font=("Segoe UI", 24, "bold"), fill=self.colors['text_primary'])
        
        # Status text
        status = "Complete!" if animated_percentage >= 100 else "In Progress" if animated_percentage >= 50 else "Get Started"
        canvas.create_text(center_x, center_y + 20, text=status, 
                          font=("Segoe UI", 10), fill=self.colors['text_secondary'])

        # Animate if not at target
        if animated_percentage < target_percentage:
            self.animation_id = self.root.after(50, lambda: self.animate_progress(target_percentage, animated_percentage + 2))

    def animate_progress(self, target, current):
        if current >= target:
            self.draw_progress_circle(target)
        else:
            self.draw_progress_circle(current)
            self.animation_id = self.root.after(50, lambda: self.animate_progress(target, current + 2))

    def draw_roadmap(self):
        """Draw enhanced badge roadmap with earned badges"""
        canvas = self.roadmap_canvas
        canvas.delete("all")

        width = canvas.winfo_width()
        if width <= 1:
            width = 700  # Default width

        # Get earned badges
        try:
            earned_badges = self.db.get_earned_badges(self.current_user)
            earned_badge_ids = [b['id'] for b in earned_badges]
        except:
            earned_badge_ids = []

        # Sample badges to display (first 6)
        all_badges = [
            {"id": "first_steps", "name": "First Steps", "emoji": "🎯"},
            {"id": "getting_started", "name": "Getting Started", "emoji": "📚"},
            {"id": "dedicated_learner", "name": "Dedicated Learner", "emoji": "💪"},
            {"id": "study_enthusiast", "name": "Study Enthusiast", "emoji": "⭐"},
            {"id": "knowledge_seeker", "name": "Knowledge Seeker", "emoji": "🔍"},
            {"id": "study_master", "name": "Study Master", "emoji": "🏆"}
        ]

        step_width = width / len(all_badges)
        y_center = 50

        for i, badge in enumerate(all_badges):
            x = i * step_width + step_width / 2
            unlocked = badge["id"] in earned_badge_ids
            
            # Badge circle
            color = self.colors['success'] if unlocked else self.colors['border']
            outline_color = self.colors['primary'] if unlocked else self.colors['border']
            
            oval_id = canvas.create_oval(x-20, y_center-20, x+20, y_center+20, 
                                        fill=color, outline=outline_color, width=3)
            
            # Badge emoji
            emoji_color = "white" if unlocked else self.colors['text_secondary']
            text_id = canvas.create_text(x, y_center, text=badge["emoji"], 
                                         font=("Arial", 16), fill=emoji_color)

            # Make badge clickable
            canvas.tag_bind(oval_id, "<Button-1>", 
                          lambda e, b=badge, u=unlocked: self.show_badge_details_enhanced(b, u))
            canvas.tag_bind(text_id, "<Button-1>", 
                          lambda e, b=badge, u=unlocked: self.show_badge_details_enhanced(b, u))
            
            # Hover effect
            canvas.tag_bind(oval_id, "<Enter>", 
                          lambda e, o=oval_id: canvas.itemconfig(o, width=4))
            canvas.tag_bind(oval_id, "<Leave>", 
                          lambda e, o=oval_id: canvas.itemconfig(o, width=3))

            # Connection line
            if i < len(all_badges) - 1:
                next_x = (i+1) * step_width + step_width / 2
                line_color = self.colors['success'] if unlocked else self.colors['border']
                canvas.create_line(x+20, y_center, next_x-20, y_center, 
                                 fill=line_color, width=3)

    def show_badge_details_enhanced(self, badge, unlocked):
        """Show enhanced badge details with progress info"""
        details_window = tk.Toplevel(self.root)
        details_window.title(f"{badge['name']} Badge")
        details_window.geometry("400x350")
        details_window.configure(bg=self.colors['bg_light'])

        main_frame = tk.Frame(details_window, bg=self.colors['bg_card'], 
                             highlightbackground=self.colors['border'], highlightthickness=2)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Badge display
        badge_frame = tk.Frame(main_frame, bg=self.colors['success'] if unlocked else self.colors['border'])
        badge_frame.pack(pady=20)
        
        tk.Label(badge_frame, text=badge['emoji'], font=("Arial", 48), 
                bg=self.colors['success'] if unlocked else self.colors['border']).pack(padx=40, pady=20)

        # Badge name
        tk.Label(main_frame, text=badge['name'], font=("Segoe UI", 18, "bold"), 
                bg=self.colors['bg_card'], fg=self.colors['text_primary']).pack(pady=10)

        # Status
        if unlocked:
            status_frame = tk.Frame(main_frame, bg=self.colors['success'])
            status_frame.pack(pady=10)
            tk.Label(status_frame, text="✅ Unlocked!", font=("Segoe UI", 14, "bold"), 
                    bg=self.colors['success'], fg="white", padx=20, pady=5).pack()
        else:
            status_frame = tk.Frame(main_frame, bg=self.colors['border'])
            status_frame.pack(pady=10)
            tk.Label(status_frame, text="🔒 Locked", font=("Segoe UI", 14), 
                    bg=self.colors['border'], fg=self.colors['text_secondary'], padx=20, pady=5).pack()

        # Description
        descriptions = {
            "first_steps": "Complete your first study session",
            "getting_started": "Study for 5 total hours",
            "dedicated_learner": "Study for 10 total hours",
            "study_enthusiast": "Study for 25 total hours",
            "knowledge_seeker": "Study for 50 total hours",
            "study_master": "Study for 100 total hours"
        }
        
        desc = descriptions.get(badge['id'], "Keep studying to unlock!")
        tk.Label(main_frame, text=desc, font=("Segoe UI", 12), 
                bg=self.colors['bg_card'], fg=self.colors['text_secondary'], 
                wraplength=320).pack(pady=15, padx=20)

        # Close button
        close_btn = tk.Button(main_frame, text="Close", command=details_window.destroy,
                             font=("Segoe UI", 12, "bold"), width=15, height=2,
                             bg=self.colors['primary'], fg="white", relief=tk.FLAT, cursor="hand2")
        close_btn.pack(pady=15)
        self.add_hover_effect(close_btn, self.colors['primary'], self.colors['primary_dark'])

    def show_badge_details(self, badge):
        details_window = tk.Toplevel(self.root)
        details_window.title(f"{badge['name']} Badge")
        details_window.geometry("300x200")

        main_frame = tk.Frame(details_window, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        tk.Label(main_frame, text=f"🏆 {badge['name']}", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)
        tk.Label(main_frame, text=badge['description'], font=("Arial", 12), bg="#f0f0f0", wraplength=250).pack(pady=10)

        status_text = "Unlocked!" if badge['unlocked'] else "Locked"
        status_color = "#4CAF50" if badge['unlocked'] else "#F44336"
        tk.Label(main_frame, text=status_text, font=("Arial", 14, "bold"), fg=status_color, bg="#f0f0f0").pack(pady=10)

        button_style = {"font": ("Arial", 12), "width": 15, "height": 1, "bg": "#4CAF50", "fg": "white", "relief": tk.RAISED}
        tk.Button(main_frame, text="Close", command=details_window.destroy, **button_style).pack(pady=10)

    def show_daily_tasks(self):
        tasks_window = tk.Toplevel(self.root)
        tasks_window.title("Today's Tasks")
        tasks_window.geometry("400x300")

        main_frame = tk.Frame(tasks_window, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        tk.Label(main_frame, text="Today's Study Goals", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=20)

        tasks = [
            "Study for 2 hours",
            "Complete math exercises",
            "Review notes"
        ]

        for task in tasks:
            task_frame = tk.Frame(main_frame, bg="#f0f0f0")
            task_frame.pack(fill=tk.X, pady=5)
            tk.Label(task_frame, text="☐", font=("Arial", 14), bg="#f0f0f0").pack(side=tk.LEFT)
            tk.Label(task_frame, text=task, font=("Arial", 12), bg="#f0f0f0").pack(side=tk.LEFT, padx=10)

        button_style = {"font": ("Arial", 12), "width": 15, "height": 1, "bg": "#4CAF50", "fg": "white", "relief": tk.RAISED}
        tk.Button(main_frame, text="Close", command=tasks_window.destroy, **button_style).pack(pady=20)

    def get_study_streak(self):
        # Get real streak from database
        try:
            progress = self.db.get_student_progress(self.current_user)
            return progress.get('Current Streak', 0)
        except:
            return 0

    def get_weekly_hours(self):
        # Get real weekly study hours from database
        try:
            import sqlite3
            from datetime import datetime, timedelta

            conn = sqlite3.connect(self.db.db_name)
            c = conn.cursor()

            today = datetime.now().date()
            week_start = today - timedelta(days=today.weekday())  # Monday of current week

            weekly_hours = []
            for i in range(7):
                day = week_start + timedelta(days=i)
                c.execute("SELECT SUM(hours) FROM study_sessions WHERE username = ? AND date = ? AND completed = 1",
                          (self.current_user, day.strftime('%Y-%m-%d')))
                result = c.fetchone()[0]
                weekly_hours.append(result if result else 0.0)

            conn.close()
            return weekly_hours
        except Exception as e:
            print(f"Error getting weekly hours: {e}")
            return [0.0] * 7

    def get_random_quote(self):
        quotes = [
            "The only way to do great work is to love what you do. – Steve Jobs",
            "Believe you can and you're halfway there. – Theodore Roosevelt",
            "The future belongs to those who believe in the beauty of their dreams. – Eleanor Roosevelt",
            "You miss 100% of the shots you don't take. – Wayne Gretzky",
            "The best way to predict the future is to create it. – Peter Drucker",
            "Success is not final, failure is not fatal: It is the courage to continue that counts. – Winston Churchill"
        ]
        return random.choice(quotes)

    def draw_weekly_chart(self):
        canvas = self.weekly_canvas
        canvas.delete("all")

        width = canvas.winfo_width()
        if width <= 1:
            width = 700

        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        # Get real weekly data from database
        weekly_hours = self.get_weekly_hours()

        step_width = width / len(days)
        max_height = 100
        max_hours = max(weekly_hours) if max(weekly_hours) > 0 else 1

        for i, (day, hours) in enumerate(zip(days, weekly_hours)):
            x = i * step_width + step_width / 2
            bar_height = (hours / max_hours) * max_height if max_hours > 0 else 0
            y_bottom = 120
            y_top = y_bottom - bar_height

            # Color based on progress
            if hours >= 2:
                color = self.colors['success']
            elif hours >= 1:
                color = self.colors['warning']
            else:
                color = self.colors['danger']
            
            # Rounded bar effect
            bar_id = canvas.create_rectangle(x-20, y_top, x+20, y_bottom, 
                                            fill=color, outline="", width=0)
            
            # Day label
            canvas.create_text(x, y_bottom + 15, text=day, 
                              font=("Segoe UI", 10, "bold"), fill=self.colors['text_secondary'])
            
            # Hours label
            if hours > 0:
                canvas.create_text(x, y_top - 15, text=f"{hours:.1f}h", 
                                  font=("Segoe UI", 10, "bold"), fill=self.colors['text_primary'])

            # Hover effect
            canvas.tag_bind(bar_id, "<Enter>", lambda e, b=bar_id: canvas.itemconfig(b, fill=self.colors['primary']))
            canvas.tag_bind(bar_id, "<Leave>", lambda e, b=bar_id, c=color: canvas.itemconfig(b, fill=c))

    def quick_session(self, hours):
        """Quick session with pre-configured settings"""
        self.hours_var = tk.DoubleVar(value=hours)
        self.camera_var = tk.BooleanVar(value=True)
        self.study_detect_var = tk.BooleanVar(value=True)
        
        # Directly start session without confirmation window
        self.begin_session(None)

    def set_goals(self):
        goals_window = tk.Toplevel(self.root)
        goals_window.title("Set Study Goals")
        goals_window.geometry("400x300")

        main_frame = tk.Frame(goals_window, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        tk.Label(main_frame, text="Set Your Daily Study Goal", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=20)

        tk.Label(main_frame, text="Hours per day:", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)
        self.goal_var = tk.DoubleVar(value=2.0)
        goal_spin = tk.Spinbox(main_frame, from_=0.5, to=12, increment=0.5, textvariable=self.goal_var, font=("Arial", 12))
        goal_spin.pack(pady=10)

        tk.Label(main_frame, text="Weekly target (days):", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)
        self.weekly_goal_var = tk.IntVar(value=5)
        weekly_spin = tk.Spinbox(main_frame, from_=1, to=7, textvariable=self.weekly_goal_var, font=("Arial", 12))
        weekly_spin.pack(pady=10)

        button_style = {"font": ("Arial", 12), "width": 15, "height": 1, "bg": "#4CAF50", "fg": "white", "relief": tk.RAISED}
        tk.Button(main_frame, text="Save Goals", command=lambda: self.save_goals(goals_window), **button_style).pack(pady=20)

    def save_goals(self, window):
        daily_goal = self.goal_var.get()
        weekly_goal = self.weekly_goal_var.get()
        # In real implementation, save to database
        messagebox.showinfo("Success", f"Goals saved!\nDaily: {daily_goal}h\nWeekly: {weekly_goal} days")
        window.destroy()

    def start_monitoring_now(self):
        """Start monitoring immediately without specifying hours"""
        self.hours_var = tk.DoubleVar(value=1)  # Default to 1 hour
        self.begin_session(None)  # Pass None since no window to destroy

    def start_study_challenge(self):
        """Start a study challenge with a fixed duration"""
        challenge_window = tk.Toplevel(self.root)
        challenge_window.title("Study Challenge")
        challenge_window.geometry("400x300")

        main_frame = tk.Frame(challenge_window, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        tk.Label(main_frame, text="Choose Your Study Challenge!", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=20)

        challenge_options = [
            ("30-Minute Sprint", 0.5),
            ("1-Hour Deep Focus", 1),
            ("2-Hour Marathon", 2)
        ]

        button_style = {"font": ("Arial", 12), "width": 20, "height": 2, "bg": "#9C27B0", "fg": "white", "relief": tk.RAISED}

        for challenge_name, hours in challenge_options:
            tk.Button(main_frame, text=challenge_name, command=lambda h=hours, w=challenge_window: self.begin_challenge(h, w), **button_style).pack(pady=10)

    def begin_challenge(self, hours, window):
        """Begin a study challenge with full monitoring"""
        self.hours_var = tk.DoubleVar(value=hours)
        self.camera_var = tk.BooleanVar(value=True)
        self.study_detect_var = tk.BooleanVar(value=True)
        window.destroy()
        
        # Create a placeholder window for begin_session
        placeholder = tk.Toplevel(self.root)
        placeholder.withdraw()  # Hide it
        self.begin_session(placeholder)

    def upload_photo(self):
        from tkinter import filedialog
        file_path = filedialog.askopenfilename(
            title="Select Profile Photo",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")]
        )
        if file_path:
            # In a real implementation, you would save the photo to the database or file system
            messagebox.showinfo("Success", "Profile photo uploaded successfully!")
    
    def upload_profile_photo(self):
        """Upload and save profile photo"""
        file_path = filedialog.askopenfilename(
            title="Select Profile Photo",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                # Create a unique filename
                ext = os.path.splitext(file_path)[1]
                new_filename = f"{self.current_user}_profile{ext}"
                save_path = os.path.join('profile_photos', new_filename)
                
                # Copy and resize the image
                img = Image.open(file_path)
                
                # Resize to square (100x100) for profile photo
                img = img.resize((100, 100), Image.Resampling.LANCZOS)
                
                # Save the resized image
                img.save(save_path)
                
                # Update database
                self.db.update_profile_photo(self.current_user, save_path)
                
                # Reload profile photo in sidebar
                self.load_profile_photo()
                
                # Reload profile avatar in profile tab if it exists
                try:
                    self.load_profile_avatar()
                except:
                    pass  # Profile tab might not be created yet
                
                messagebox.showinfo("Success", "Profile photo updated successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to upload photo: {str(e)}")
    
    def load_profile_photo(self):
        """Load and display profile photo"""
        try:
            photo_path = self.db.get_profile_photo(self.current_user)
            
            if photo_path and os.path.exists(photo_path):
                # Load image
                img = Image.open(photo_path)
                img = img.resize((100, 100), Image.Resampling.LANCZOS)
                
                # Create circular mask
                mask = Image.new('L', (100, 100), 0)
                from PIL import ImageDraw
                draw = ImageDraw.Draw(mask)
                draw.ellipse((0, 0, 100, 100), fill=255)
                
                # Apply mask for circular effect
                output = Image.new('RGBA', (100, 100), (0, 0, 0, 0))
                output.paste(img, (0, 0))
                output.putalpha(mask)
                
                # Convert to PhotoImage
                self.profile_photo_image = ImageTk.PhotoImage(output)
                self.profile_photo_label.config(image=self.profile_photo_image)
            else:
                # Show default emoji if no photo
                self.profile_photo_label.config(image="", text="👤", font=("Arial", 60))
        except Exception as e:
            print(f"Error loading profile photo: {e}")
            # Show default emoji on error
            self.profile_photo_label.config(image="", text="👤", font=("Arial", 60))
    
    def load_profile_avatar(self):
        """Load and display profile photo in profile tab (larger version)"""
        try:
            photo_path = self.db.get_profile_photo(self.current_user)
            
            if photo_path and os.path.exists(photo_path):
                # Load image
                img = Image.open(photo_path)
                img = img.resize((120, 120), Image.Resampling.LANCZOS)
                
                # Create circular mask
                mask = Image.new('L', (120, 120), 0)
                from PIL import ImageDraw
                draw = ImageDraw.Draw(mask)
                draw.ellipse((0, 0, 120, 120), fill=255)
                
                # Apply mask for circular effect
                output = Image.new('RGBA', (120, 120), (0, 0, 0, 0))
                output.paste(img, (0, 0))
                output.putalpha(mask)
                
                # Convert to PhotoImage
                photo_image = ImageTk.PhotoImage(output)
                self.profile_avatar_label.config(image=photo_image)
                self.profile_avatar_label.image = photo_image  # Keep reference
            else:
                # Show default emoji if no photo
                self.profile_avatar_label.config(image="", text="👤", font=("Arial", 60))
        except Exception as e:
            print(f"Error loading profile avatar: {e}")
            # Show default emoji on error
            self.profile_avatar_label.config(image="", text="👤", font=("Arial", 60))

    def add_hover_effect(self, button, normal_color, hover_color):
        """Add hover effect to buttons"""
        def on_enter(e):
            button.config(bg=hover_color)
        def on_leave(e):
            button.config(bg=normal_color)
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentApp(root)
    root.mainloop()
