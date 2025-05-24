"""
Movie Review App Configuration
"""
import os

class Config:
    # Paths
    DATA_DIR = "data"
    USERS_FILE = os.path.join(DATA_DIR, "users.json")
    MOVIES_FILE = os.path.join(DATA_DIR, "movies.json")
    
    # Window settings
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 800
    
    # Colors
    COLORS = {
        'bg_primary': '#1a1a2e',
        'bg_secondary': '#16213e', 
        'bg_tertiary': '#0f3460',
        'accent': '#e94560',
        'accent_hover': '#c73650',
        'text_primary': '#fff',
        'text_secondary': '#f5c518'
    }
    
    # Fonts
    FONTS = {
        'title': ('Arial', 24, 'bold'),
        'subtitle': ('Arial', 12),
        'normal': ('Arial', 10),
        'button': ('Arial', 11, 'bold'),
        'entry': ('Arial', 12)
    }