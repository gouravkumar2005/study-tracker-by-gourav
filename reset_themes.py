import sqlite3

# Reset theme prices to 0
conn = sqlite3.connect('study_tracker.db')
c = conn.cursor()

# Check if rewards table exists
c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='rewards'")
if c.fetchone():
    # Update all theme rewards to cost 0
    c.execute("UPDATE rewards SET cost = 0 WHERE type = 'theme'")
    print("Themes reset to 0 coins!")
else:
    print("No rewards table - themes already free!")

conn.commit()
conn.close()

print("All themes are now FREE!")
print("Restart the app.")
