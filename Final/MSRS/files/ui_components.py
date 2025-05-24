"""
UI Components for Movie Review App
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from config import Config

class UIComponents:
    def __init__(self, parent):
        self.parent = parent
        self.colors = Config.COLORS
        
    def create_header(self, container):
        """Create application header"""
        header_frame = tk.Frame(container, bg=self.colors['bg_primary'])
        header_frame.pack(fill='x', pady=(0, 20))
        
        title_label = ttk.Label(header_frame, 
                               text="🎬 Movie & TV Series Review System", 
                               style='Title.TLabel')
        title_label.pack()
        
        return header_frame
    
    def create_user_status_frame(self, container):
        """Create user status display frame"""
        user_frame = tk.Frame(container, bg=self.colors['bg_primary'])
        user_frame.pack(pady=(10, 0))
        
        user_label = ttk.Label(user_frame, text="Not logged in", 
                              style='Subtitle.TLabel')
        user_label.pack(side='left')
        
        auth_button = ttk.Button(user_frame, text="Login", 
                                style='Accent.TButton')
        auth_button.pack(side='right', padx=(10, 0))
        
        return user_frame, user_label, auth_button
    
    def create_search_frame(self, container, search_var, callback):
        """Create search frame with entry"""
        search_frame = tk.Frame(container, bg=self.colors['bg_secondary'])
        search_frame.pack(fill='x', padx=15, pady=15)
        
        ttk.Label(search_frame, text="Search Movies:", 
                 style='Modern2.TLabel').pack(side='left')
        
        search_entry = ttk.Entry(search_frame, textvariable=search_var,
                               style='Modern.TEntry', font=Config.FONTS['normal'])
        search_entry.pack(side='left', padx=(10, 0), fill='x', expand=True)
        search_entry.bind('<KeyRelease>', callback)
        
        return search_frame
    
    def create_movies_listbox(self, container):
        """Create movies listbox with scrollbar"""
        listbox_frame = tk.Frame(container, bg=self.colors['bg_secondary'])
        listbox_frame.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        
        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side='right', fill='y')
        
        movies_listbox = tk.Listbox(listbox_frame, 
                                   bg=self.colors['bg_tertiary'], 
                                   fg=self.colors['text_primary'],
                                   selectbackground=self.colors['accent'],
                                   font=Config.FONTS['normal'],
                                   yscrollcommand=scrollbar.set)
        movies_listbox.pack(fill='both', expand=True)
        scrollbar.config(command=movies_listbox.yview)
        
        return movies_listbox
    
    def create_button_frame(self, container, buttons):
        """Create frame with buttons"""
        button_frame = tk.Frame(container, bg=self.colors['bg_secondary'])
        button_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        created_buttons = []
        for i, (text, command, style) in enumerate(buttons):
            btn = ttk.Button(button_frame, text=text, 
                           command=command, style=style)
            if i == 0:
                btn.pack(side='left')
            else:
                btn.pack(side='left', padx=(10, 0))
            created_buttons.append(btn)
        
        return button_frame, created_buttons
    
    def create_scrolled_text(self, container, **kwargs):
        """Create scrolled text widget"""
        default_kwargs = {
            'bg': self.colors['bg_tertiary'],
            'fg': self.colors['text_primary'],
            'font': Config.FONTS['normal'],
            'wrap': 'word',
            'state': 'disabled'
        }
        default_kwargs.update(kwargs)
        
        text_widget = scrolledtext.ScrolledText(container, **default_kwargs)
        return text_widget
    
    def create_login_dialog(self, parent, title="Login / Register"):
        """Create login/register dialog"""
        dialog = tk.Toplevel(parent)
        dialog.title(title)
        dialog.geometry("400x500")
        dialog.configure(bg=self.colors['bg_primary'])
        dialog.transient(parent)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = parent.winfo_rootx() + 400
        y = parent.winfo_rooty() + 150
        dialog.geometry(f"400x500+{x}+{y}")
        
        return dialog
    
    def create_rating_dialog(self, parent, movie_title):
        """Create rating/review dialog"""
        dialog = tk.Toplevel(parent)
        dialog.title(f"Rate & Review - {movie_title}")
        dialog.geometry("600x600")
        dialog.configure(bg=self.colors['bg_primary'])
        dialog.transient(parent)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        w, h = 600, 600
        x = (dialog.winfo_screenwidth() // 2) - (w // 2)
        y = (dialog.winfo_screenheight() // 2) - (h // 2)
        dialog.geometry(f"{w}x{h}+{x}+{y}")
        
        return dialog
    
    def create_movie_details_window(self, parent, movie_title):
        """Create movie details window"""
        details_window = tk.Toplevel(parent)
        details_window.withdraw()  # Hide initially
        
        details_window.title(f"Details - {movie_title}")
        details_window.configure(bg=self.colors['bg_primary'])
        details_window.transient(parent)
        details_window.grab_set()
        
        # Set geometry and center
        w, h = 800, 600
        details_window.geometry(f"{w}x{h}")
        details_window.update_idletasks()
        x = (details_window.winfo_screenwidth() // 2) - (w // 2)
        y = (details_window.winfo_screenheight() // 2) - (h // 2)
        details_window.geometry(f"{w}x{h}+{x}+{y}")
        
        details_window.deiconify()  # Show after all settings
        return details_window
    
    def bind_mousewheel(self, widget, target_canvas):
        """Bind mousewheel events to canvas"""
        def _on_mousewheel(event):
            if event.delta:
                target_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            else:  # For Linux systems
                if event.num == 4:
                    target_canvas.yview_scroll(-1, "units")
                elif event.num == 5:
                    target_canvas.yview_scroll(1, "units")
        
        widget.bind_all("<MouseWheel>", _on_mousewheel)
        widget.bind_all("<Button-4>", _on_mousewheel)
        widget.bind_all("<Button-5>", _on_mousewheel)