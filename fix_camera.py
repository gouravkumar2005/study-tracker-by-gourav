import cv2
import sys

print("=" * 60)
print("CAMERA PERMISSION CHECKER")
print("=" * 60)

print("\n1. Checking OpenCV installation...")
try:
    print(f"   ✓ OpenCV version: {cv2.__version__}")
except:
    print("   ✗ OpenCV not found! Install: pip install opencv-python")
    sys.exit(1)

print("\n2. Testing camera access...")
print("\n   Trying different camera backends:")

backends = [
    (cv2.CAP_DSHOW, "DirectShow (Windows)"),
    (cv2.CAP_MSMF, "Media Foundation (Windows)"),
    (cv2.CAP_ANY, "Auto-detect")
]

camera_found = False

for backend, name in backends:
    print(f"\n   Testing {name}...")
    for idx in [0, 1]:
        try:
            cap = cv2.VideoCapture(idx, backend)
            if cap.isOpened():
                ret, frame = cap.read()
                if ret and frame is not None:
                    print(f"      ✓ Camera {idx} WORKS with {name}!")
                    print(f"        Frame size: {frame.shape}")
                    camera_found = True
                    cap.release()
                    break
                else:
                    print(f"      ✗ Camera {idx} opened but can't read frames")
                    cap.release()
            else:
                print(f"      ✗ Camera {idx} failed to open")
        except Exception as e:
            print(f"      ✗ Camera {idx} error: {e}")
    
    if camera_found:
        break

print("\n" + "=" * 60)
if camera_found:
    print("✓ CAMERA IS WORKING!")
else:
    print("✗ CAMERA NOT ACCESSIBLE")
    print("\nFIX STEPS:")
    print("1. Windows Settings > Privacy & Security > Camera")
    print("2. Turn ON 'Camera access'")
    print("3. Turn ON 'Let apps access your camera'")
    print("4. Turn ON 'Let desktop apps access your camera'")
    print("5. Close any app using camera (Zoom, Teams, etc.)")
    print("6. Restart this script")
print("=" * 60)
