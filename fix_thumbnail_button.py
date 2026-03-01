# Quick Fix for Thumbnail Upload Button
# Run this to fix the corrupted emoji in create_group method

import re

# Read the file
with open('student_gui.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the corrupted section
# Looking for the thumbnail section in create_group method
old_pattern = r'thumbnail_label = tk\.Label\(thumbnail_frame, text="[^"]*", font=\("Arial", 40\),'
new_code = 'thumbnail_label = tk.Label(thumbnail_frame, text="[Photo]", font=("Arial", 20),'

content = re.sub(old_pattern, new_code, content)

# Also fix the button text
old_button = r'tk\.Button\(thumbnail_frame, text="[^"]*Upload Group Photo"'
new_button = 'tk.Button(thumbnail_frame, text="Upload Group Photo"'

content = re.sub(old_button, new_button, content)

# Fix the uploaded indicator
old_uploaded = r'thumbnail_label\.config\(text="[^"]*"\)'
new_uploaded = 'thumbnail_label.config(text="[Uploaded]")'

content = re.sub(old_uploaded, new_uploaded, content)

# Write back
with open('student_gui.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed! Now run main.py and try creating a group.")
print("You should see 'Upload Group Photo' button.")
