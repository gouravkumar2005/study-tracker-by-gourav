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
        
        # Activity tracking
        self.prev_frame = None
        self.motion_threshold = 1000
        self.idle_frames = 0
        self.max_idle_frames = 150
        
        # Advanced detection tracking
        self.face_history = []  # Track face position/size over time
        self.eye_detection_fails = 0
        self.max_eye_fails = 10  # Consecutive eye detection failures
        self.head_angle_history = []
        self.phone_usage_score = 0
        self.distraction_score = 0
        self.hand_region_motion_history = []
        self.face_center_history = []
        self.face_size_history = []
        
        # Reduced frequency camera checking (EFFICIENCY)
        self.last_frame_capture = None
        self.cached_eye_score = 50
        self.cached_pose_score = 50

    def start_camera(self, resolution=(640, 480)):
        """Start camera with reduced resolution for efficiency"""
        if not CV2_AVAILABLE:
            raise Exception("Camera not available: OpenCV not installed")
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise Exception("Could not open camera")
        
        # Set lower resolution (480p) for efficiency
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])
        self.cap.set(cv2.CAP_PROP_FPS, 15)  # Lower FPS for efficiency

    def stop_camera(self):
        if self.cap and CV2_AVAILABLE:
            self.cap.release()
            cv2.destroyAllWindows()

    def detect_face(self, frame):
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
        h, w = frame.shape[:2]

        # Detect faces
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if len(faces) == 0:
            self.eye_detection_fails += 1
            return False

        # Analyze the primary face (largest one)
        face = max(faces, key=lambda f: f[2] * f[3])
        x, y, fw, fh = face
        
        # Track face metrics
        face_center_y = y + fh // 2
        face_size = fw * fh
        face_center = (x + fw // 2, y + fh // 2)
        
        self.face_center_history.append(face_center_y / h)  # Normalized position
        self.face_size_history.append(face_size)
        if len(self.face_center_history) > 30:
            self.face_center_history.pop(0)
            self.face_size_history.pop(0)

        # 1. HEAD ANGLE DETECTION (Most Important!)
        head_tilted_down = self._detect_head_tilt(face, h, w)
        
        # 2. EYE DETECTION (Check if eyes are visible)
        roi_gray = gray[y:y+fh, x:x+fw]
        eyes = self.eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=3, minSize=(15, 15))
        
        eyes_detected = len(eyes) >= 2
        if not eyes_detected:
            self.eye_detection_fails += 1
        else:
            self.eye_detection_fails = max(0, self.eye_detection_fails - 2)

        # 3. PHONE USAGE DETECTION (Hand regions)
        phone_detected = self._detect_phone_usage(frame, face, h, w)
        
        # 4. MICRO-MOVEMENT ANALYSIS (Thumb scrolling)
        scrolling_detected = self._detect_scrolling_pattern(gray)
        
        # 5. FACE POSITION ANALYSIS (Looking down pattern)
        looking_down = self._analyze_face_position_pattern()
        
        # 6. GAZE DIRECTION (Where eyes are pointing)
        gaze_down = self._detect_gaze_direction(eyes, roi_gray, fh) if eyes_detected else True
        
        # 7. HAND MOTION IN SPECIFIC REGIONS
        hand_activity = self._detect_hand_activity_regions(frame, gray, face)
        
        # Calculate distraction scores
        distraction_indicators = {
            'head_tilted': head_tilted_down,
            'no_eyes': self.eye_detection_fails > 5,
            'phone_present': phone_detected,
            'scrolling': scrolling_detected,
            'looking_down_pattern': looking_down,
            'gaze_down': gaze_down,
            'phone_region_activity': hand_activity['phone_region'],
            'face_too_low': face_center_y > h * 0.6,  # Face in lower part of frame
            'face_size_decreased': self._check_face_size_change()
        }
        
        # Count active distraction indicators
        active_distractions = sum(distraction_indicators.values())
        
        # Update phone usage score
        if phone_detected or (head_tilted_down and not eyes_detected):
            self.phone_usage_score = min(100, self.phone_usage_score + 3)
        else:
            self.phone_usage_score = max(0, self.phone_usage_score - 1)
        
        # Update distraction score
        self.distraction_score = (active_distractions / len(distraction_indicators)) * 100
        
        # FINAL DECISION - Be very strict!
        # If ANY major indicator suggests phone/distraction, mark as not studying
        if active_distractions >= 3:  # 3+ indicators = definitely distracted
            return False
        elif self.phone_usage_score > 30:  # Consistent phone usage pattern
            return False
        elif self.distraction_score > 40:  # High overall distraction
            return False
        elif head_tilted_down and not eyes_detected:  # Classic phone usage
            return False
        elif self.eye_detection_fails > self.max_eye_fails:  # Eyes not visible for too long
            return False
        
        # Must have eyes visible and proper posture to count as studying
        return eyes_detected and not head_tilted_down

    def _detect_head_tilt(self, face, frame_h, frame_w):
        """Detect if head is tilted down (looking at phone)"""
        x, y, w, h = face
        face_center_y = y + h // 2
        
        # If face is in lower 60% of frame, likely looking down
        if face_center_y > frame_h * 0.6:
            return True
        
        # Check face aspect ratio (tilted faces are shorter)
        aspect_ratio = h / w if w > 0 else 1
        if aspect_ratio < 1.2:  # Normal face is ~1.3-1.5
            return True
        
        # Check if face moved significantly downward
        if len(self.face_center_history) >= 10:
            recent_avg = sum(self.face_center_history[-10:]) / 10
            if recent_avg > 0.55:  # Face consistently low
                return True
        
        return False

    def _detect_phone_usage(self, frame, face, frame_h, frame_w):
        """Detect rectangular object (phone) in hand regions"""
        x, y, w, h = face
        
        # Define phone regions (below and beside face - where hands hold phone)
        phone_regions = [
            (max(0, x - w), y + h, min(frame_w, x + w * 2), min(frame_h, y + h + int(h * 1.5))),  # Below face
            (max(0, x - int(w * 0.5)), max(0, y - int(h * 0.3)), x + int(w * 0.3), y + h)  # Left side
        ]
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        phone_detected = False
        
        for region in phone_regions:
            rx1, ry1, rx2, ry2 = region
            if rx2 > rx1 and ry2 > ry1:
                roi = gray[ry1:ry2, rx1:rx2]
                
                # Detect edges (phones have rectangular edges)
                edges = cv2.Canny(roi, 50, 150)
                
                # Look for rectangles
                contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                for contour in contours:
                    area = cv2.contourArea(contour)
                    if area > 500:  # Significant object
                        # Check if it's rectangular
                        peri = cv2.arcLength(contour, True)
                        approx = cv2.approxPolyDP(contour, 0.04 * peri, True)
                        
                        # 4 corners = rectangle (likely phone)
                        if len(approx) == 4:
                            phone_detected = True
                            break
        
        return phone_detected

    def _detect_scrolling_pattern(self, gray):
        """Detect micro-movements typical of thumb scrolling"""
        if self.prev_frame is None:
            return False
        
        # Calculate optical flow in hand regions (bottom 40% of frame)
        h, w = gray.shape
        hand_region = gray[int(h * 0.6):, :]
        prev_hand_region = self.prev_frame[int(h * 0.6):, :]
        
        # Detect small repeated motions
        diff = cv2.absdiff(hand_region, prev_hand_region)
        _, thresh = cv2.threshold(diff, 15, 255, cv2.THRESH_BINARY)
        
        motion = cv2.countNonZero(thresh)
        
        self.hand_region_motion_history.append(motion)
        if len(self.hand_region_motion_history) > 20:
            self.hand_region_motion_history.pop(0)
        
        # Scrolling creates rhythmic motion pattern
        if len(self.hand_region_motion_history) >= 10:
            # Check for repeated small motions (scrolling pattern)
            recent_motions = self.hand_region_motion_history[-10:]
            avg_motion = sum(recent_motions) / len(recent_motions)
            
            # Scrolling: consistent small motion (200-1000 pixels)
            if 200 < avg_motion < 1000:
                # Check for rhythmic pattern
                variations = [abs(recent_motions[i] - recent_motions[i-1]) for i in range(1, len(recent_motions))]
                avg_variation = sum(variations) / len(variations)
                
                # Low variation = rhythmic scrolling
                if avg_variation < 300:
                    return True
        
        return False

    def _analyze_face_position_pattern(self):
        """Analyze if face position suggests looking down at phone"""
        if len(self.face_center_history) < 15:
            return False
        
        # Calculate average face position
        recent_positions = self.face_center_history[-15:]
        avg_position = sum(recent_positions) / len(recent_positions)
        
        # Face consistently in lower portion (> 0.55 normalized)
        if avg_position > 0.55:
            # Check if it's stable (not just moving down temporarily)
            position_variance = sum((p - avg_position) ** 2 for p in recent_positions) / len(recent_positions)
            
            # Low variance + low position = stable phone-watching position
            if position_variance < 0.01:
                return True
        
        return False

    def _detect_gaze_direction(self, eyes, roi_gray, face_height):
        """Detect if eyes are looking down vs forward"""
        if len(eyes) < 2:
            return True  # Can't determine, assume looking down
        
        # Sort eyes by y-coordinate to find top eye
        eyes_sorted = sorted(eyes, key=lambda e: e[1])
        
        # Calculate eye position relative to face
        avg_eye_y = sum(e[1] for e in eyes) / len(eyes)
        
        # If eyes are in lower 60% of face region, likely looking down
        if avg_eye_y > face_height * 0.6:
            return True
        
        # Check eye aspect ratio (eyes looking down are more closed)
        eye_heights = [e[3] for e in eyes]
        avg_eye_height = sum(eye_heights) / len(eye_heights)
        
        # Very small eye height = squinting/looking down
        if avg_eye_height < 10:
            return True
        
        return False

    def _detect_hand_activity_regions(self, frame, gray, face):
        """Detect hand movements in regions typical of phone usage"""
        x, y, w, h = face
        frame_h, frame_w = gray.shape
        
        # Define regions where phone would be held
        regions = {
            'phone_region': (max(0, x - w//2), y + h, min(frame_w, x + w*2), min(frame_h, frame_h)),  # Below face
            'lap_region': (0, int(frame_h * 0.7), frame_w, frame_h),  # Bottom 30% (lap)
            'side_region': (0, y, x, y + h)  # Left of face
        }
        
        activity = {}
        
        if self.prev_frame is None:
            return {k: False for k in regions.keys()}
        
        for region_name, (rx1, ry1, rx2, ry2) in regions.items():
            if rx2 > rx1 and ry2 > ry1:
                curr_region = gray[ry1:ry2, rx1:rx2]
                prev_region = self.prev_frame[ry1:ry2, rx1:rx2]
                
                diff = cv2.absdiff(curr_region, prev_region)
                _, thresh = cv2.threshold(diff, 20, 255, cv2.THRESH_BINARY)
                motion = cv2.countNonZero(thresh)
                
                # Significant motion in phone-holding regions
                region_size = (rx2 - rx1) * (ry2 - ry1)
                motion_ratio = motion / region_size if region_size > 0 else 0
                
                # Even small motion in these regions is suspicious
                activity[region_name] = motion_ratio > 0.01
            else:
                activity[region_name] = False
        
        return activity

    def _check_face_size_change(self):
        """Detect if face size decreased (leaning back to watch phone)"""
        if len(self.face_size_history) < 10:
            return False
        
        # Compare recent size to baseline
        baseline = sum(self.face_size_history[:5]) / 5
        recent = sum(self.face_size_history[-5:]) / 5
        
        # Face got 20% smaller = leaned back
        if baseline > 0 and recent < baseline * 0.8:
            return True
        
        return False

    def analyze_activity_pattern(self, frame, gray):
        """Analyze frame differences to detect activity type
        Returns: 'studying', 'gaming', 'watching', 'idle', 'moving'
        """
        if not CV2_AVAILABLE or self.prev_frame is None:
            self.prev_frame = gray.copy()
            return 'studying'

        # Calculate frame difference
        frame_diff = cv2.absdiff(self.prev_frame, gray)
        _, thresh = cv2.threshold(frame_diff, 25, 255, cv2.THRESH_BINARY)
        
        # Count non-zero pixels (motion)
        motion_pixels = cv2.countNonZero(thresh)
        
        # Analyze motion in different regions
        h, w = gray.shape
        
        # Upper region (head movement)
        upper_region = thresh[0:h//2, :]
        upper_motion = cv2.countNonZero(upper_region)
        
        # Lower region (hand/body movement)
        lower_region = thresh[h//2:, :]
        lower_motion = cv2.countNonZero(lower_region)
        
        # Center region (screen area typically)
        center_region = thresh[h//4:3*h//4, w//4:3*w//4]
        center_motion = cv2.countNonZero(center_region)
        
        # Activity classification
        if motion_pixels < 500:
            # Very little motion - idle or just watching
            self.idle_frames += 1
            if self.idle_frames > self.max_idle_frames:
                activity = 'idle'  # Sitting idle for too long
            else:
                activity = 'watching'  # Watching screen
        else:
            self.idle_frames = 0
            
            # Significant motion detected
            if lower_motion > upper_motion * 2:
                # More lower body motion (hands) - could be gaming or typing
                if motion_pixels > 3000:
                    activity = 'gaming'  # Rapid hand movements (gaming)
                else:
                    activity = 'studying'  # Normal hand movements (writing/typing)
            elif center_motion > motion_pixels * 0.6:
                # Motion concentrated in center - watching videos
                activity = 'watching'
            elif motion_pixels > 5000:
                # Too much motion - moving around
                activity = 'moving'
            else:
                # Normal studying motion pattern
                activity = 'studying'
        
        # Update previous frame
        self.prev_frame = gray.copy()
        
        return activity

    def monitor_session(self, duration_hours, detect_study=False, callback=None):
        """
        Monitor study session with advanced detection and warnings
        callback: function to call with monitoring updates (status, warnings, elapsed_time)
        """
        if not CV2_AVAILABLE:
            # Simulate monitoring without camera
            time.sleep(duration_hours * 3600)
            return {'success': True, 'warnings': 0, 'focus_score': 100}

        if not self.cap:
            self.start_camera()

        start_time = time.time()
        end_time = start_time + (duration_hours * 3600)
        
        # Tracking variables
        face_present = True
        study_active = True
        last_face_time = start_time
        last_study_time = start_time
        warning_count = 0
        total_checks = 0
        successful_checks = 0
        
        # Warning thresholds
        face_warning_threshold = 10  # seconds
        study_warning_threshold = 30  # seconds
        
        last_warning_time = 0
        warning_cooldown = 5  # seconds between warnings

        while time.time() < end_time:
            ret, frame = self.cap.read()
            if not ret:
                break

            current_time = time.time()
            total_checks += 1

            # Check face presence
            face_detected = self.detect_face(frame)
            if face_detected:
                last_face_time = current_time
                face_present = True
            else:
                time_since_face = current_time - last_face_time
                if time_since_face > face_warning_threshold:
                    face_present = False
                    # Trigger warning if cooldown passed
                    if current_time - last_warning_time > warning_cooldown:
                        warning_count += 1
                        last_warning_time = current_time
                        if callback:
                            callback({
                                'status': 'warning',
                                'type': 'no_face',
                                'message': '⚠️ Face not detected! Please return to your study area.',
                                'warnings': warning_count,
                                'elapsed_time': current_time - start_time,
                                'remaining_time': end_time - current_time
                            })

            # Check study activity if enabled
            if detect_study:
                studying = self.detect_study_activity(frame)
                if studying:
                    last_study_time = current_time
                    study_active = True
                    successful_checks += 1
                else:
                    time_since_study = current_time - last_study_time
                    if time_since_study > study_warning_threshold:
                        study_active = False
                        # Detect specific activity type for detailed warning
                        activity, confidence = self.detect_specific_activity(frame)
                        
                        # Trigger warning if cooldown passed
                        if current_time - last_warning_time > warning_cooldown:
                            warning_count += 1
                            last_warning_time = current_time
                            
                            # Detect specific activity for targeted warning
                            activity, confidence = self.detect_specific_activity(frame)
                            
                            # Highly specific warning messages
                            if activity == 'phone_gaming':
                                warning_msg = '🎮📱 MOBILE GAMING DETECTED! Put your phone away immediately!'
                            elif activity == 'phone_reels':
                                warning_msg = '📱📺 WATCHING REELS/VIDEOS! Stop scrolling and study now!'
                            elif activity == 'phone_usage':
                                warning_msg = '📱 PHONE IN HAND DETECTED! Put it down and focus on studies!'
                            elif activity == 'looking_away':
                                warning_msg = '👀 LOOKING AWAY! Keep your eyes on study material!'
                            elif activity == 'distracted':
                                warning_msg = '⚠️ HIGH DISTRACTION DETECTED! Refocus immediately!'
                            elif activity == 'gaming':
                                warning_msg = '🎮 GAMING DETECTED! Close games and return to studying!'
                            elif activity == 'watching':
                                warning_msg = '📺 WATCHING SCREEN! Close videos/entertainment!'
                            elif activity == 'idle':
                                warning_msg = '😴 SITTING IDLE! Pick up your study materials now!'
                            else:
                                warning_msg = '⚠️ NOT STUDYING DETECTED! Focus on your studies!'
                            
                            if callback:
                                callback({
                                    'status': 'warning',
                                    'type': f'not_studying_{activity}',
                                    'message': warning_msg,
                                    'warnings': warning_count,
                                    'activity': activity,
                                    'confidence': confidence,
                                    'phone_score': self.phone_usage_score,
                                    'distraction_score': self.distraction_score,
                                    'elapsed_time': current_time - start_time,
                                    'remaining_time': end_time - current_time
                                })
            else:
                if face_detected:
                    successful_checks += 1

            # Send status update
            if callback and total_checks % 30 == 0:  # Every 30 frames (~1 second)
                callback({
                    'status': 'monitoring',
                    'face_present': face_present,
                    'study_active': study_active if detect_study else None,
                    'warnings': warning_count,
                    'elapsed_time': current_time - start_time,
                    'remaining_time': end_time - current_time
                })

            # Draw monitoring info on frame
            self._draw_monitoring_overlay(frame, face_present, study_active if detect_study else None, 
                                         warning_count, current_time - start_time, end_time - current_time)

            cv2.imshow('Study Session Monitor', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.stop_camera()
        
        # Calculate focus score
        focus_score = (successful_checks / total_checks * 100) if total_checks > 0 else 0
        
        return {
            'success': face_present and (study_active if detect_study else True),
            'warnings': warning_count,
            'focus_score': round(focus_score, 2),
            'total_time': duration_hours * 3600,
            'total_checks': total_checks,
            'successful_checks': successful_checks
        }

    def detect_specific_activity(self, frame):
        """Detect specific non-study activities with high precision
        Returns: activity_name and confidence
        """
        if not CV2_AVAILABLE:
            return 'unknown', 0
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Get basic activity pattern
        basic_activity = self.analyze_activity_pattern(frame, gray)
        
        # Enhanced detection with phone usage score
        if self.phone_usage_score > 50:
            if self.distraction_score > 60:
                return 'phone_gaming', 0.95  # Very confident
            else:
                return 'phone_reels', 0.90  # Watching reels/videos
        elif self.phone_usage_score > 30:
            return 'phone_usage', 0.85
        elif self.distraction_score > 50:
            return 'distracted', 0.80
        elif self.eye_detection_fails > 8:
            return 'looking_away', 0.75
        elif basic_activity == 'gaming':
            return 'gaming', 0.85
        elif basic_activity == 'watching':
            return 'watching', 0.80
        elif basic_activity == 'idle':
            return 'idle', 0.70
        elif basic_activity == 'studying':
            return 'studying', 0.60
        
        return basic_activity, 0.50

    def _draw_monitoring_overlay(self, frame, face_present, study_active, warnings, elapsed, remaining):
        """Draw advanced monitoring overlay with detailed detection info"""
        height, width = frame.shape[:2]
        
        # Semi-transparent overlay at top
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (width, 140), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        # Status indicators
        face_color = (0, 255, 0) if face_present else (0, 0, 255)
        face_text = "✓ Face OK" if face_present else "✗ No Face"
        cv2.putText(frame, face_text, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, face_color, 2)
        
        if study_active is not None:
            study_color = (0, 255, 0) if study_active else (0, 0, 255)
            study_text = "✓ STUDYING" if study_active else "✗ NOT STUDYING"
            cv2.putText(frame, study_text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, study_color, 2)
            
            # Show detected activity with confidence
            activity, confidence = self.detect_specific_activity(frame)
            activity_colors = {
                'studying': (0, 255, 0),
                'phone_gaming': (0, 0, 255),
                'phone_reels': (255, 0, 255),
                'phone_usage': (255, 128, 0),
                'distracted': (0, 165, 255),
                'looking_away': (128, 128, 255),
                'gaming': (0, 0, 255),
                'watching': (0, 165, 255),
                'idle': (128, 128, 128),
                'moving': (255, 255, 0)
            }
            activity_color = activity_colors.get(activity, (255, 255, 255))
            activity_text = f"{activity.upper().replace('_', ' ')} ({confidence*100:.0f}%)"
            cv2.putText(frame, activity_text, (10, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.5, activity_color, 2)
            
            # Advanced detection scores
            cv2.putText(frame, f"Phone Score: {self.phone_usage_score:.0f}%", 
                       (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 165, 0), 1)
            cv2.putText(frame, f"Distraction: {self.distraction_score:.0f}%", 
                       (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 100, 100), 1)
        
        # Warnings count with visual indicator
        warning_color = (0, 255, 0) if warnings < 3 else (0, 165, 255) if warnings < 5 else (0, 0, 255)
        cv2.putText(frame, f"Warnings: {warnings}", (width - 200, 25), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, warning_color, 2)
        
        # Warning bar
        bar_width = min(warnings * 20, 180)
        cv2.rectangle(frame, (width - 200, 35), (width - 200 + bar_width, 45), warning_color, -1)
        
        # Time info
        elapsed_str = f"{int(elapsed//60)}:{int(elapsed%60):02d}"
        remaining_str = f"{int(remaining//60)}:{int(remaining%60):02d}"
        cv2.putText(frame, f"Time: {elapsed_str} / {remaining_str}", 
                   (width - 300, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Critical alerts at bottom
        activity, confidence = self.detect_specific_activity(frame)
        
        if not face_present:
            cv2.putText(frame, "⚠️ RETURN TO STUDY AREA NOW!", (width//2 - 220, height - 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
        elif activity == 'phone_gaming':
            cv2.putText(frame, "🎮 MOBILE GAMING DETECTED - STOP NOW!", (width//2 - 280, height - 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
        elif activity == 'phone_reels':
            cv2.putText(frame, "📱 WATCHING REELS DETECTED - FOCUS!", (width//2 - 270, height - 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 3)
        elif activity == 'phone_usage':
            cv2.putText(frame, "📱 PHONE USAGE DETECTED - PUT IT DOWN!", (width//2 - 280, height - 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 128, 0), 3)
        elif activity == 'gaming':
            cv2.putText(frame, "🎮 GAMING DETECTED - STUDY NOW!", (width//2 - 240, height - 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
        elif activity == 'watching':
            cv2.putText(frame, "📺 WATCHING SCREEN - STUDY INSTEAD!", (width//2 - 260, height - 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 165, 255), 3)
        elif activity == 'idle':
            cv2.putText(frame, "😴 SITTING IDLE - START STUDYING!", (width//2 - 240, height - 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (128, 128, 128), 3)
        elif activity == 'distracted':
            cv2.putText(frame, "👀 DISTRACTED - FOCUS ON STUDIES!", (width//2 - 240, height - 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 100, 100), 3)
        elif study_active:
            cv2.putText(frame, "✅ GOOD - KEEP STUDYING!", (width//2 - 180, height - 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 3)
