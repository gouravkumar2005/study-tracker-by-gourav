"""Validate that theme manager has all required colors"""
from theme_manager import ThemeManager

tm = ThemeManager()
light_theme = tm.get_theme('light')

required_colors = [
    'primary',
    'primary_dark',
    'secondary',
    'success',
    'success_light',
    'warning',
    'danger',
    'bg_light',
    'bg_card',
    'text_primary',
    'text_secondary',
    'border'
]

print("Checking if all required colors are present in light theme...")
all_present = True
for color in required_colors:
    if color in light_theme:
        print(f"  [OK] {color}: {light_theme[color]}")
    else:
        print(f"  [MISSING] {color}")
        all_present = False

if all_present:
    print("\n[SUCCESS] All required colors are present.")
    print("The login page should now display properly with Login and Create Account buttons visible.")
else:
    print("\n[FAILED] Some colors are missing.")
