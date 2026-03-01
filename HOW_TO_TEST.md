# 🧪 How to Test the New System

## ✅ App is Running!

Your study tracker app is now integrated with the multi-signal fusion system that can detect YouTube and other distractions!

---

## 🎯 Test It Now

### Step 1: Login
1. Click **"Student Login"**
2. Use your existing username/password
3. Or create a new account

### Step 2: Start a Study Session
1. Go to the **"📚 Study Session"** tab
2. Click **"🎯 Configure & Start"**
3. Set duration (try 0.1 hours = 6 minutes for testing)
4. **IMPORTANT**: Enable "Enable Camera Monitoring" checkbox
5. Click **"Start Session"**

### Step 3: Test Detection

**The system will now detect:**

#### ✅ Study Apps (High Score)
- Word, Excel, PowerPoint
- PDF readers (Adobe, Foxit)
- Code editors (VS Code, PyCharm)
- Notion, Evernote, OneNote
- **Browser with study sites** (GitHub, StackOverflow, Wikipedia)

#### ❌ Distraction Apps (Low Score, Warnings)
- **YouTube** (especially entertainment/shorts)
- **Netflix, Prime Video**
- **Games** (Steam, any game)
- **Social Media** (Discord, WhatsApp, Telegram)
- **Spotify, VLC** (entertainment)

### Step 4: Watch for Warnings

**What will happen:**
1. **First 60 seconds**: System observes (no warnings yet)
2. **If you open YouTube/game**: Score drops below 40
3. **After 60 seconds of distraction**: First gentle warning appears
4. **After 3 minutes of distraction**: Stronger warning
5. **If you return to study**: Warnings stop, score increases

---

## 📊 What You'll See

### In the Monitor Window:

```
✅ Session Active
Focus Score: 85%          ← Real-time score
App: chrome.exe | Actively studying  ← What you're doing
⚠️ Warnings: 0            ← Warning counter
```

### Score Meanings:

- **80-100**: ✅ Focused - No warnings
- **60-79**: 💭 Mild drift - Monitored silently
- **40-59**: ⚠️ Distracted - Warning after 60s
- **0-39**: 🚨 High distraction - Warning after 3 min

---

## 🔬 Real Test Scenarios

### Scenario 1: Study → YouTube → Study
1. Start session
2. Open Word/PDF (score: 90+)
3. Switch to YouTube (score drops to 20-30)
4. Wait 60 seconds → **Warning appears!**
5. Close YouTube, return to Word
6. Score recovers to 90+
7. No more warnings (forgiveness system)

### Scenario 2: Gaming Detection
1. Start session
2. Open any game
3. Score drops immediately to 10-20
4. After 60 seconds → **"Distraction app detected" warning**
5. Warnings continue until you close the game

### Scenario 3: Browser Behavior
1. Open Chrome/Firefox
2. If on Wikipedia/GitHub → Score: 85-90 (study)
3. If on YouTube entertainment → Score: 20-30 (distraction)
4. System detects the difference!

---

## 🐛 If Something Doesn't Work

### No warnings appearing?
**Check:**
- Is camera enabled in session start?
- Are you using a distraction app for 60+ seconds continuously?
- Check terminal for any errors

### App not detected?
**Solution:**
1. Stop session
2. Open `focus_config.py`
3. Add your app to `STUDY_APPS` or `DISTRACTION_APPS`:
```python
FocusConfig.STUDY_APPS.add('myapp.exe')
```

### Too many warnings?
**Solution:**
Edit `focus_config.py`:
```python
FocusConfig.SUSTAINED_DISTRACTION_DURATION = 120  # Slower warnings
FocusConfig.WARNING_COOLDOWN = 120  # More time between warnings
```

### Not enough warnings?
**Solution:**
Edit `focus_config.py`:
```python
FocusConfig.SUSTAINED_DISTRACTION_DURATION = 30  # Faster warnings
FocusConfig.THRESHOLD_DISTRACTED = 50  # Higher threshold
```

---

## ✨ Key Features Now Working

1. ✅ **Desktop app detection** (50% of score)
   - Detects Chrome, Firefox, games, etc.
   
2. ✅ **Typing/mouse pattern analysis** (25% of score)
   - Distinguishes study typing from gaming
   - Detects fast scrolling (YouTube shorts/reels)

3. ✅ **Camera eye tracking** (15% of score)
   - Checks if you're looking at screen

4. ✅ **Head posture** (10% of score)
   - Detects if you're looking down (phone)

5. ✅ **Smart warnings**
   - No instant warnings (60-second sustained check)
   - Warning cooldown (won't spam)
   - Forgiveness system (warnings decay)

6. ✅ **Silent when focused**
   - Score above 80 → Complete silence
   - No interruptions for good behavior

---

## 📈 After Testing

Check your session results:
1. Complete the session
2. See detailed stats:
   - Average focus score
   - Time focused vs distracted
   - Warning count
   - Peak focus achieved

Parent dashboard will also show:
- Focus score trends
- Improvement over time
- **Privacy-preserved** (no screenshots or detailed logs)

---

## 🎉 You're All Set!

The system is now detecting:
- ✅ YouTube watching
- ✅ Gaming
- ✅ Social media
- ✅ Any distraction app
- ✅ Entertainment vs study browsing

**Try it now!** Start a 6-minute test session and switch between apps to see it work!