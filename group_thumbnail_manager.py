import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import shutil

class GroupThumbnailManager:
    def __init__(self, thumbnails_dir='group_thumbnails'):
        self.thumbnails_dir = thumbnails_dir
        if not os.path.exists(thumbnails_dir):
            os.makedirs(thumbnails_dir)
    
    def upload_thumbnail(self, group_id):
        """Open file dialog to upload thumbnail"""
        file_path = filedialog.askopenfilename(
            title="Select Group Photo",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")]
        )
        
        if file_path:
            ext = os.path.splitext(file_path)[1]
            new_path = os.path.join(self.thumbnails_dir, f"group_{group_id}{ext}")
            shutil.copy(file_path, new_path)
            return new_path
        return None
    
    def get_thumbnail_image(self, thumbnail_path, size=(80, 80)):
        """Load and resize thumbnail for display"""
        if thumbnail_path and os.path.exists(thumbnail_path):
            try:
                img = Image.open(thumbnail_path)
                img = img.resize(size, Image.Resampling.LANCZOS)
                return ImageTk.PhotoImage(img)
            except:
                return None
        return None
    
    def create_thumbnail_widget(self, parent, thumbnail_path, size=(80, 80)):
        """Create a label widget with thumbnail"""
        photo = self.get_thumbnail_image(thumbnail_path, size)
        if photo:
            label = tk.Label(parent, image=photo, bg=parent['bg'])
            label.image = photo  # Keep reference
            return label
        else:
            # Default placeholder
            label = tk.Label(parent, text="📷", font=("Arial", 40), bg=parent['bg'])
            return label
