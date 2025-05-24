"""
Main Application File for Movie Review System
"""
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from config import Config
from data_manager import DataManager
from styles_manager import StyleManager
from ui_components import UIComponents
from ai_analyzer import AIAnalyzer
from auth_manager import AuthManager

class MovieReviewApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie & TV Series Review System")
        self.root.geometry(f"{Config.WINDOW_WIDTH}x{Config.WINDOW_HEIGHT}")
        self.root.configure(bg=Config.COLORS['bg_primary'])
        
        # Initialize managers
        self.data_manager = DataManager()
        self.style_manager = StyleManager()
        self.ui = UIComponents(self.root)
        self.ai_analyzer = AIAnalyzer()
        self.auth_manager = AuthManager()
        
        # Configure styles
        self.style_manager.setup_styles()
        
        # Create main interface
        self.create_main_interface()
        
        # Center the window
        self.center_window()
        
    def center_window(self):
        """Center the main window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
    def create_main_interface(self):
        """Create the main application interface"""
        # Main container
        main_frame = tk.Frame(self.root, bg=Config.COLORS['bg_primary'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header
        header_frame = self.ui.create_header(main_frame)
        
        # User status frame
        self.user_frame, self.user_label, self.auth_button = self.ui.create_user_status_frame(header_frame)
        self.auth_button.config(command=self.toggle_auth)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill='both', expand=True)
        
        # Create tabs
        self.create_movies_tab()
        self.create_reviews_tab()
        self.create_recommendations_tab()
        
        # Update user status
        self.update_user_status()
        
    def create_movies_tab(self):
        """Create movies listing and details tab"""
        movies_frame = tk.Frame(self.notebook, bg=Config.COLORS['bg_primary'])
        self.notebook.add(movies_frame, text='Movies & TV Series')
        
        # Movies list frame
        list_frame = tk.Frame(movies_frame, bg=Config.COLORS['bg_secondary'], relief='raised', bd=1)
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Search frame
        self.search_var = tk.StringVar()
        search_frame = self.ui.create_search_frame(list_frame, self.search_var, self.filter_movies)
        
        # Movies listbox with scrollbar
        self.movies_listbox = self.ui.create_movies_listbox(list_frame)
        
        # Button frame
        buttons = [
            ("View Details", self.show_movie_details, 'Secondary.TButton'),
            ("Rate & Review", self.rate_movie, 'Accent.TButton')
        ]
        button_frame, _ = self.ui.create_button_frame(list_frame, buttons)
        
        # Load movies
        self.load_movies_list()
        
    def create_reviews_tab(self):
        """Create user reviews tab"""
        reviews_frame = tk.Frame(self.notebook, bg=Config.COLORS['bg_primary'])
        self.notebook.add(reviews_frame, text='My Reviews')
        
        # Reviews container
        self.reviews_container = tk.Frame(reviews_frame, bg=Config.COLORS['bg_secondary'], relief='raised', bd=1)
        self.reviews_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Reviews text area
        self.reviews_text = self.ui.create_scrolled_text(self.reviews_container)
        self.reviews_text.pack(fill='both', expand=True, padx=15, pady=15)
        self.reviews_text.tag_configure('movie_title', font=('Arial', 16, 'bold'), 
                                      foreground=Config.COLORS['accent'])
        
    def create_recommendations_tab(self):
        """Create recommendations tab"""
        rec_frame = tk.Frame(self.notebook, bg=Config.COLORS['bg_primary'])
        self.notebook.add(rec_frame, text='Recommendations')
        
        # Recommendations container
        rec_container = tk.Frame(rec_frame, bg=Config.COLORS['bg_secondary'], relief='raised', bd=1)
        rec_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Get recommendations button
        button_frame = tk.Frame(rec_container, bg=Config.COLORS['bg_secondary'])
        button_frame.pack(fill='x', padx=15, pady=15)
        
        ttk.Button(button_frame, text="Get AI Recommendations", 
                  command=self.get_recommendations,
                  style='Accent.TButton').pack()
        
        # Recommendations text area
        self.rec_text = self.ui.create_scrolled_text(rec_container)
        self.rec_text.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        
    def toggle_auth(self):
        """Toggle between login and logout"""
        if self.auth_manager.is_logged_in():
            self.auth_manager.logout()
            self.update_user_status()
        else:
            self.show_login_dialog()
            
    def update_user_status(self):
        """Update user status display"""
        if self.auth_manager.is_logged_in():
            self.user_label.config(text=f"Logged in as: {self.auth_manager.get_current_user()}")
            self.auth_button.config(text="Logout")
            self.load_user_reviews()
        else:
            self.user_label.config(text="Not logged in")
            self.auth_button.config(text="Login")
            self.clear_reviews_tab()
            
    def clear_reviews_tab(self):
        """Clear the reviews tab when user logs out"""
        self.reviews_text.config(state='normal')
        self.reviews_text.delete(1.0, tk.END)
        self.reviews_text.insert(tk.END, "Please login to view your reviews.")
        self.reviews_text.config(state='disabled')
        
    def load_movies_list(self):
        """Load movies into the listbox"""
        movies = self.data_manager.load_movies()
        self.movies_listbox.delete(0, tk.END)
        
        for movie_id, movie in movies.items():
            title = f"{movie['Series_Title']} ({movie['Released_Year']}) - IMDB: {movie.get('IMDB_Rating', 'N/A')}"
            self.movies_listbox.insert(tk.END, title)
    
    def filter_movies(self, event=None):
        """Filter movies based on search term"""
        search_term = self.search_var.get().lower()
        movies = self.data_manager.load_movies()
        
        self.movies_listbox.delete(0, tk.END)
        
        for movie_id, movie in movies.items():
            title = movie['Series_Title'].lower()
            if search_term in title:
                display_title = f"{movie['Series_Title']} ({movie['Released_Year']}) - IMDB: {movie.get('IMDB_Rating', 'N/A')}"
                self.movies_listbox.insert(tk.END, display_title)
    
    def show_login_dialog(self):
        """Show login/register dialog"""
        dialog = self.ui.create_login_dialog(self.root)
        
        # Notebook for login/register
        auth_notebook = ttk.Notebook(dialog)
        auth_notebook.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Login tab
        login_frame = tk.Frame(auth_notebook, bg=Config.COLORS['bg_primary'])
        auth_notebook.add(login_frame, text='Login')
        
        ttk.Label(login_frame, text="Username:", style='Modern.TLabel').pack(pady=(20, 5))
        login_username = ttk.Entry(login_frame, style='Modern.TEntry', font=Config.FONTS['entry'])
        login_username.pack(pady=(0, 10), padx=20, fill='x')
        
        ttk.Label(login_frame, text="Password:", style='Modern.TLabel').pack(pady=(0, 5))
        login_password = ttk.Entry(login_frame, show="*", style='Modern.TEntry', font=Config.FONTS['entry'])
        login_password.pack(pady=(0, 20), padx=20, fill='x')
        
        ttk.Button(login_frame, text="Login", 
                  command=lambda: self.handle_login(login_username.get(), login_password.get(), dialog),
                  style='Accent.TButton').pack(pady=10)
        
        # Register tab
        register_frame = tk.Frame(auth_notebook, bg=Config.COLORS['bg_primary'])
        auth_notebook.add(register_frame, text='Register')
        
        ttk.Label(register_frame, text="Username:", style='Modern.TLabel').pack(pady=(20, 5))
        reg_username = ttk.Entry(register_frame, style='Modern.TEntry', font=Config.FONTS['entry'])
        reg_username.pack(pady=(0, 10), padx=20, fill='x')
        
        ttk.Label(register_frame, text="Password:", style='Modern.TLabel').pack(pady=(0, 5))
        reg_password = ttk.Entry(register_frame, show="*", style='Modern.TEntry', font=Config.FONTS['entry'])
        reg_password.pack(pady=(0, 10), padx=20, fill='x')
        
        ttk.Label(register_frame, 
                 text="Requirements: 5+ chars, 8+ chars password with digit and letter", 
                 style='Modern.TLabel', wraplength=300).pack(pady=(0, 20))
        
        ttk.Button(register_frame, text="Register", 
                  command=lambda: self.handle_register(reg_username.get(), reg_password.get(), dialog),
                  style='Accent.TButton').pack(pady=10)
    
    def handle_login(self, username, password, dialog):
        """Handle login attempt"""
        success, message = self.auth_manager.login(username, password)
        if success:
            dialog.destroy()
            self.update_user_status()
        else:
            tk.messagebox.showerror("Error", message)
    
    def handle_register(self, username, password, dialog):
        """Handle registration attempt"""
        success, message = self.auth_manager.register(username, password)
        if success:
            dialog.destroy()
            tk.messagebox.showinfo("Success", message)
        else:
            tk.messagebox.showerror("Error", message)
    
    def show_movie_details(self):
        """Show detailed movie information"""
        selection = self.movies_listbox.curselection()
        if not selection:
            tk.messagebox.showwarning("Warning", "Please select a movie first")
            return

        movies = self.data_manager.load_movies()
        movie_list = list(movies.items())
        movie_id, movie_data = movie_list[selection[0]]

        details_window = self.ui.create_movie_details_window(self.root, movie_data['Series_Title'])
        
        # Create scrollable frame
        canvas = tk.Canvas(details_window, bg=Config.COLORS['bg_primary'])
        scrollbar = ttk.Scrollbar(details_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=Config.COLORS['bg_primary'])
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Movie details
        title_label = tk.Label(
            scrollable_frame,
            text=f"{movie_data['Series_Title']} ({movie_data['Released_Year']})",
            bg=Config.COLORS['bg_primary'],
            fg=Config.COLORS['accent'],
            font=('Arial', 28, 'bold'),
            anchor='w',
            justify='left',
            wraplength=750
        )
        title_label.pack(padx=20, pady=(20, 10), anchor='w')

        details_text = f"""
Certificate: {movie_data['Certificate']}
Runtime: {movie_data['Runtime']} minutes
Genre: {movie_data['Genre']}
IMDB Rating: {movie_data.get('IMDB_Rating', 'N/A')}
Metascore: {movie_data['Meta_score']}
Director: {movie_data['Director']}
Stars: {movie_data['Star1']}, {movie_data['Star2']}, {movie_data['Star3']}, {movie_data['Star4']}
Votes: {movie_data['No_of_Votes']}
Gross: ${movie_data['Gross']} million

Overview:
{movie_data['Overview']}
"""

        details_label = tk.Label(scrollable_frame, text=details_text, 
                               bg=Config.COLORS['bg_primary'], fg=Config.COLORS['text_primary'], 
                               font=('Arial', 10), justify='left', wraplength=750)
        details_label.pack(padx=20, pady=20)
        
        if movie_data['reviews']:
            avg_rating = sum([review['rating'] for review in movie_data['reviews']]) / len(movie_data['reviews'])
            avg_label = tk.Label(scrollable_frame, text=f"Average Rating: {avg_rating:.1f}/10", 
                                 bg=Config.COLORS['bg_primary'], fg=Config.COLORS['text_secondary'], 
                                 font=('Arial', 12, 'bold'))
            avg_label.pack(padx=20, pady=(0, 10), anchor='w')

            reviews_box = scrolledtext.ScrolledText(
                scrollable_frame, bg='#232323', fg='white', font=('Arial', 10), height=12, wrap='word'
            )
            reviews_box.pack(fill='both', expand=True, padx=20, pady=(0, 20))
            reviews_box.tag_configure('username', font=('Arial', 12, 'bold'), foreground=Config.COLORS['accent'])
            reviews_box.tag_configure('reviewinfo', font=('Arial', 10), foreground=Config.COLORS['text_secondary'])
            reviews_box.tag_configure('reviewtext', font=('Arial', 10), foreground='white')

            for review in movie_data['reviews']:
                sentiment, score = self.ai_analyzer.analyze_sentiment(review['content'])
                reviews_box.insert(tk.END, f"{review['username']}", 'username')
                reviews_box.insert(tk.END, f" | {review['date']} | {review['rating']}/10\n", 'reviewinfo')
                reviews_box.insert(tk.END, f"Sentiment: {sentiment} ({score:.2f})\n", 'reviewinfo')
                reviews_box.insert(tk.END, f"{review['content']}\n", 'reviewtext')
                reviews_box.insert(tk.END, "-" * 50 + "\n\n", 'reviewinfo')
            reviews_box.config(state='disabled')
        else:
            no_reviews = tk.Label(scrollable_frame, text="No reviews yet.", 
                                 bg=Config.COLORS['bg_primary'], fg=Config.COLORS['text_primary'], 
                                 font=('Arial', 10))
            no_reviews.pack(padx=20, pady=20, anchor='w')
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.ui.bind_mousewheel(details_window, canvas)
    
    def rate_movie(self):
        """Rate and review a movie"""
        if not self.auth_manager.is_logged_in():
            tk.messagebox.showwarning("Warning", "Please login first!")
            return
        
        selection = self.movies_listbox.curselection()
        if not selection:
            tk.messagebox.showwarning("Warning", "Please select a movie first")
            return
        
        movies = self.data_manager.load_movies()
        movie_list = list(movies.items())
        movie_id, movie_data = movie_list[selection[0]]
        
        # Check if already rated
        users = self.data_manager.load_users()
        if movie_id in users[self.auth_manager.get_current_user()]["rated_movies"]:
            result = tk.messagebox.askyesno("Update Review", 
                                       "You've already rated this movie. Do you want to update your review?")
            if not result:
                return
        
        # Create rating dialog
        rating_dialog = self.ui.create_rating_dialog(self.root, movie_data['Series_Title'])
        
        # Title
        ttk.Label(rating_dialog, text=f"Rate & Review", style='Title.TLabel').pack(pady=20)
        ttk.Label(rating_dialog, text=movie_data['Series_Title'], style='Subtitle.TLabel').pack()
        
        # Review text
        ttk.Label(rating_dialog, text="Your Review:", style='Modern.TLabel').pack(pady=(20, 5))
        review_text = scrolledtext.ScrolledText(rating_dialog, 
                                              bg=Config.COLORS['bg_tertiary'], 
                                              fg=Config.COLORS['text_primary'],
                                              font=Config.FONTS['normal'], 
                                              height=8, wrap='word')
        review_text.pack(padx=20, pady=(0, 10), fill='x')
        
        # AI suggestion frame
        ai_frame = tk.Frame(rating_dialog, bg=Config.COLORS['bg_secondary'], relief='raised', bd=1)
        ai_frame.pack(fill='x', padx=20, pady=10)
        
        ai_label = ttk.Label(ai_frame, text="AI Analysis will appear here", 
                           style='Modern2.TLabel')
        ai_label.pack(pady=10)
        
        # Rating scale
        ttk.Label(rating_dialog, text="Your Rating (1-10):", style='Modern.TLabel').pack(pady=(10, 5))
        
        rating_frame = tk.Frame(rating_dialog, bg=Config.COLORS['bg_primary'])
        rating_frame.pack(pady=10)
        
        rating_var = tk.IntVar(value=5)
        for i in range(1, 11):
            ttk.Radiobutton(
                rating_frame, 
                text=str(i), 
                variable=rating_var, 
                value=i, 
                style='Modern.TRadiobutton'
            ).pack(side='left', padx=5)

        # Analyze button
        def analyze_review():
            content = review_text.get("1.0", tk.END).strip()
            if content:
                suggested_rating, sentiment, polarity = self.ai_analyzer.suggest_rating_from_review(content)
                ai_label.config(text=f"AI Analysis: {sentiment} review | Suggested rating: {suggested_rating}/10")
        
        ttk.Button(rating_dialog, text="Analyze Review", 
                  command=analyze_review, style='Secondary.TButton').pack(pady=10)
        
        # Submit button
        def submit_review():
            content = review_text.get("1.0", tk.END).strip()
            if not content:
                tk.messagebox.showerror("Error", "Review cannot be empty!")
                return
            
            rating = rating_var.get()
            
            # Add review through data manager
            self.data_manager.add_review_to_movie(
                movie_id, 
                self.auth_manager.get_current_user(), 
                rating, 
                content
            )
            
            rating_dialog.destroy()
            tk.messagebox.showinfo("Success", "Rating and review submitted successfully!")
            self.load_user_reviews()
        
        ttk.Button(rating_dialog, text="Submit Review", 
                  command=submit_review, style='Accent.TButton').pack(pady=20)
    
    def load_user_reviews(self):
        """Load user's reviews into the reviews tab"""
        if not self.auth_manager.is_logged_in():
            return
        
        user_reviews = self.data_manager.get_user_reviews(self.auth_manager.get_current_user())
        
        self.reviews_text.config(state='normal')
        self.reviews_text.delete(1.0, tk.END)
        
        if not user_reviews:
            self.reviews_text.insert(tk.END, "You haven't reviewed any movies yet.\n\nStart by selecting a movie from the Movies tab and clicking 'Rate & Review'!")
        else:
            self.reviews_text.insert(tk.END, f"Your Reviews ({len(user_reviews)} total)\n\n")
            for title, review in user_reviews:
                sentiment, score = self.ai_analyzer.analyze_sentiment(review['content'])
                self.reviews_text.insert(tk.END, f"{title}\n", 'movie_title')
                review_text = f"{review['date']}\n"
                review_text += f"Rating: {review['rating']}/10\n"
                review_text += f"Sentiment: {sentiment} ({score:.2f})\n"
                review_text += f"Review: {review['content']}\n"
                review_text += "=" * 60 + "\n\n"
                self.reviews_text.insert(tk.END, review_text)
        
        self.reviews_text.config(state='disabled')
    
    def get_recommendations(self):
        """Get AI-based movie recommendations"""
        if not self.auth_manager.is_logged_in():
            tk.messagebox.showwarning("Warning", "Please login first!")
            return
        
        users = self.data_manager.load_users()
        movies = self.data_manager.load_movies()
        rated_movies = users[self.auth_manager.get_current_user()]["rated_movies"]
        
        if not rated_movies:
            self.rec_text.config(state='normal')
            self.rec_text.delete(1.0, tk.END)
            self.rec_text.insert(tk.END, "AI Recommendations\n\n")
            self.rec_text.insert(tk.END, "Please rate some movies first to get personalized recommendations!\n\n")
            self.rec_text.insert(tk.END, "Go to the Movies tab and rate at least 3 movies to get started.")
            self.rec_text.config(state='disabled')
            return
        
        # Get user ratings
        user_ratings = []
        for movie_id in rated_movies:
            for review in movies[movie_id]["reviews"]:
                if review["username"] == self.auth_manager.get_current_user():
                    user_ratings.append({
                        "movie_id": movie_id,
                        "rating": review["rating"]
                    })
        
        recommendations, error = self.ai_analyzer.get_recommendations(user_ratings, movies)
        
        self.rec_text.config(state='normal')
        self.rec_text.delete(1.0, tk.END)
        
        if error:
            self.rec_text.insert(tk.END, "AI Recommendations\n\n")
            self.rec_text.insert(tk.END, error)
        elif not recommendations:
            self.rec_text.insert(tk.END, "AI Recommendations\n\n")
            self.rec_text.insert(tk.END, "No new recommendations found. Try rating more movies!")
        else:
            self.rec_text.insert(tk.END, "AI-Powered Movie Recommendations\n")
            self.rec_text.insert(tk.END, "Based on your viewing preferences and ratings\n\n")
            self.rec_text.insert(tk.END, f"Top {min(10, len(recommendations))} Recommendations:\n\n")
            
            for i, (sim, title, genres, imdb, year) in enumerate(recommendations[:10], 1):
                rec_text = f"{i}. {title} ({year})\n"
                rec_text += f"   IMDB: {imdb} | {genres}\n"
                rec_text += f"   Similarity Score: {sim:.2f}\n\n"
                self.rec_text.insert(tk.END, rec_text)
        
        self.rec_text.config(state='disabled')
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide window at first
    
    # Set window size and center
    root.geometry(f"{Config.WINDOW_WIDTH}x{Config.WINDOW_HEIGHT}")
    root.update_idletasks()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (Config.WINDOW_WIDTH // 2)
    y = (screen_height // 2) - (Config.WINDOW_HEIGHT // 2)
    root.geometry(f"{Config.WINDOW_WIDTH}x{Config.WINDOW_HEIGHT}+{x}+{y}")
    
    root.deiconify()  # Show window after centering
    app = MovieReviewApp(root)
    app.run()