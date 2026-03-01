"""
Enhanced Face Detection with Multi-Signal Fusion Support
Adapted for production-grade focus monitoring with efficiency optimizations
"""

try:
    import cv2  # type: ignore
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
import time


class FaceDetector:
    def __init__(self):
        if not CV2_AVAILABLE:
            print("Warning: OpenCV not available. Face detection will be simulated.")
            self.face_cascade = None
            self.eye_cascade = None
        else:
            self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        self.cap = None
        
        # Reduced frequency camera checking (EFFICIENCY)
        self.last_frame_capture = None
        self.cached_eye_score = 50
        self.cached_pose_score = 50
        
        # Legacy tracking (for backward compatibility)
        self.prev_frame = None
        self.eye_detection_fails = 0

    def start_camera(self, resolution=(640, 480)):
        """Start camera with reduced resolution for efficiency (480p)"""
        if not CV2_AVAILABLE:
            raise Exception("Camera not available: OpenCV not installed")
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise Exception("Could not open camera")
        
        # Set lower resolution for efficiency
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])
        self.cap.set(cv2.CAP_PROP_FPS, 15)  # Lower FPS

    def stop_camera(self):
        if self.cap and CV2_AVAILABLE:
            self.cap.release()
            cv2.destroyAllWindows()

    def detect_face(self, frame):
        """Simple face presence detection"""
        if not CV2_AVAILABLE:
            return True  # Simulate face always present
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        return len(faces) > 0
    
    def get_eye_gaze_score(self):
        """
        Get eye gaze score for focus scoring (15% weight)
        Only called every 3 seconds for efficiency
        Returns 0-100 where higher = better focus
        """
        if not CV2_AVAILABLE:
            return 50
        
        if not self.cap or not self.cap.isOpened():
            return self.cached_eye_score
        
        ret, frame = self.cap.read()
        if not ret:
            return self.cached_eye_score
        
        self.last_frame_capture = frame
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect face and eyes
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        if len(faces) == 0:
            self.cached_eye_score = 30  # No face visible
            return self.cached_eye_score
        
        # Get largest face
        face = max(faces, key=lambda f: f[2] * f[3])
        x, y, w, h = face
        
        # Check for eyes
        roi_gray = gray[y:y+h, x:x+w]
        eyes = self.eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=3, minSize=(15, 15))
        
        score = 50  # Start neutral
        
        if len(eyes) >= 2:
            # Eyes detected - good sign
            score = 75
            
            # Analyze eye position (looking forward vs down)
            avg_eye_y = sum(e[1] for e in eyes) / len(eyes)
            if avg_eye_y < h * 0.6:  # Eyes in upper 60% of face
                score = 85  # Looking forward
        elif len(eyes) == 1:
            score = 60  # One eye visible
        else:
            score = 40  # No eyes visible
        
        self.cached_eye_score = score
        return score
    
    def get_head_pose_score(self):
        """
        Get head pose score for focus scoring (10% weight)
        Returns 0-100 where higher = better posture
        """
        if not CV2_AVAILABLE:
            return 50
        
        if self.last_frame_capture is None:
            return self.cached_pose_score
        
        gray = cv2.cvtColor(self.last_frame_capture, cv2.COLOR_BGR2GRAY)
        h, w = gray.shape
        
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        if len(faces) == 0:
            self.cached_pose_score = 30
            return self.cached_pose_score
        
        face = max(faces, key=lambda f: f[2] * f[3])
        x, y, fw, fh = face
        
        score = 50
        
        # Check head position (not too low in frame)
        face_center_y = y + fh // 2
        normalized_y = face_center_y / h
        
        if normalized_y < 0.45:
            score = 90  # Good upright posture
        elif normalized_y < 0.55:
            score = 75  # Acceptable posture
        elif normalized_y < 0.65:
            score = 50  # Slightly low
        else:
            score = 30  # Head too low (looking down)
        
        # Check face size (distance from camera)
        face_area = fw * fh
        frame_area = w * h
        face_ratio = face_area / frame_area
        
        if 0.05 < face_ratio < 0.3:  # Good distance
            score = min(100, score + 10)
        
        self.cached_pose_score = score
        return score
    
    def monitor_session_with_focus_scorer(self, duration_hours, focus_scorer, callback=None):
        """
        NEW: Monitor session using FocusScorer multi-signal fusion
        This is the production-grade monitoring method
        """
        if not CV2_AVAILABLE:
            # Simulate monitoring without camera
            time.sleep(duration_hours * 3600)
            return {'success': True, 'warnings': 0, 'focus_score': 100}
        
        if not self.cap:
            self.start_camera()
        
        start_time = time.time()
        end_time = start_time + (duration_hours * 3600)
        
        last_update = start_time
        update_interval = 1  # Update every second
        
        while time.time() < end_time:
            current_time = time.time()
            
            # Update focus score every second
            if current_time - last_update >= update_interval:
                score, breakdown, recommendation = focus_scorer.calculate_focus_score()
                last_update = current_time
                
                # Send callback with current status
                if callback:
                    callback({
                        'status': 'monitoring',
                        'focus_score': score,
                        'breakdown': breakdown,
                        'recommendation': recommendation,
                        'elapsed_time': current_time - start_time,
                        'remaining_time': end_time - current_time
                    })
                    
                    # Send warning if needed
                    if recommendation['should_warn']:
                        callback({
                            'status': 'warning',
                            'type': recommendation['action'],
                            'message': recommendation['message'],
                            'focus_score': score,
                            'warnings': breakdown['warnings'],
                            'elapsed_time': current_time - start_time,
                            'remaining_time': end_time - current_time
                        })
            
            # Small sleep to prevent CPU overload
            time.sleep(0.1)
        
        self.stop_camera()
        
        # Get session summary
        summary = focus_scorer.get_session_summary()
        
        return {
            'success': True,
            'warnings': summary['warnings_issued'],
            'focus_score': summary['average_focus'],
            'total_time': duration_hours * 3600,
            'peak_focus': summary['peak_focus'],
            'time_focused': summary['time_focused'],
            'time_distracted': summary['time_distracted']
        }
    
    # ===== LEGACY METHODS FOR BACKWARD COMPATIBILITY =====
    
    def monitor_session(self, duration_hours, detect_study=False, callback=None):
        """
        LEGACY: Original monitoring method (kept for backward compatibility)
        For new code, use monitor_session_with_focus_scorer instead
        """
        if not CV2_AVAILABLE:
            time.sleep(duration_hours * 3600)
            return {'success': True, 'warnings': 0, 'focus_score': 100}
        
        if not self.cap:
            self.start_camera()
        
        start_time = time.time()
        end_time = start_time + (duration_hours * 3600)
        
        warning_count = 0
        total_checks = 0
        successful_checks = 0
        last_face_time = start_time
        
        while time.time() < end_time:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            current_time = time.time()
            total_checks += 1
            
            face_detected = self.detect_face(frame)
            if face_detected:
                last_face_time = current_time
                successful_checks += 1
            else:
                if current_time - last_face_time > 10:  # 10 seconds no face
                    warning_count += 1
                    if callback:
                        callback({
                            'status': 'warning',
                            'type': 'no_face',
                            'message': '⚠️ Face not detected!',
                            'warnings': warning_count,
                            'elapsed_time': current_time - start_time,
                            'remaining_time': end_time - current_time
                        })
                    last_face_time = current_time  # Reset
            
            time.sleep(1)  # Check every second
        
        self.stop_camera()
        
        focus_score = (successful_checks / total_checks * 100) if total_checks > 0 else 0
        
        return {
            'success': True,
            'warnings': warning_count,
            'focus_score': round(focus_score, 2),
            'total_time': duration_hours * 3600,
            'total_checks': total_checks,
            'successful_checks': successful_checks
        }