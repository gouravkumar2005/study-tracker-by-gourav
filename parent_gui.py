import tkinter as tk
from tkinter import messagebox, ttk
from database import Database
import time
import random
import datetime
import threading

class ParentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("👪 Study Tracker - Parent Dashboard")
        self.root.geometry("900x700")

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
        self.current_user = None
        self.clock_label = None
        self.notification_thread = None
        self.stop_notifications = False

        self.create_login_screen()

    def create_login_screen(self):
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
        
        tk.Label(header_frame, text="👪", font=("Arial", 48), bg=self.colors['bg_card']).pack()
        tk.Label(header_frame, text="Parent Login", font=("Segoe UI", 24, "bold"), 
                bg=self.colors['bg_card'], fg=self.colors['text_primary']).pack(pady=(10, 5))
        tk.Label(header_frame, text="Monitor and support your child's learning journey", 
                font=("Segoe UI", 10), bg=self.colors['bg_card'], fg=self.colors['text_secondary']).pack()

        # Form
        form_frame = tk.Frame(card_frame, bg=self.colors['bg_card'])
        form_frame.pack(pady=30, padx=40)

        tk.Label(form_frame, text="Username", font=("Segoe UI", 11, "bold"), 
                bg=self.colors['bg_card'], fg=self.colors['text_primary']).grid(row=0, column=0, sticky="w", pady=(0, 5))
        self.username_entry = tk.Entry(form_frame, font=("Segoe UI", 12), width=30, 
                                      relief=tk.FLAT, highlightbackground=self.colors['border'], 
                                      highlightthickness=2, bd=8)
        self.username_entry.grid(row=1, column=0, pady=(0, 20))

        tk.Label(form_frame, text="Password", font=("Segoe UI", 11, "bold"), 
                bg=self.colors['bg_card'], fg=self.colors['text_primary']).grid(row=2, column=0, sticky="w", pady=(0, 5))
        self.password_entry = tk.Entry(form_frame, show="●", font=("Segoe UI", 12), width=30, 
                                      relief=tk.FLAT, highlightbackground=self.colors['border'], 
                                      highlightthickness=2, bd=8)
        self.password_entry.grid(row=3, column=0, pady=(0, 10))

        # Buttons
        button_frame = tk.Frame(card_frame, bg=self.colors['bg_card'])
        button_frame.pack(pady=(10, 30), padx=40)

        login_btn = tk.Button(button_frame, text="Login", command=self.login,
                            font=("Segoe UI", 12, "bold"), width=28, height=2,
                            bg=self.colors['primary'], fg="white", relief=tk.FLAT,
                            cursor="hand2", activebackground=self.colors['primary_dark'])
        login_btn.pack(pady=5)
        self.add_hover_effect(login_btn, self.colors['primary'], self.colors['primary_dark'])

        register_btn = tk.Button(button_frame, text="Create Account", command=self.create_register_screen,
                               font=("Segoe UI", 11), width=28, height=2,
                               bg=self.colors['bg_light'], fg=self.colors['text_primary'], 
                               relief=tk.FLAT, cursor="hand2")
        register_btn.pack(pady=5)
        self.add_hover_effect(register_btn, self.colors['bg_light'], self.colors['border'])

    def create_register_screen(self):
        self.clear_screen()

        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        tk.Label(main_frame, text="Parent Register", font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=30)

        form_frame = tk.Frame(main_frame, bg="#f0f0f0")
        form_frame.pack(pady=20)

        tk.Label(form_frame, text="Username:", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=0, sticky="e", padx=10, pady=5)
        self.reg_username_entry = tk.Entry(form_frame, font=("Arial", 12))
        self.reg_username_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Password:", font=("Arial", 12), bg="#f0f0f0").grid(row=1, column=0, sticky="e", padx=10, pady=5)
        self.reg_password_entry = tk.Entry(form_frame, show="*", font=("Arial", 12))
        self.reg_password_entry.grid(row=1, column=1, padx=10, pady=5)

        button_frame = tk.Frame(main_frame, bg="#f0f0f0")
        button_frame.pack(pady=20)

        button_style = {"font": ("Arial", 12), "width": 15, "height": 1, "bg": "#4CAF50", "fg": "white", "relief": tk.RAISED}

        tk.Button(button_frame, text="Register", command=self.register, **button_style).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="Back to Login", command=self.create_login_screen, **button_style).grid(row=0, column=1, padx=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Show loading indicator
        loading_frame = self.show_loading_indicator(self.root, "Logging in...")
        self.root.update()

        # Simulate authentication delay for better UX
        self.root.after(1000, lambda: self.complete_login(username, password, loading_frame))

    def complete_login(self, username, password, loading_frame):
        """Complete the login process after loading delay"""
        loading_frame.destroy()

        if self.db.authenticate_user(username, password, 'parent'):
            self.current_user = username
            self.create_main_screen()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def register(self):
        username = self.reg_username_entry.get()
        password = self.reg_password_entry.get()

        if self.db.register_user(username, password, 'parent'):
            messagebox.showinfo("Success", "Registration successful")
            self.create_login_screen()
        else:
            messagebox.showerror("Error", "Username already exists")

    def create_main_screen(self):
        self.clear_screen()

        main_frame = tk.Frame(self.root, bg=self.colors['bg_light'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header Card
        header_card = tk.Frame(main_frame, bg=self.colors['bg_card'], 
                              highlightbackground=self.colors['border'], highlightthickness=1)
        header_card.pack(fill=tk.X, pady=(0, 20))

        header_container = tk.Frame(header_card, bg=self.colors['bg_card'])
        header_container.pack(fill=tk.X, padx=25, pady=20)

        # Left side - Welcome
        left_frame = tk.Frame(header_container, bg=self.colors['bg_card'])
        left_frame.pack(side=tk.LEFT)
        
        tk.Label(left_frame, text=f"Welcome, {self.current_user}! 👋", 
                font=("Segoe UI", 22, "bold"), bg=self.colors['bg_card'], 
                fg=self.colors['text_primary']).pack(anchor="w")
        tk.Label(left_frame, text="Monitor your children's learning progress", 
                font=("Segoe UI", 11), bg=self.colors['bg_card'], 
                fg=self.colors['text_secondary']).pack(anchor="w", pady=(5, 0))

        # Right side - Stats
        right_frame = tk.Frame(header_container, bg=self.colors['bg_card'])
        right_frame.pack(side=tk.RIGHT)

        students = self.db.get_students_for_parent(self.current_user)
        
        stats_container = tk.Frame(right_frame, bg=self.colors['primary'], 
                                  highlightbackground=self.colors['primary'], highlightthickness=2)
        stats_container.pack(side=tk.LEFT, padx=10)
        self.family_stats_label = tk.Label(stats_container, text=f"👨‍👩‍👧‍👦 {len(students)} Children", 
                                           font=("Segoe UI", 12, "bold"), bg=self.colors['primary'], 
                                           fg="white", padx=15, pady=8)
        self.family_stats_label.pack()

        clock_container = tk.Frame(right_frame, bg=self.colors['success'], 
                                  highlightbackground=self.colors['success'], highlightthickness=2)
        clock_container.pack(side=tk.LEFT)
        self.clock_label = tk.Label(clock_container, text="", font=("Segoe UI", 12, "bold"), 
                                    bg=self.colors['success'], fg="white", padx=15, pady=8)
        self.clock_label.pack()
        self.update_clock()

        # Start notification thread
        self.start_notifications()

        # Parent Tip Card
        tip_card = tk.Frame(main_frame, bg=self.colors['success_light'], 
                           highlightbackground=self.colors['success'], highlightthickness=2)
        tip_card.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(tip_card, text="💡", font=("Arial", 24), bg=self.colors['success_light']).pack(pady=(15, 5))
        self.tip_label = tk.Label(tip_card, text=self.get_random_parent_tip(), 
                                  font=("Segoe UI", 12, "italic"), bg=self.colors['success_light'], 
                                  fg=self.colors['text_primary'], wraplength=700)
        self.tip_label.pack(pady=(0, 15), padx=20)

        # Family Progress Summary Card
        summary_card = tk.Frame(main_frame, bg=self.colors['bg_card'], 
                               highlightbackground=self.colors['border'], highlightthickness=1)
        summary_card.pack(pady=(0, 20), fill=tk.X)

        tk.Label(summary_card, text="📊 Family Study Summary", font=("Segoe UI", 16, "bold"), 
                bg=self.colors['bg_card'], fg=self.colors['text_primary']).pack(pady=(20, 15), padx=20, anchor="w")

        self.summary_canvas = tk.Canvas(summary_card, height=100, bg=self.colors['bg_card'], highlightthickness=0)
        self.summary_canvas.pack(fill=tk.X, padx=30, pady=(0, 20))
        self.draw_family_summary()

        # Stats Overview Card
        stats_card = tk.Frame(main_frame, bg=self.colors['bg_card'], 
                             highlightbackground=self.colors['border'], highlightthickness=1)
        stats_card.pack(pady=(0, 20), fill=tk.X)

        tk.Label(stats_card, text="👥 Individual Student Progress", font=("Segoe UI", 16, "bold"), 
                bg=self.colors['bg_card'], fg=self.colors['text_primary']).pack(pady=(20, 15), padx=20, anchor="w")

        self.stats_canvas = tk.Canvas(stats_card, height=120, bg=self.colors['bg_card'], highlightthickness=0)
        self.stats_canvas.pack(fill=tk.X, padx=30, pady=(0, 20))
        self.stats_canvas.bind("<Configure>", lambda e: self.draw_stats_overview())

        # Quick Actions Card
        actions_card = tk.Frame(main_frame, bg=self.colors['bg_card'], 
                               highlightbackground=self.colors['border'], highlightthickness=1)
        actions_card.pack(pady=(0, 20), fill=tk.X)

        tk.Label(actions_card, text="⚡ Quick Actions", font=("Segoe UI", 16, "bold"), 
                bg=self.colors['bg_card'], fg=self.colors['text_primary']).pack(pady=(20, 15), padx=20, anchor="w")

        quick_buttons_frame = tk.Frame(actions_card, bg=self.colors['bg_card'])
        quick_buttons_frame.pack(pady=(0, 20), padx=20)

        refresh_btn = tk.Button(quick_buttons_frame, text="🔄 Refresh Data", command=self.refresh_data,
                               font=("Segoe UI", 11, "bold"), width=18, height=2,
                               bg=self.colors['primary'], fg="white", relief=tk.FLAT, cursor="hand2")
        refresh_btn.grid(row=0, column=0, padx=10, pady=5)
        self.add_hover_effect(refresh_btn, self.colors['primary'], self.colors['primary_dark'])

        goals_btn = tk.Button(quick_buttons_frame, text="🎯 Set Family Goals", command=self.set_family_goals,
                             font=("Segoe UI", 11, "bold"), width=18, height=2,
                             bg=self.colors['secondary'], fg="white", relief=tk.FLAT, cursor="hand2")
        goals_btn.grid(row=0, column=1, padx=10, pady=5)
        self.add_hover_effect(goals_btn, self.colors['secondary'], '#7C3AED')

        encourage_btn = tk.Button(quick_buttons_frame, text="💌 Send Encouragement", command=self.send_encouragement,
                                 font=("Segoe UI", 11, "bold"), width=18, height=2,
                                 bg=self.colors['success'], fg="white", relief=tk.FLAT, cursor="hand2")
        encourage_btn.grid(row=0, column=2, padx=10, pady=5)
        self.add_hover_effect(encourage_btn, self.colors['success'], '#059669')

        # Student Selection and Actions Card
        selection_card = tk.Frame(main_frame, bg=self.colors['bg_card'], 
                                 highlightbackground=self.colors['border'], highlightthickness=1)
        selection_card.pack(fill=tk.X)

        tk.Label(selection_card, text="📋 Student Management", font=("Segoe UI", 16, "bold"), 
                bg=self.colors['bg_card'], fg=self.colors['text_primary']).pack(pady=(20, 15), padx=20, anchor="w")

        # Student selector
        selector_frame = tk.Frame(selection_card, bg=self.colors['bg_card'])
        selector_frame.pack(pady=(0, 15), padx=20, fill=tk.X)

        tk.Label(selector_frame, text="Select Student:", font=("Segoe UI", 12, "bold"), 
                bg=self.colors['bg_card'], fg=self.colors['text_primary']).pack(side=tk.LEFT, padx=(0, 15))
        
        self.student_var = tk.StringVar()
        student_combo = ttk.Combobox(selector_frame, textvariable=self.student_var, 
                                     values=students, font=("Segoe UI", 11), width=25, state="readonly")
        student_combo.pack(side=tk.LEFT)

        # Action buttons
        button_frame = tk.Frame(selection_card, bg=self.colors['bg_card'])
        button_frame.pack(pady=(0, 20), padx=20)

        report_btn = tk.Button(button_frame, text="📊 View Student Report", command=self.view_report,
                              font=("Segoe UI", 12, "bold"), width=25, height=2,
                              bg=self.colors['primary'], fg="white", relief=tk.FLAT, cursor="hand2")
        report_btn.grid(row=0, column=0, padx=5, pady=5)
        self.add_hover_effect(report_btn, self.colors['primary'], self.colors['primary_dark'])

        compare_btn = tk.Button(button_frame, text="⚖️ Compare Students", command=self.compare_students,
                               font=("Segoe UI", 12, "bold"), width=25, height=2,
                               bg=self.colors['secondary'], fg="white", relief=tk.FLAT, cursor="hand2")
        compare_btn.grid(row=0, column=1, padx=5, pady=5)
        self.add_hover_effect(compare_btn, self.colors['secondary'], '#7C3AED')

        logout_btn = tk.Button(button_frame, text="🚪 Logout", command=self.logout,
                              font=("Segoe UI", 12, "bold"), width=25, height=2,
                              bg=self.colors['danger'], fg="white", relief=tk.FLAT, cursor="hand2")
        logout_btn.grid(row=0, column=2, padx=5, pady=5)
        self.add_hover_effect(logout_btn, self.colors['danger'], '#DC2626')

    def draw_stats_overview(self):
        canvas = self.stats_canvas
        canvas.delete("all")

        width = canvas.winfo_width()
        if width <= 1:
            width = 400  # Default width

        students = self.db.get_students_for_parent(self.current_user)
        if not students:
            canvas.create_text(width/2, 50, text="No students registered yet", font=("Arial", 12), fill="#666")
            return

        step_width = width / len(students)
        y_center = 50

        for i, student in enumerate(students):
            x = i * step_width + step_width / 2
            progress = self.db.get_student_progress(student)
            total_hours = progress.get('total_study_hours', 0)
            color = "#4CAF50" if total_hours >= 10 else "#FFC107" if total_hours >= 5 else "#F44336"

            # Create animated circle with pulsing effect
            oval_id = canvas.create_oval(x-20, y_center-20, x+20, y_center+20, fill=color, outline="")
            canvas.create_text(x, y_center, text=f"{student}\n{total_hours}h", font=("Arial", 10, "bold"), fill="white")

            # Make student circles clickable with enhanced interaction
            canvas.tag_bind(oval_id, "<Button-1>", lambda e, s=student: self.quick_view_student(s))
            canvas.tag_bind(oval_id, "<Enter>", lambda e, o=oval_id: self.animate_student_circle(o, color, "enter"))
            canvas.tag_bind(oval_id, "<Leave>", lambda e, o=oval_id: self.animate_student_circle(o, color, "leave"))

            # Add progress indicator ring around each student
            self.draw_progress_ring(canvas, x, y_center, total_hours, 25)

    def view_report(self):
        student = self.student_var.get()
        if not student:
            messagebox.showerror("Error", "Please select a student")
            return

        report = self.db.get_student_report(student)
        report_window = tk.Toplevel(self.root)
        report_window.title(f"Report for {student}")
        report_window.geometry("500x400")

        main_frame = tk.Frame(report_window, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        tk.Label(main_frame, text=f"📊 Detailed Report for {student}", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=20)

        # Progress bar for study hours
        progress_frame = tk.Frame(main_frame, bg="#f0f0f0")
        progress_frame.pack(pady=10)

        total_hours = report.get('total_study_hours', 0)
        goal = 20  # Weekly goal
        progress_percentage = min(total_hours / goal * 100, 100)

        tk.Label(progress_frame, text=f"Study Hours Progress: {total_hours}/{goal} hours", font=("Arial", 12), bg="#f0f0f0").pack()
        progress_bar = ttk.Progressbar(progress_frame, orient="horizontal", length=300, mode="determinate", value=progress_percentage)
        progress_bar.pack(pady=5)

        report_frame = tk.Frame(main_frame, bg="#f0f0f0")
        report_frame.pack(pady=20)

        for key, value in report.items():
            tk.Label(report_frame, text=f"{key}: {value}", font=("Arial", 12), bg="#f0f0f0").pack(anchor="w", padx=10, pady=5)

        button_style = {"font": ("Arial", 12), "width": 15, "height": 1, "bg": "#4CAF50", "fg": "white", "relief": tk.RAISED}
        tk.Button(main_frame, text="Close", command=report_window.destroy, **button_style).pack(pady=20)

    def quick_view_student(self, student):
        # Set the student in the dropdown and view report
        self.student_var.set(student)
        self.view_report()

    def logout(self):
        self.current_user = None
        self.create_login_screen()

    def get_random_parent_tip(self):
        tips = [
            "Praise effort over results to build confidence and resilience.",
            "Set achievable goals and celebrate small victories together.",
            "Create a distraction-free study space to improve focus.",
            "Encourage breaks and healthy habits during study sessions.",
            "Discuss what your child learned, not just grades or scores.",
            "Model good study habits by reading or learning something new yourself."
        ]
        return random.choice(tips)

    def draw_family_summary(self):
        canvas = self.summary_canvas
        canvas.delete("all")

        width = canvas.winfo_width()
        if width <= 1:
            width = 400

        students = self.db.get_students_for_parent(self.current_user)
        if not students:
            canvas.create_text(width/2, 40, text="No students registered yet", font=("Arial", 12), fill="#666")
            return

        total_hours = sum(self.db.get_student_progress(s).get('total_study_hours', 0) for s in students)
        avg_hours = total_hours / len(students) if students else 0

        # Draw total hours bar with animation
        bar_width = min(total_hours / 50 * width, width)  # Assume 50 hours max expected weekly
        total_bar_id = canvas.create_rectangle(0, 10, bar_width, 30, fill="#4CAF50", outline="")
        canvas.create_rectangle(0, 10, width, 30, outline="#ccc", width=2)
        canvas.create_text(width/2, 20, text=f"Total Family Hours: {total_hours:.1f}h", font=("Arial", 10, "bold"))

        # Draw average hours bar with animation
        avg_bar_width = min(avg_hours / 10 * width, width)  # Assume 10 hours max per child
        avg_bar_id = canvas.create_rectangle(0, 40, avg_bar_width, 60, fill="#2196F3", outline="")
        canvas.create_rectangle(0, 40, width, 60, outline="#ccc", width=2)
        canvas.create_text(width/2, 50, text=f"Average per Child: {avg_hours:.1f}h", font=("Arial", 10, "bold"))

        # Add achievement indicators
        self.add_achievement_indicators(canvas, total_hours, avg_hours, width)

        # Add hover effects to bars
        canvas.tag_bind(total_bar_id, "<Enter>", lambda e: self.animate_bar(canvas, total_bar_id, "#4CAF50", "#66BB6A"))
        canvas.tag_bind(total_bar_id, "<Leave>", lambda e: self.animate_bar(canvas, total_bar_id, "#66BB6A", "#4CAF50"))
        canvas.tag_bind(avg_bar_id, "<Enter>", lambda e: self.animate_bar(canvas, avg_bar_id, "#2196F3", "#42A5F5"))
        canvas.tag_bind(avg_bar_id, "<Leave>", lambda e: self.animate_bar(canvas, avg_bar_id, "#42A5F5", "#2196F3"))

    def refresh_data(self):
        # Refresh all data displays
        self.draw_stats_overview()
        self.draw_family_summary()
        students = self.db.get_students_for_parent(self.current_user)
        self.family_stats_label.config(text=f"👨‍👩‍👧‍👦 {len(students)} Children")
        messagebox.showinfo("Refreshed", "📊 Data refreshed successfully!")

    def set_family_goals(self):
        goals_window = tk.Toplevel(self.root)
        goals_window.title("Set Family Study Goals")
        goals_window.geometry("400x300")

        main_frame = tk.Frame(goals_window, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        tk.Label(main_frame, text="Set Family Study Goals", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=20)

        tk.Label(main_frame, text="Weekly study hours goal:", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)
        self.family_weekly_goal_var = tk.DoubleVar(value=50.0)
        weekly_spin = tk.Spinbox(main_frame, from_=10, to=200, increment=5, textvariable=self.family_weekly_goal_var, font=("Arial", 12))
        weekly_spin.pack(pady=10)

        tk.Label(main_frame, text="Daily screen time limit (hours):", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)
        self.screen_time_limit_var = tk.DoubleVar(value=2.0)
        screen_spin = tk.Spinbox(main_frame, from_=0.5, to=8, increment=0.5, textvariable=self.screen_time_limit_var, font=("Arial", 12))
        screen_spin.pack(pady=10)

        button_style = {"font": ("Arial", 12), "width": 15, "height": 1, "bg": "#4CAF50", "fg": "white", "relief": tk.RAISED}
        tk.Button(main_frame, text="Save Goals", command=lambda: self.save_family_goals(goals_window), **button_style).pack(pady=20)

    def save_family_goals(self, window):
        weekly_goal = self.family_weekly_goal_var.get()
        screen_limit = self.screen_time_limit_var.get()
        # In real implementation, save to database
        messagebox.showinfo("Success", f"Family goals saved!\nWeekly: {weekly_goal}h\nScreen limit: {screen_limit}h per day")
        window.destroy()

    def send_encouragement(self):
        students = self.db.get_students_for_parent(self.current_user)
        if not students:
            messagebox.showwarning("No Students", "No students registered to send encouragement to.")
            return

        encouragement_window = tk.Toplevel(self.root)
        encouragement_window.title("Send Encouragement")
        encouragement_window.geometry("400x250")

        main_frame = tk.Frame(encouragement_window, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        tk.Label(main_frame, text="Send Encouragement to Students", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=20)

        tk.Label(main_frame, text="Select student:", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)
        self.encourage_student_var = tk.StringVar()
        student_combo = tk.OptionMenu(main_frame, self.encourage_student_var, *students)
        student_combo.config(font=("Arial", 12))
        student_combo.pack(pady=10)

        tk.Label(main_frame, text="Message:", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)
        self.encouragement_text = tk.Text(main_frame, height=3, width=40, font=("Arial", 10))
        self.encouragement_text.pack(pady=10)
        self.encouragement_text.insert(tk.END, "Great job on your studies! Keep up the excellent work! 🌟")

        button_style = {"font": ("Arial", 12), "width": 15, "height": 1, "bg": "#4CAF50", "fg": "white", "relief": tk.RAISED}
        tk.Button(main_frame, text="Send", command=lambda: self.send_encouragement_message(encouragement_window), **button_style).pack(pady=10)

    def send_encouragement_message(self, window):
        student = self.encourage_student_var.get()
        message = self.encouragement_text.get("1.0", tk.END).strip()
        if not student:
            messagebox.showerror("Error", "Please select a student")
            return
        if not message:
            messagebox.showerror("Error", "Please enter a message")
            return
        # In real implementation, this would send a notification or email
        messagebox.showinfo("Sent", f"Encouragement sent to {student}!\n\n\"{message}\"")
        window.destroy()

    def compare_students(self):
        students = self.db.get_students_for_parent(self.current_user)
        if len(students) < 2:
            messagebox.showwarning("Not Enough Students", "Need at least 2 students to compare progress.")
            return

        compare_window = tk.Toplevel(self.root)
        compare_window.title("Compare Student Progress")
        compare_window.geometry("600x400")

        main_frame = tk.Frame(compare_window, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        tk.Label(main_frame, text="📊 Student Progress Comparison", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=20)

        # Create comparison table
        tree = ttk.Treeview(main_frame, columns=("Student", "Total Hours", "Sessions", "Avg Session", "Badges"), show="headings", height=10)
        tree.heading("Student", text="Student")
        tree.heading("Total Hours", text="Total Hours")
        tree.heading("Sessions", text="Sessions")
        tree.heading("Avg Session", text="Avg Session (h)")
        tree.heading("Badges", text="Badges")

        tree.column("Student", width=100)
        tree.column("Total Hours", width=100)
        tree.column("Sessions", width=80)
        tree.column("Avg Session", width=120)
        tree.column("Badges", width=80)

        for student in students:
            progress = self.db.get_student_progress(student)
            total_hours = progress.get('total_study_hours', 0)
            sessions = progress.get('total_sessions', 0)
            avg_session = total_hours / sessions if sessions > 0 else 0
            badges = progress.get('badges_earned', 0)

            tree.insert("", tk.END, values=(student, f"{total_hours:.1f}", sessions, f"{avg_session:.1f}", badges))

        tree.pack(pady=20, fill=tk.X)

        button_style = {"font": ("Arial", 12), "width": 15, "height": 1, "bg": "#4CAF50", "fg": "white", "relief": tk.RAISED}
        tk.Button(main_frame, text="Close", command=compare_window.destroy, **button_style).pack(pady=10)

    def fade_in(self, widget, alpha=0.0):
        """Fade in animation for widgets"""
        if alpha < 1.0:
            try:
                # Try to set alpha if supported
                widget.attributes("-alpha", alpha)
            except:
                pass  # Alpha not supported on this platform
            alpha += 0.1
            self.root.after(50, lambda: self.fade_in(widget, alpha))

    def add_hover_effect(self, button, normal_color, hover_color):
        """Add hover effect to a button"""
        def on_enter(e):
            button.config(bg=hover_color)
        def on_leave(e):
            button.config(bg=normal_color)
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    def add_tooltips(self):
        """Add tooltips to interactive elements"""
        # This would require a tooltip class, but for simplicity we'll use simple hover effects
        pass

    def show_loading_indicator(self, parent, text="Loading..."):
        """Show a loading indicator"""
        loading_frame = tk.Frame(parent, bg="#f0f0f0")
        loading_frame.pack(pady=20)

        tk.Label(loading_frame, text="⏳", font=("Arial", 24), bg="#f0f0f0").pack()
        tk.Label(loading_frame, text=text, font=("Arial", 12), bg="#f0f0f0").pack()

        return loading_frame

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def update_clock(self):
        """Update the clock label every second"""
        if self.clock_label:
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            self.clock_label.config(text=current_time)
            self.root.after(1000, self.update_clock)

    def start_notifications(self):
        """Start the notification thread"""
        self.stop_notifications = False
        self.notification_thread = threading.Thread(target=self.check_notifications, daemon=True)
        self.notification_thread.start()

    def check_notifications(self):
        """Check for notifications in a loop"""
        while not self.stop_notifications:
            time.sleep(30)  # Check every 30 seconds
            if not self.stop_notifications:
                self.root.after(0, self.show_random_notification)

    def show_random_notification(self):
        """Show a random encouraging notification"""
        notifications = [
            "🌟 Great job keeping up with studies!",
            "📚 Remember to take breaks and stay hydrated!",
            "🎯 Your children are making progress - keep encouraging them!",
            "🏆 Family study goals are within reach!",
            "💪 Consistency is key to success!"
        ]
        notification = random.choice(notifications)
        # In a real app, this would be a system notification
        # For now, we'll just update the tip label
        if hasattr(self, 'tip_label') and self.tip_label.winfo_exists():
            self.tip_label.config(text=notification)

    def animate_student_circle(self, oval_id, base_color, action):
        """Animate student circles on hover"""
        canvas = self.stats_canvas
        if action == "enter":
            # Scale up and change color
            canvas.scale(oval_id, canvas.coords(oval_id)[0] + 10, canvas.coords(oval_id)[1] + 10, 1.2, 1.2)
            canvas.itemconfig(oval_id, outline="#FFF", width=3)
        elif action == "leave":
            # Scale back and reset
            canvas.scale(oval_id, canvas.coords(oval_id)[0] + 10, canvas.coords(oval_id)[1] + 10, 1/1.2, 1/1.2)
            canvas.itemconfig(oval_id, outline="", width=1)

    def draw_progress_ring(self, canvas, x, y, hours, radius):
        """Draw a progress ring around student circles"""
        # Background ring
        canvas.create_oval(x-radius, y-radius, x+radius, y+radius, outline="#ddd", width=3)

        # Progress arc (assume 10 hours = 100%)
        progress = min(hours / 10, 1)  # Max 10 hours for full ring
        if progress > 0:
            angle = progress * 360
            color = "#4CAF50" if progress >= 0.8 else "#FFC107" if progress >= 0.5 else "#F44336"
            canvas.create_arc(x-radius, y-radius, x+radius, y+radius,
                            start=90, extent=-angle, fill=color, outline="", width=3)

    def animate_bar(self, canvas, bar_id, from_color, to_color):
        """Animate bar color change"""
        canvas.itemconfig(bar_id, fill=to_color)

    def add_achievement_indicators(self, canvas, total_hours, avg_hours, width):
        """Add achievement indicators and badges"""
        # Family achievement badges
        if total_hours >= 40:
            canvas.create_text(width - 30, 20, text="🏆", font=("Arial", 16))
        elif total_hours >= 20:
            canvas.create_text(width - 30, 20, text="⭐", font=("Arial", 16))

        if avg_hours >= 8:
            canvas.create_text(width - 30, 50, text="🌟", font=("Arial", 16))
        elif avg_hours >= 5:
            canvas.create_text(width - 30, 50, text="✨", font=("Arial", 16))

    def logout(self):
        self.stop_notifications = True
        if self.notification_thread:
            self.notification_thread.join(timeout=1)
        self.current_user = None
        self.create_login_screen()

if __name__ == "__main__":
    root = tk.Tk()
    app = ParentApp(root)
    root.mainloop()
