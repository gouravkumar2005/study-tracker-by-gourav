"""
Focus Scoring System - Multi-Signal Fusion
Combines multiple signals to calculate real-time focus score with minimal false positives
"""

import time
from collections import deque
from datetime import datetime


class FocusScorer:
    """
    Multi-signal fusion focus scoring system
    
    Signal Weights (as per requirements):
    - Desktop app usage: 50%
    - Interaction patterns: 25%
    - Eye gaze tracking: 15%
    - Head pose: 10%
    
    Focus Score Interpretation:
    - 80-100: Focused (SILENT, no action)
    - 60-79: Mild drift (SILENT, monitor only)
    - 40-59: Sustained distraction (gentle nudge after continuous period)
    - 0-39: High distraction (warning after 3-5 minutes)
    """
    
    def __init__(self, activity_monitor=None, camera_detector=None):
        self.activity_monitor = activity_monitor
        self.camera_detector = camera_detector
        
        # Focus score history
        self.focus_history = deque(maxlen=300)  # Last 5 minutes @ 1 sample/sec
        
        # Warning system
        self.warning_count = 0
        self.last_warning_time = 0
        self.warning_cooldown = 60  # 60 seconds between warnings
        
        # Thresholds (configurable)
        self.thresholds = {
            'focused': 80,
            'mild_drift': 60,
            'distracted': 40,
            'high_distraction': 0
        }
        
        # Camera efficiency
        self.last_camera_check = 0
        self.camera_check_interval = 3  # Check every 3 seconds
        self.cached_camera_score = 50
        
        # Warning decay system
        self.last_focused_time = time.time()
        self.focused_time_for_decay = 300  # 5 minutes focused = remove 1 warning
    
    def calculate_focus_score(self):
        """
        Calculate real-time focus score using multi-signal fusion
        Returns: (score, breakdown, recommendation)
        """
        now = time.time()
        
        # Signal 1: Desktop App Usage (50% weight)
        app_score = self._get_app_usage_signal()
        
        # Signal 2: Interaction Patterns (25% weight)
        pattern_score = self._get_interaction_pattern_signal()
        
        # Signal 3: Eye Gaze (15% weight) - Low frequency
        eye_score = self._get_eye_gaze_signal(now)
        
        # Signal 4: Head Pose (10% weight) - Low frequency
        pose_score = self._get_head_pose_signal(now)
        
        # Weighted fusion
        focus_score = (
            app_score * 0.50 +
            pattern_score * 0.25 +
            eye_score * 0.15 +
            pose_score * 0.10
        )
        
        # Store in history
        self.focus_history.append({
            'timestamp': now,
            'score': focus_score,
            'app': app_score,
            'pattern': pattern_score,
            'eye': eye_score,
            'pose': pose_score
        })
        
        # Get recommendation
        recommendation = self._get_recommendation(focus_score)
        
        # Update warning decay
        if focus_score >= self.thresholds['focused']:
            if now - self.last_focused_time > self.focused_time_for_decay:
                if self.warning_count > 0:
                    self.warning_count -= 1
                self.last_focused_time = now
        
        breakdown = {
            'app_usage': app_score,
            'interaction_pattern': pattern_score,
            'eye_gaze': eye_score,
            'head_pose': pose_score,
            'warnings': self.warning_count
        }
        
        return round(focus_score, 2), breakdown, recommendation
    
    def _get_app_usage_signal(self):
        """Signal 1: Desktop application usage (50% weight)"""
        if self.activity_monitor:
            return self.activity_monitor.get_app_usage_score()
        return 50  # Neutral if unavailable
    
    def _get_interaction_pattern_signal(self):
        """Signal 2: Keyboard/mouse patterns (25% weight)"""
        if self.activity_monitor:
            return self.activity_monitor.get_interaction_pattern_score()
        return 50  # Neutral if unavailable
    
    def _get_eye_gaze_signal(self, now):
        """Signal 3: Eye gaze tracking (15% weight) - EFFICIENT"""
        # Only check camera every N seconds
        if now - self.last_camera_check < self.camera_check_interval:
            return self.cached_camera_score
        
        if self.camera_detector and hasattr(self.camera_detector, 'get_eye_gaze_score'):
            self.cached_camera_score = self.camera_detector.get_eye_gaze_score()
            self.last_camera_check = now
            return self.cached_camera_score
        
        return 50  # Neutral if unavailable
    
    def _get_head_pose_signal(self, now):
        """Signal 4: Head pose (10% weight) - EFFICIENT"""
        # Reuse camera check timing
        if self.camera_detector and hasattr(self.camera_detector, 'get_head_pose_score'):
            return self.camera_detector.get_head_pose_score()
        return 50  # Neutral if unavailable
    
    def _get_recommendation(self, focus_score):
        """
        Get recommendation based on focus score and history
        IMPORTANT: Most states result in NO ACTION (silent)
        """
        now = time.time()
        
        # Focused - DO NOTHING (silent success state)
        if focus_score >= self.thresholds['focused']:
            return {
                'action': 'none',
                'level': 'success',
                'message': None,
                'should_warn': False
            }
        
        # Mild drift - MONITOR ONLY (still silent)
        if focus_score >= self.thresholds['mild_drift']:
            return {
                'action': 'monitor',
                'level': 'info',
                'message': None,
                'should_warn': False
            }
        
        # Sustained distraction - Check if it's continuous
        if focus_score >= self.thresholds['distracted']:
            # Need sustained low score before warning
            sustained = self._check_sustained_distraction(
                threshold=self.thresholds['distracted'],
                duration=60  # 1 minute of sustained distraction
            )
            
            if sustained and now - self.last_warning_time > self.warning_cooldown:
                self.last_warning_time = now
                self.warning_count += 1
                return {
                    'action': 'gentle_nudge',
                    'level': 'warning',
                    'message': '💭 Taking a break? Ready to refocus?',
                    'should_warn': True
                }
            
            return {
                'action': 'monitor',
                'level': 'info',
                'message': None,
                'should_warn': False
            }
        
        # High distraction - Stronger intervention needed
        sustained = self._check_sustained_distraction(
            threshold=self.thresholds['high_distraction'],
            duration=180  # 3 minutes of high distraction
        )
        
        if sustained and now - self.last_warning_time > self.warning_cooldown:
            self.last_warning_time = now
            self.warning_count += 1
            
            # Escalate message based on warning count
            if self.warning_count <= 2:
                message = '📚 Time to get back to studying'
            elif self.warning_count <= 4:
                message = '⚠️ Multiple distractions detected. Please refocus.'
            else:
                message = '🚨 Consistent distraction. Consider taking a scheduled break.'
            
            return {
                'action': 'warning',
                'level': 'alert',
                'message': message,
                'should_warn': True
            }
        
        # Not yet sustained enough for warning
        return {
            'action': 'monitor',
            'level': 'info',
            'message': None,
            'should_warn': False
        }
    
    def _check_sustained_distraction(self, threshold, duration):
        """
        Check if focus score has been below threshold for sustained duration
        Returns True only if CONTINUOUSLY below threshold
        """
        if len(self.focus_history) < duration:
            return False
        
        now = time.time()
        sustained_period = [
            h for h in self.focus_history 
            if now - h['timestamp'] < duration
        ]
        
        if not sustained_period:
            return False
        
        # Check if ALL samples in period are below threshold
        all_below = all(h['score'] < threshold for h in sustained_period)
        return all_below
    
    def get_session_summary(self):
        """Get summary statistics for completed session"""
        if not self.focus_history:
            return {
                'average_focus': 0,
                'peak_focus': 0,
                'lowest_focus': 0,
                'time_focused': 0,
                'time_distracted': 0,
                'warnings_issued': self.warning_count
            }
        
        scores = [h['score'] for h in self.focus_history]
        
        time_focused = sum(
            1 for h in self.focus_history 
            if h['score'] >= self.thresholds['focused']
        )
        time_distracted = sum(
            1 for h in self.focus_history 
            if h['score'] < self.thresholds['distracted']
        )
        
        return {
            'average_focus': round(sum(scores) / len(scores), 2),
            'peak_focus': round(max(scores), 2),
            'lowest_focus': round(min(scores), 2),
            'time_focused': time_focused,  # seconds
            'time_distracted': time_distracted,  # seconds
            'warnings_issued': self.warning_count,
            'total_samples': len(scores)
        }
    
    def get_focus_trend(self, minutes=5):
        """Get focus trend for last N minutes"""
        now = time.time()
        cutoff = now - (minutes * 60)
        
        recent = [h for h in self.focus_history if h['timestamp'] > cutoff]
        
        if not recent:
            return 'unknown'
        
        # Compare first half to second half
        mid = len(recent) // 2
        first_half_avg = sum(h['score'] for h in recent[:mid]) / max(len(recent[:mid]), 1)
        second_half_avg = sum(h['score'] for h in recent[mid:]) / max(len(recent[mid:]), 1)
        
        diff = second_half_avg - first_half_avg
        
        if diff > 10:
            return 'improving'
        elif diff < -10:
            return 'declining'
        else:
            return 'stable'
    
    def reset_warnings(self):
        """Reset warning count (for new session)"""
        self.warning_count = 0
        self.last_warning_time = 0
        self.last_focused_time = time.time()