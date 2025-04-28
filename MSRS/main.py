import json
import os
from datetime import datetime

# Constants for file paths
DATA_DIR = "data"
USERS_FILE = os.path.join(DATA_DIR, "users.json")
MOVIES_FILE = os.path.join(DATA_DIR, "movies.json")

# Data handling functions
def load_users():
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

def load_movies():
    with open(MOVIES_FILE, 'r') as f:
        return json.load(f)

def save_movies(movies):
    with open(MOVIES_FILE, 'w') as f:
        json.dump(movies, f, indent=4)

# Clearing the screen for better readability
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# User registration
def register_user():
    users = load_users()
    
    print("\n--- Register ---")
    username = input("Enter username: ").strip().lower() 
    
    
    if username in users: # Check if username already exists
        clear_screen()
        print("Username already exists!")
        return None
    elif len(username) < 5: # Username length check
        clear_screen()
        print("Username must be at least 5 characters long!")
        return None
    
    password = input("Enter password: ").strip()  
    if not password: # Password empty check
        clear_screen()
        print("Password cannot be empty!") 
        return None
    elif len(password) < 8: # Password length check
        clear_screen()
        print("Password must be at least 8 characters long!")
        return None
    elif not any(char.isdigit() for char in password): # Password digit check
        clear_screen()
        print("Password must contain at least one digit!")
        return None
    elif not any(char.isalpha() for char in password): # Password letter check
        clear_screen()
        print("Password must contain at least one letter!")
        return None
    elif any(char in "!@#$%^&*()-_+=<>?/" for char in password): # Password special character check
        clear_screen()
        print("Password cannot contain special characters! (!@#$%^&*()-_+=<>?/)")
        return None
    
    users[username] = {
        "password": password,
        "rated_movies": []
    } 
    
    save_users(users) # Save new user to data file
    clear_screen()
    print("Registration successful! You can now login.")
    return username 

# User login
def login_user():
    users = load_users()
    
    print("\n--- Login ---")
    username = input("Username: ").strip().lower()
    password = input("Password: ").strip()
    
    if username in users and users[username]["password"] == password: # Check if username and password match
        clear_screen()
        print("Login successful!")
        return username
    else: # Invalid login attempt
        clear_screen()
        print("Invalid username or password!")
        return None

# Movie listing and details
def list_movies():
    movies = load_movies()
    clear_screen()
    print("\n--- Movie/TV Series List ---")
    for idx, (movie_id, movie) in enumerate(movies.items(), 1): # Enumerate movies // AI suggested to use enumerate for better readability
        print(f"{idx}. {movie['Series_Title']} ({movie['Released_Year']}) - IMDB: {movie.get('IMDB_Rating')}")

def get_movie_by_index(index): # Get movie by index
    movies = load_movies()
    try:
        return list(movies.items())[index - 1]
    except IndexError:
        return None, None

# Show movie details
def show_movie_details(movie_id, movie_data):
    clear_screen()
    print("\n--- Movie/TV Series Details ---")
    print(f"Title: {movie_data['Series_Title']}")
    print(f"Year: {movie_data['Released_Year']}")
    print(f"Certificate: {movie_data['Certificate']}")
    print(f"Runtime: {movie_data['Runtime']} minutes")
    print(f"Genre: {movie_data['Genre']}")
    print(f"IMDB Rating: {movie_data.get('IMDB_Rating')}")
    print(f"Metascore: {movie_data['Meta_score']}")
    print(f"Director: {movie_data['Director']}")
    print(f"Stars: {movie_data['Star1']}, {movie_data['Star2']}, {movie_data['Star3']}, {movie_data['Star4']}")
    print(f"Votes: {movie_data['No_of_Votes']}")
    print(f"Gross: ${movie_data['Gross']} million")
    print(f"\nOverview:\n{movie_data['Overview']}")
    
    print("\n--- Reviews ---") # Display reviews
    if movie_data['reviews']:
        for review in movie_data['reviews']:
            print(f"User: {review['username']}")
            print(f"Date: {review['date']}")
            print(f"Rating: {review['rating']}/10")
            print(f"Review: {review['content']}")
            print("-" * 30)
    else:
        print("No reviews yet.")

# Rate and review a movie
def rate_and_review_movie(username):
    users = load_users()
    movies = load_movies()
    
    list_movies()
    try:
        choice = int(input("Enter movie number to rate/review: "))
        movie_id, movie_data = get_movie_by_index(choice)
        if not movie_id:
            clear_screen()
            print("Invalid movie number!")
            return
    except ValueError:
        clear_screen()
        print("Please enter a valid number!")
        return
    
    # Check if the user has already rated the movie
    if movie_id in users[username]["rated_movies"]:
        clear_screen()
        print("You've already rated this movie!")
        update_choice = input("Do you want to update your review? (yes/no): ").strip().lower()
        if update_choice != "yes":
            return
    
    # System asks for rating until a valid input is given
    while True:
        try:
            rating = int(input(f"Enter your rating for '{movie_data['Series_Title']}' (1-10): "))
            if 1 <= rating <= 10:
                break
            else:
                clear_screen()
                print("Rating must be between 1 and 10!")
        except ValueError:
            clear_screen()
            print("Please enter a valid number!")
    
    # Gets review
    print(f"\nWrite your review for '{movie_data['Series_Title']}':")
    review_content = input("> ").strip()
    
    if not review_content: # Check if review is empty
        clear_screen()
        print("Review cannot be empty!")
        return
    
    # Update movie reviews
    all_reviews = movies[movie_id]['reviews']
    for review in all_reviews:
        if review['username'] == username: # Check if the user has already reviewed
            review['rating'] = rating
            review['content'] = review_content
            review['date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            break
    else:
        # Add new review
        movies[movie_id]['reviews'].append({
            "username": username,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "rating": rating,
            "content": review_content
        })
        # Update user's rated movies
        users[username]["rated_movies"].append(movie_id)
    
    save_movies(movies)
    save_users(users)
    clear_screen()
    print("Rating and review submitted successfully!")


# Main menu
def main():
    current_user = None
    
    while True:
        print("\n=== Movie/Tv Series Review System ===")
        if current_user:
            users = load_users()
            
            print("Logged in as: " + current_user)
            
            print("1. List Movies")
            print("2. View Movie Details")
            print("3. Rate & Review a Movie")
            print("4. Logout")
            print("5. Exit")
        else:
            print("1. Register")
            print("2. Login")
            print("3. List Movies")
            print("4. View Movie Details (Login Required)")
            print("5. Exit")
        
        choice = input("Enter your choice: ").strip()
        
        if current_user:
            if choice == "1":
                list_movies()
            elif choice == "2":
                list_movies()
                try:
                    movie_num = int(input("Enter movie number to view details: "))
                    movie_id, movie_data = get_movie_by_index(movie_num)
                    if movie_id:
                        show_movie_details(movie_id, movie_data)
                    else:
                        print("Invalid movie number!")
                except ValueError:
                    print("Please enter a valid number!")
            elif choice == "3":
                rate_and_review_movie(current_user)
            elif choice == "4":
                current_user = None
                clear_screen()
                print("Logged out successfully!")
            elif choice == "5":
                clear_screen()
                print("Goodbye!")
                break
            else:
                clear_screen()
                print("Invalid choice!")
        else:
            if choice == "1":
                register_user()
            elif choice == "2":
                current_user = login_user()
            elif choice == "3":
                list_movies()
            elif choice == "4":
                clear_screen()
                print("Please login first!")
            elif choice == "5":
                clear_screen()
                print("Goodbye!")
                break
            else:
                clear_screen()
                print("Invalid choice!")

if __name__ == "__main__": 
    main()