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
        self.face_history = []
        self.eye_detection_fails = 0
        self.max_eye_fails = 10
        self.head_angle_history = []
        self.phone_usage_score = 0
        self.distraction_score = 0
        self.hand_region_motion_history = []
        self.face_center_history = []
        self.face_size_history = []
        
        # Reduced frequency camera checking
        self.last_frame_capture = None
        self.cached_eye_score = 50
        self.cached_pose_score = 50

    def start_camera(self, resolution=(640, 480)):
        """Start camera with reduced resolution for efficiency"""
        if not CV2_AVAILABLE:
            raise Exception("Camera not available: OpenCV not installed")
        
        # Try multiple camera indices with DirectShow backend for Windows
        for camera_index in [0, 1, -1]:
            try:
                self.cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
                if self.cap.isOpened():
                    break
            except:
                continue
        
        if not self.cap or not self.cap.isOpened():
            raise Exception("Could not open camera. Check camera permissions in Windows Settings > Privacy > Camera")
        
        # Set lower resolution (480p) for efficiency
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])
        self.cap.set(cv2.CAP_PROP_FPS, 15)

    def stop_camera(self):
        if self.cap and CV2_AVAILABLE:
            self.cap.release()
            cv2.destroyAllWindows()

    def detect_face(self, frame):
        if not CV2_AVAILABLE:
            return True
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        return len(faces) > 0
