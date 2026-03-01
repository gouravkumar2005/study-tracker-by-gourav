#!/usr/bin/env python3
"""
Test script for Activity Monitor
Tests desktop app detection and input pattern analysis
"""

from activity_monitor import ActivityMonitor
import time

def test_activity_monitoring():
    """Test activity monitoring without camera"""
    print("=" * 60)
    print("ACTIVITY MONITOR TEST")
    print("=" * 60)
    print("\nThis will monitor your desktop activity for 30 seconds.")
    print("Try the following to test detection:")
    print("  - Open different applications")
    print("  - Type some text")
    print("  - Click around")
    print("  - Scroll in a browser")
    print("\nStarting in 3 seconds...")
    time.sleep(3)
    
    monitor = ActivityMonitor()
    monitor.start_monitoring()
    
    print("\n" + "=" * 60)
    print("MONITORING ACTIVE - Test for 30 seconds")
    print("=" * 60 + "\n")
    
    for i in range(30):
        time.sleep(1)
        
        app_score = monitor.get_app_usage_score()
        pattern_score = monitor.get_interaction_pattern_score()
        stability = monitor.get_session_stability()
        summary = monitor.get_activity_summary()
        current_app = monitor.current_app or "Unknown"
        
        print(f"[{i+1:2d}s] App: {current_app:20s} | "
              f"Scores: App={app_score:3.0f} Pattern={pattern_score:3.0f} Stability={stability:3.0f} | "
              f"{summary}")
    
    monitor.stop_monitoring()
    
    print("\n" + "=" * 60)
    print("TEST COMPLETE!")
    print("=" * 60)
    print("\nInterpretation:")
    print("  App Score:")
    print("    90-100: Definitely studying (study apps)")
    print("    70-89:  Likely studying")
    print("    40-69:  Mixed/Unknown")
    print("    20-39:  Likely distracted")
    print("    0-19:   Definitely distracted (entertainment/games)")
    print("\n  Pattern Score:")
    print("    >70: Study-like patterns (steady typing, slow scrolling)")
    print("    40-70: Normal usage")
    print("    <40: Distraction patterns (rapid clicks, fast scrolling)")

if __name__ == "__main__":
    try:
        test_activity_monitoring()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
    except Exception as e:
        print(f"\n\nERROR: {e}")
        import traceback
        traceback.print_exc()
        print("\nTroubleshooting:")
        print("  1. Install dependencies: pip install pywin32 psutil pynput")
        print("  2. Run as administrator if on Windows")
        print("  3. Check SETUP_GUIDE.md for help")