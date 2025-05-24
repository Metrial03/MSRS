"""
Data Manager for Movie Review App
"""
import json
import os
from datetime import datetime
from config import Config

class DataManager:
    def __init__(self):
        self.users_file = Config.USERS_FILE
        self.movies_file = Config.MOVIES_FILE
        self.data_dir = Config.DATA_DIR
        
    def ensure_data_dir(self):
        """Ensure data directory exists"""
        os.makedirs(self.data_dir, exist_ok=True)
    
    def load_users(self):
        """Load users from JSON file"""
        try:
            with open(self.users_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def save_users(self, users):
        """Save users to JSON file"""
        self.ensure_data_dir()
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=4)
    
    def load_movies(self):
        """Load movies from JSON file"""
        try:
            with open(self.movies_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def save_movies(self, movies):
        """Save movies to JSON file"""
        self.ensure_data_dir()
        with open(self.movies_file, 'w') as f:
            json.dump(movies, f, indent=4)
    
    def add_review_to_movie(self, movie_id, username, rating, content):
        """Add or update a review for a movie"""
        movies = self.load_movies()
        users = self.load_users()
        
        # Update or add review
        all_reviews = movies[movie_id]['reviews']
        for review in all_reviews:
            if review['username'] == username:
                review['rating'] = rating
                review['content'] = content
                review['date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                break
        else:
            movies[movie_id]['reviews'].append({
                "username": username,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "rating": rating,
                "content": content
            })
            users[username]["rated_movies"].append(movie_id)
        
        self.save_movies(movies)
        self.save_users(users)
        
    def get_user_reviews(self, username):
        """Get all reviews for a specific user"""
        users = self.load_users()
        movies = self.load_movies()
        
        user_reviews = []
        if username in users:
            for movie_id in users[username]["rated_movies"]:
                if movie_id in movies:
                    movie = movies[movie_id]
                    for review in movie["reviews"]:
                        if review["username"] == username:
                            user_reviews.append((movie["Series_Title"], review))
        
        return user_reviews