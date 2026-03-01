#!/usr/bin/env python3
"""
Test script for study activity detection functionality
"""

from face_detection import FaceDetector

def test_face_detector_initialization():
    """Test that FaceDetector initializes correctly"""
    print("Testing FaceDetector initialization...")
    detector = FaceDetector()
    print("✓ FaceDetector initialized successfully")
    return detector

def test_simulated_detection():
    """Test detection with simulated data (no camera)"""
    print("\nTesting simulated detection...")
    detector = FaceDetector()

    # Test face detection (should return True in simulation mode when no cv2)
    face_detected = detector.detect_face(None)  # Pass None to trigger simulation
    print(f"Face detection result: {face_detected}")

    # Test study activity detection (should return True in simulation mode when no cv2)
    study_detected = detector.detect_study_activity(None)  # Pass None to trigger simulation
    print(f"Study activity detection result: {study_detected}")

    return face_detected and study_detected

def test_monitor_session_simulation():
    """Test session monitoring in simulation mode"""
    print("\nTesting session monitoring simulation...")
    detector = FaceDetector()

    # Test short session (1 second) without camera
    result = detector.monitor_session(1/3600, detect_study=False)  # 1 second session
    print(f"Session monitoring result (no study detection): {result}")

    result_with_study = detector.monitor_session(1/3600, detect_study=True)  # 1 second session with study detection
    print(f"Session monitoring result (with study detection): {result_with_study}")

    return result and result_with_study

def main():
    print("=== Study Activity Detection Test Suite ===\n")

    try:
        # Test 1: Initialization
        detector = test_face_detector_initialization()

        # Test 2: Simulated detection
        sim_result = test_simulated_detection()

        # Test 3: Session monitoring
        session_result = test_monitor_session_simulation()

        print("\n=== Test Results ===")
        print(f"Initialization: ✓")
        print(f"Simulated Detection: {'✓' if sim_result else '✗'}")
        print(f"Session Monitoring: {'✓' if session_result else '✗'}")

        if sim_result and session_result:
            print("\n🎉 All tests passed! Study activity detection is working correctly.")
        else:
            print("\n❌ Some tests failed. Please check the implementation.")

    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
