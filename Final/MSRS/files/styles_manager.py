"""
Style Manager for Movie Review App
"""
from tkinter import ttk
from config import Config

class StyleManager:
    def __init__(self):
        self.colors = Config.COLORS
        self.fonts = Config.FONTS
        
    def setup_styles(self):
        """Configure modern dark theme styles"""
        style = ttk.Style()

        # Notebook (tab) style
        style.theme_use('clam')
        style.configure('TNotebook', 
                       background=self.colors['bg_primary'], 
                       borderwidth=0)
        
        style.configure('TNotebook.Tab',
                        background=self.colors['bg_tertiary'],
                        foreground=self.colors['text_primary'],
                        padding=[20, 10],
                        font=self.fonts['button'])
        
        style.map('TNotebook.Tab',
                  background=[('selected', self.colors['accent']), 
                            ('active', self.colors['bg_secondary'])],
                  foreground=[('selected', self.colors['text_primary']), 
                            ('active', self.colors['text_primary']), 
                            ('!selected', self.colors['text_primary'])])

        # Button styles
        style.configure('Accent.TButton',
                        background=self.colors['accent'],
                        foreground=self.colors['text_primary'],
                        font=self.fonts['button'],
                        borderwidth=0)
        
        style.map('Accent.TButton',
                  background=[('active', self.colors['accent_hover']), 
                            ('pressed', self.colors['accent_hover'])],
                  foreground=[('active', self.colors['text_primary']), 
                            ('pressed', self.colors['text_primary'])])

        style.configure('Secondary.TButton',
                        background=self.colors['bg_tertiary'],
                        foreground=self.colors['text_primary'],
                        font=self.fonts['normal'],
                        borderwidth=0)
        
        style.map('Secondary.TButton',
                  background=[('active', '#1e5f8b'), ('pressed', '#1e5f8b')],
                  foreground=[('active', self.colors['text_primary']), 
                            ('pressed', self.colors['text_primary'])])

        # Entry styles
        style.configure('Modern.TEntry',
                        fieldbackground=self.colors['bg_secondary'],
                        foreground=self.colors['text_primary'],
                        borderwidth=1,
                        insertcolor=self.colors['text_primary'])

        # Label styles
        style.configure('Title.TLabel',
                        background=self.colors['bg_primary'],
                        foreground=self.colors['accent'],
                        font=self.fonts['title'])

        style.configure('Subtitle.TLabel',
                        background=self.colors['bg_primary'],
                        foreground=self.colors['text_primary'],
                        font=self.fonts['subtitle'])

        style.configure('Modern.TLabel',
                        background=self.colors['bg_primary'],
                        foreground=self.colors['text_primary'],
                        font=self.fonts['normal'])
        
        style.configure('Modern2.TLabel', 
                        background=self.colors['bg_secondary'], 
                        foreground=self.colors['text_primary'], 
                        font=self.fonts['normal'])
        # Radiobutton style
        style.configure('Modern.TRadiobutton',
                        background=self.colors['bg_primary'],
                        foreground=self.colors['accent'],
                        font=self.fonts['normal'],
                        indicatorcolor=self.colors['accent'],
                        indicatordiameter=12,
                        indicatormargin=6,
                        focuscolor=self.colors['accent'])
        style.map('Modern.TRadiobutton',
                  background=[('active', self.colors['bg_secondary'])],
                  foreground=[('active', self.colors['accent'])])