import cv2

print("Testing camera access...")

for i in [0, 1, -1]:
    print(f"\nTrying camera index {i}...")
    try:
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
        if cap.isOpened():
            print(f"✓ Camera {i} opened successfully!")
            ret, frame = cap.read()
            if ret:
                print(f"✓ Frame captured: {frame.shape}")
            cap.release()
            break
        else:
            print(f"✗ Camera {i} failed to open")
    except Exception as e:
        print(f"✗ Error with camera {i}: {e}")

print("\nTest complete!")
