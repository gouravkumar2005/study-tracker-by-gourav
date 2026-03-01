# 🚀 Setup Guide - Multi-Signal Focus Monitoring System

## Prerequisites

- Windows 10/11 (for desktop app monitoring)
- Python 3.11+
- Webcam (optional, for camera signals)
- Administrator rights (for installing dependencies)

---

## Quick Start (5 Minutes)

### Step 1: Install Dependencies

```bash
# Navigate to your project directory
cd "c:\Users\goura\Desktop\python full"

# Install all required packages
pip install -r requirements.txt
```

**What gets installed:**
- `opencv-python` - Camera and face detection
- `pywin32` - Windows desktop app monitoring
- `psutil` - Process information
- `pynput` - Keyboard/mouse event monitoring
- `Pillow`, `numpy` - Image processing

### Step 2: Test Components

```bash
# Test activity monitoring (no camera needed)
python test_activity_monitor.py

# Test camera functions (requires webcam)
python test_camera.py

# Test full integration
python test_focus_system.py
```

### Step 3: Run the App

```bash
python main.py
```

---

## Detailed Setup

### Option 1: Using New Multi-Signal System

1. **Replace old face detector** with new one:
   ```bash
   # Backup original
   copy face_detection.py face_detection_old_backup.py
   
   # Use new version
   copy face_detection_v2.py face_detection.py
   ```

2. **Update student_gui.py** to use the new system:
   
   Add imports:
   ```python
   from activity_monitor import ActivityMonitor
   from focus_scorer import FocusScorer
   from focus_config import FocusConfig
   ```
   
   Initialize in `__init__`:
   ```python
   self.activity_monitor = ActivityMonitor()
   self.focus_scorer = FocusScorer(self.activity_monitor, self.face_detector)
   ```
   
   Start monitoring when session begins:
   ```python
   self.activity_monitor.start_monitoring()
   ```

3. **Test the integration**:
   ```bash
   python main.py
   ```

### Option 2: Gradual Migration

Keep both systems running in parallel:

1. Add new components without removing old ones
2. Test new system on separate study sessions
3. Compare results
4. Switch when confident

---

## Configuration

### Adjusting Sensitivity

Edit `focus_config.py`:

```python
# For stricter monitoring
FocusConfig.THRESHOLD_FOCUSED = 85  # Higher bar for "focused"
FocusConfig.SUSTAINED_DISTRACTION_DURATION = 30  # Faster warnings

# For relaxed monitoring  
FocusConfig.THRESHOLD_FOCUSED = 75
FocusConfig.SUSTAINED_DISTRACTION_DURATION = 120  # Slower warnings
```

### Adding Custom Study Apps

```python
FocusConfig.STUDY_APPS.add('myapp.exe')
FocusConfig.STUDY_APPS.add('customtool.exe')
```

### Adding Custom Distraction Apps

```python
FocusConfig.DISTRACTION_APPS.add('timewaster.exe')
```

---

## Troubleshooting

### Issue: "Module not found" errors

**Solution:**
```bash
pip install --upgrade -r requirements.txt
```

### Issue: "Could not open camera"

**Solutions:**
1. Check if another app is using the camera
2. Test camera in Camera app
3. Run as administrator
4. Use system without camera (app monitoring still works!)

### Issue: High CPU usage

**Solutions:**
```python
# In focus_config.py
FocusConfig.CAMERA_CHECK_INTERVAL = 5  # Check less frequently
FocusConfig.CAMERA_FPS = 10  # Lower FPS
```

### Issue: Too many false warnings

**Solutions:**
```python
# In focus_config.py  
FocusConfig.WARNING_COOLDOWN = 120  # Longer cooldown
FocusConfig.SUSTAINED_DISTRACTION_DURATION = 180  # Require longer distraction
FocusConfig.THRESHOLD_DISTRACTED = 35  # Lower threshold (more lenient)
```

### Issue: Not enough warnings (missing distractions)

**Solutions:**
```python
# In focus_config.py
FocusConfig.THRESHOLD_FOCUSED = 85  # Higher bar
FocusConfig.SUSTAINED_DISTRACTION_DURATION = 45  # Faster response
FocusConfig.THRESHOLD_DISTRACTED = 45  # Higher threshold (stricter)
```

### Issue: pywin32 installation fails

**Solution:**
```bash
# Download and install manually
# https://github.com/mhammond/pywin32/releases
# Choose the correct Python version (3.11)

# Or try:
pip install --upgrade pywin32
python Scripts/pywin32_postinstall.py -install
```

### Issue: pynput not working

**Solution:**
```bash
# Run as administrator
# Some systems require admin rights for keyboard/mouse monitoring

# Or disable if not needed:
# The system works without input monitoring (just lower accuracy)
```

---

## Performance Optimization

### Low-End Systems

```python
# In focus_config.py
FocusConfig.CAMERA_RESOLUTION = (320, 240)  # Even lower resolution
FocusConfig.CAMERA_CHECK_INTERVAL = 5  # Less frequent
FocusConfig.APP_CHECK_INTERVAL = 3  # Less frequent
```

### High-End Systems

```python
# Can use higher quality for better detection
FocusConfig.CAMERA_RESOLUTION = (640, 480)  # Keep default
FocusConfig.CAMERA_CHECK_INTERVAL = 2  # More frequent
```

---

## Testing

### Test Activity Monitoring (No Camera)

Create `test_activity_monitor.py`:

```python
from activity_monitor import ActivityMonitor
import time

monitor = ActivityMonitor()
monitor.start_monitoring()

print("Testing activity monitoring for 30 seconds...")
print("Try opening different apps and using keyboard/mouse")

for i in range(30):
    time.sleep(1)
    app_score = monitor.get_app_usage_score()
    pattern_score = monitor.get_interaction_pattern_score()
    summary = monitor.get_activity_summary()
    
    print(f"[{i+1}s] App: {app_score}, Pattern: {pattern_score} - {summary}")

monitor.stop_monitoring()
print("Test complete!")
```

Run:
```bash
python test_activity_monitor.py
```

### Test Focus Scoring

Create `test_focus_system.py`:

```python
from activity_monitor import ActivityMonitor
from focus_scorer import FocusScorer
from face_detection_v2 import FaceDetector
import time

# Initialize
activity_monitor = ActivityMonitor()
camera = FaceDetector()
scorer = FocusScorer(activity_monitor, camera)

# Start
activity_monitor.start_monitoring()

print("Testing focus scoring for 60 seconds...")
for i in range(60):
    time.sleep(1)
    score, breakdown, rec = scorer.calculate_focus_score()
    
    print(f"[{i+1}s] Focus: {score} | {rec['action']} - {rec.get('message', 'OK')}")
    print(f"  Breakdown: App={breakdown['app_usage']}, Pattern={breakdown['interaction_pattern']}")
    
activity_monitor.stop_monitoring()
summary = scorer.get_session_summary()
print("\nSession Summary:", summary)
```

Run:
```bash
python test_focus_system.py
```

---

## Uninstall / Rollback

### Remove New Components

```bash
# Delete new files
del activity_monitor.py
del focus_scorer.py
del focus_config.py
del face_detection_v2.py

# Restore backup
copy face_detection_old_backup.py face_detection.py
```

### Uninstall New Dependencies

```bash
pip uninstall pywin32 psutil pynput
```

---

## Next Steps

1. ✅ Complete setup and testing
2. 📊 Run sample study session
3. 🎯 Adjust configuration to your needs
4. 📝 Review ARCHITECTURE.md for details
5. 🚀 Start using for real study sessions!

---

## Support

For issues or questions:
1. Check this guide
2. Review ARCHITECTURE.md
3. Check configuration in focus_config.py
4. Run test scripts to isolate problem

---

## Summary of Files

| File | Purpose | Required? |
|------|---------|-----------|
| `activity_monitor.py` | Desktop app & input monitoring | Yes |
| `focus_scorer.py` | Multi-signal fusion & scoring | Yes |
| `focus_config.py` | Configuration & tuning | Yes |
| `face_detection_v2.py` | Efficient camera monitoring | Optional* |
| `requirements.txt` | Python dependencies | Yes |
| `ARCHITECTURE.md` | System documentation | Reference |
| `SETUP_GUIDE.md` | This file | Reference |

\* System works without camera using just app/input monitoring

---

Good luck with your studies! 📚✨