"""
Quick Test Script for Group Thumbnail Feature
Run this to test if thumbnail feature is working
"""

import os
from group_thumbnail_manager import GroupThumbnailManager
from study_groups import StudyGroupsSystem

def test_thumbnail_feature():
    print("🧪 Testing Group Thumbnail Feature...")
    print("-" * 50)
    
    # Test 1: Check if thumbnail manager initializes
    print("\n1. Testing Thumbnail Manager Initialization...")
    try:
        tm = GroupThumbnailManager()
        print("   ✅ Thumbnail Manager initialized successfully")
        print(f"   📁 Thumbnails directory: {tm.thumbnails_dir}")
        print(f"   📂 Directory exists: {os.path.exists(tm.thumbnails_dir)}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # Test 2: Check if study groups system has thumbnail support
    print("\n2. Testing Study Groups System...")
    try:
        sg = StudyGroupsSystem()
        print("   ✅ Study Groups System initialized")
        
        # Check if update_group_thumbnail method exists
        if hasattr(sg, 'update_group_thumbnail'):
            print("   ✅ update_group_thumbnail method exists")
        else:
            print("   ❌ update_group_thumbnail method NOT found")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # Test 3: Check database schema
    print("\n3. Testing Database Schema...")
    try:
        import sqlite3
        conn = sqlite3.connect('study_tracker.db')
        c = conn.cursor()
        
        # Check if thumbnail_path column exists
        c.execute("PRAGMA table_info(study_groups)")
        columns = c.fetchall()
        column_names = [col[1] for col in columns]
        
        if 'thumbnail_path' in column_names:
            print("   ✅ thumbnail_path column exists in database")
        else:
            print("   ❌ thumbnail_path column NOT found")
            print("   💡 Run the app once to create the column")
        
        conn.close()
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 4: Check if placeholder works
    print("\n4. Testing Placeholder Display...")
    try:
        widget = tm.create_thumbnail_widget(None, None, size=(80, 80))
        print("   ✅ Placeholder widget created successfully")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("✨ Test Complete!")
    print("\n📝 Next Steps:")
    print("   1. Run main.py")
    print("   2. Login as student")
    print("   3. Go to Study Groups")
    print("   4. Click 'Create Group'")
    print("   5. Try uploading a group photo!")
    print("=" * 50)

if __name__ == "__main__":
    test_thumbnail_feature()
