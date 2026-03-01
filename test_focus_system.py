#!/usr/bin/env python3
"""
Test script for complete Focus Monitoring System
Tests multi-signal fusion and focus scoring
"""

from activity_monitor import ActivityMonitor
from focus_scorer import FocusScorer
from face_detection_v2 import FaceDetector
from focus_config import FocusConfig
import time

def test_focus_system(use_camera=False):
    """Test complete focus monitoring system"""
    print("=" * 70)
    print("FOCUS MONITORING SYSTEM TEST")
    print("=" * 70)
    print(f"\nCamera: {'ENABLED' if use_camera else 'DISABLED (app/input only)'}")
    print(f"Test Duration: 60 seconds")
    print(f"\nConfiguration:")
    print(f"  Focused Threshold: {FocusConfig.THRESHOLD_FOCUSED}")
    print(f"  Distracted Threshold: {FocusConfig.THRESHOLD_DISTRACTED}")
    print(f"  Warning Cooldown: {FocusConfig.WARNING_COOLDOWN}s")
    print("\nTry different activities to test detection:")
    print("  ✅ Study apps (Word, PDF, Code Editor, Browser with docs)")
    print("  ❌ Distraction apps (Games, Social Media, YouTube entertainment)")
    print("  ⌨️  Different typing/clicking patterns")
    
    print("\nStarting in 3 seconds...")
    time.sleep(3)
    
    # Initialize components
    activity_monitor = ActivityMonitor()
    camera = FaceDetector() if use_camera else None
    scorer = FocusScorer(activity_monitor, camera)
    
    # Start monitoring
    activity_monitor.start_monitoring()
    if use_camera:
        try:
            camera.start_camera()
            print("\n✓ Camera started successfully")
        except Exception as e:
            print(f"\n⚠️  Camera failed to start: {e}")
            print("Continuing without camera...")
            camera = None
            scorer.camera_detector = None
    
    print("\n" + "=" * 70)
    print("MONITORING ACTIVE")
    print("=" * 70 + "\n")
    
    try:
        for i in range(60):
            time.sleep(1)
            
            # Get focus score
            score, breakdown, recommendation = scorer.calculate_focus_score()
            
            # Display status
            status_icon = "✅" if score >= 80 else "💭" if score >= 60 else "⚠️" if score >= 40 else "🚨"
            action_text = recommendation['action'].upper().ljust(12)
            
            print(f"[{i+1:2d}s] {status_icon} Focus: {score:5.1f} | {action_text} | "
                  f"App={breakdown['app_usage']:3.0f} Pattern={breakdown['interaction_pattern']:3.0f} "
                  f"Eye={breakdown['eye_gaze']:3.0f} Pose={breakdown['head_pose']:3.0f} "
                  f"Warnings={breakdown['warnings']}")
            
            # Show warning messages
            if recommendation['should_warn'] and recommendation.get('message'):
                print(f"     >>> {recommendation['message']}")
    
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
    
    finally:
        # Cleanup
        activity_monitor.stop_monitoring()
        if camera:
            camera.stop_camera()
        
        # Get summary
        summary = scorer.get_session_summary()
        
        print("\n" + "=" * 70)
        print("SESSION SUMMARY")
        print("=" * 70)
        print(f"\n  Average Focus Score: {summary['average_focus']:.1f}")
        print(f"  Peak Focus Score:    {summary['peak_focus']:.1f}")
        print(f"  Lowest Focus Score:  {summary['lowest_focus']:.1f}")
        print(f"\n  Time Focused:        {summary['time_focused']} seconds ({summary['time_focused']/60:.1f} min)")
        print(f"  Time Distracted:     {summary['time_distracted']} seconds ({summary['time_distracted']/60:.1f} min)")
        print(f"\n  Warnings Issued:     {summary['warnings_issued']}")
        print(f"  Total Samples:       {summary['total_samples']}")
        
        # Calculate percentages
        total_time = summary['total_samples']
        if total_time > 0:
            focused_pct = (summary['time_focused'] / total_time) * 100
            distracted_pct = (summary['time_distracted'] / total_time) * 100
            
            print(f"\n  Focus Percentage:    {focused_pct:.1f}%")
            print(f"  Distraction Pct:     {distracted_pct:.1f}%")
        
        print("\n" + "=" * 70)
        print("INTERPRETATION")
        print("=" * 70)
        
        if summary['average_focus'] >= 80:
            print("\n  🎉 EXCELLENT! Great focus throughout the session.")
        elif summary['average_focus'] >= 60:
            print("\n  ✅ GOOD! Mostly focused with some drift.")
        elif summary['average_focus'] >= 40:
            print("\n  ⚠️  NEEDS IMPROVEMENT. Too many distractions.")
        else:
            print("\n  🚨 POOR FOCUS. Major distractions detected.")
        
        if summary['warnings_issued'] == 0:
            print("  ✨ Perfect session with no warnings!")
        elif summary['warnings_issued'] <= 2:
            print(f"  👍 Acceptable session with {summary['warnings_issued']} warning(s).")
        else:
            print(f"  ⚠️  {summary['warnings_issued']} warnings issued. Try to minimize distractions.")

if __name__ == "__main__":
    import sys
    
    # Check for camera flag
    use_camera = '--camera' in sys.argv or '-c' in sys.argv
    
    if not use_camera:
        print("\nℹ️  Running without camera (app/input monitoring only)")
        print("   To test with camera, run: python test_focus_system.py --camera\n")
    
    try:
        test_focus_system(use_camera=use_camera)
    except Exception as e:
        print(f"\n\nERROR: {e}")
        import traceback
        traceback.print_exc()
        print("\nTroubleshooting:")
        print("  1. Install dependencies: pip install -r requirements.txt")
        print("  2. Run as administrator if on Windows")  
        print("  3. Check SETUP_GUIDE.md for detailed help")
        print("  4. Ensure webcam is available if using --camera flag")