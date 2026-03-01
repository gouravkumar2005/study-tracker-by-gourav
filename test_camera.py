import cv2
import time

def test_camera():
    print("Testing camera functionality...")

    # Check if OpenCV is available
    try:
        print("OpenCV version:", cv2.__version__)
    except AttributeError:
        print("OpenCV not properly installed")
        return False

    # Try to open camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Could not open camera")
        return False

    print("Camera opened successfully")

    # Try to read a frame
    ret, frame = cap.read()
    if not ret:
        print("Could not read frame from camera")
        cap.release()
        return False

    print("Frame read successfully, shape:", frame.shape)

    # Try face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    print(f"Detected {len(faces)} faces in test frame")

    # Show frame for 2 seconds
    cv2.imshow('Camera Test', frame)
    cv2.waitKey(2000)
    cv2.destroyAllWindows()

    cap.release()
    print("Camera test completed successfully")
    return True

if __name__ == "__main__":
    test_camera()
