f = open('student_gui.py', 'r', encoding='utf-8')
lines = f.readlines()
f.close()

# Find __init__ method and add colors early
for i, line in enumerate(lines):
    if 'self.root.geometry' in line:
        # Add default colors right after geometry
        default_colors = """
        # Default colors (before any UI creation)
        self.colors = {
            'primary': '#6366F1',
            'secondary': '#8B5CF6',
            'success': '#10B981',
            'warning': '#F59E0B',
            'danger': '#EF4444',
            'bg_light': '#F9FAFB',
            'bg_card': '#FFFFFF',
            'text_primary': '#111827',
            'text_secondary': '#6B7280',
            'border': '#E5E7EB',
            'success_light': '#D1FAE5',
            'primary_dark': '#4F46E5'
        }

"""
        lines.insert(i + 1, default_colors)
        break

f = open('student_gui.py', 'w', encoding='utf-8')
f.writelines(lines)
f.close()

print('Default colors added at start of __init__')
