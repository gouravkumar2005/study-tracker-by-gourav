import cv2
import sys

print("=" * 60)
print("CAMERA TEST")
print("=" * 60)

print("\n1. Checking OpenCV...")
try:
    print(f"   OK - OpenCV version: {cv2.__version__}")
except:
    print("   ERROR - OpenCV not found!")
    sys.exit(1)

print("\n2. Testing camera...")

backends = [
    (cv2.CAP_DSHOW, "DirectShow"),
    (cv2.CAP_MSMF, "Media Foundation"),
    (cv2.CAP_ANY, "Auto")
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
                    print(f"      SUCCESS! Camera {idx} works with {name}")
                    print(f"      Frame size: {frame.shape}")
                    camera_found = True
                    cap.release()
                    break
                else:
                    cap.release()
        except Exception as e:
            print(f"      Error: {e}")
    
    if camera_found:
        break

print("\n" + "=" * 60)
if camera_found:
    print("SUCCESS - CAMERA IS WORKING!")
else:
    print("FAILED - CAMERA NOT ACCESSIBLE")
    print("\nFIX:")
    print("1. Windows Settings > Privacy > Camera")
    print("2. Enable 'Camera access'")
    print("3. Enable 'Let apps access camera'")
    print("4. Enable 'Let desktop apps access camera'")
    print("5. Close Zoom/Teams/other camera apps")
print("=" * 60)
