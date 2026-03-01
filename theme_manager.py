import json
import os

class ThemeManager:
    def __init__(self):
        self.themes_file = 'themes.json'
        self.current_theme = 'light'
        self.themes = {
            'light': {
                'primary': '#6366F1',
                'primary_dark': '#4F46E5',
                'secondary': '#8B5CF6',
                'success': '#10B981',
                'success_light': '#D1FAE5',
                'warning': '#F59E0B',
                'danger': '#EF4444',
                'bg_light': '#F9FAFB',
                'bg_card': '#FFFFFF',
                'text_primary': '#111827',
                'text_secondary': '#6B7280',
                'border': '#E5E7EB'
            },
            'dark': {
                'primary': '#818CF8',
                'primary_dark': '#6366F1',
                'secondary': '#A78BFA',
                'success': '#34D399',
                'success_light': '#064E3B',
                'warning': '#FBBF24',
                'danger': '#F87171',
                'bg_light': '#1F2937',
                'bg_card': '#111827',
                'text_primary': '#F9FAFB',
                'text_secondary': '#9CA3AF',
                'border': '#374151'
            },
            'ocean': {
                'primary': '#0EA5E9',
                'primary_dark': '#0284C7',
                'secondary': '#06B6D4',
                'success': '#10B981',
                'success_light': '#D1FAE5',
                'warning': '#F59E0B',
                'danger': '#EF4444',
                'bg_light': '#E0F2FE',
                'bg_card': '#FFFFFF',
                'text_primary': '#0C4A6E',
                'text_secondary': '#0369A1',
                'border': '#7DD3FC'
            },
            'forest': {
                'primary': '#059669',
                'primary_dark': '#047857',
                'secondary': '#10B981',
                'success': '#34D399',
                'success_light': '#D1FAE5',
                'warning': '#F59E0B',
                'danger': '#EF4444',
                'bg_light': '#D1FAE5',
                'bg_card': '#FFFFFF',
                'text_primary': '#064E3B',
                'text_secondary': '#047857',
                'border': '#6EE7B7'
            },
            'sunset': {
                'primary': '#F59E0B',
                'primary_dark': '#D97706',
                'secondary': '#EF4444',
                'success': '#10B981',
                'success_light': '#D1FAE5',
                'warning': '#FBBF24',
                'danger': '#DC2626',
                'bg_light': '#FEF3C7',
                'bg_card': '#FFFFFF',
                'text_primary': '#78350F',
                'text_secondary': '#92400E',
                'border': '#FCD34D'
            },
            'purple': {
                'primary': '#9333EA',
                'primary_dark': '#7E22CE',
                'secondary': '#A855F7',
                'success': '#10B981',
                'success_light': '#D1FAE5',
                'warning': '#F59E0B',
                'danger': '#EF4444',
                'bg_light': '#F3E8FF',
                'bg_card': '#FFFFFF',
                'text_primary': '#581C87',
                'text_secondary': '#7E22CE',
                'border': '#D8B4FE'
            }
        }
        self._load_user_themes()
    
    def _load_user_themes(self):
        """Load user custom themes"""
        if os.path.exists(self.themes_file):
            try:
                with open(self.themes_file, 'r') as f:
                    user_themes = json.load(f)
                    self.themes.update(user_themes)
            except:
                pass
    
    def get_theme(self, theme_name='light'):
        """Get theme colors"""
        return self.themes.get(theme_name, self.themes['light'])
    
    def set_theme(self, theme_name):
        """Set current theme"""
        if theme_name in self.themes:
            self.current_theme = theme_name
            return True
        return False
    
    def get_available_themes(self):
        """Get list of available themes"""
        return list(self.themes.keys())
    
    def create_custom_theme(self, name, colors):
        """Create custom theme"""
        self.themes[name] = colors
        self._save_user_themes()
        return True
    
    def _save_user_themes(self):
        """Save user themes to file"""
        user_themes = {k: v for k, v in self.themes.items() 
                      if k not in ['light', 'dark', 'ocean', 'forest', 'sunset', 'purple']}
        with open(self.themes_file, 'w') as f:
            json.dump(user_themes, f, indent=2)
