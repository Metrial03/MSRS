"""
Authentication Manager for Movie Review App
"""
from data_manager import DataManager

class AuthManager:
    def __init__(self):
        self.data_manager = DataManager()
        self.current_user = None
    
    def validate_username(self, username):
        """Validate username requirements"""
        username = username.strip().lower()
        
        if len(username) < 5:
            return False, "Username must be at least 5 characters long!"
        
        return True, ""
    
    def validate_password(self, password):
        """Validate password requirements"""
        password = password.strip()
        
        if len(password) < 8:
            return False, "Password must be at least 8 characters long!"
        
        if not any(char.isdigit() for char in password):
            return False, "Password must contain at least one digit!"
        
        if not any(char.isalpha() for char in password):
            return False, "Password must contain at least one letter!"
        
        if any(char in "!@#$%^&*()-_+=<>?/" for char in password):
            return False, "Password cannot contain special characters!"
        
        return True, ""
    
    def login(self, username, password):
        """Handle user login"""
        if not username or not password:
            return False, "Please fill in all fields"
        
        users = self.data_manager.load_users()
        username = username.strip().lower()
        
        if username in users and users[username]["password"] == password:
            self.current_user = username
            return True, "Login successful!"
        else:
            return False, "Invalid username or password!"
    
    def register(self, username, password):
        """Handle user registration"""
        if not username or not password:
            return False, "Please fill in all fields"
        
        username = username.strip().lower()
        
        # Validate username
        valid, message = self.validate_username(username)
        if not valid:
            return False, message
        
        # Validate password
        valid, message = self.validate_password(password)
        if not valid:
            return False, message
        
        users = self.data_manager.load_users()
        
        if username in users:
            return False, "Username already exists!"
        
        users[username] = {
            "password": password.strip(),
            "rated_movies": []
        }
        
        self.data_manager.save_users(users)
        return True, "Registration successful! You can now login."
    
    def logout(self):
        """Handle user logout"""
        self.current_user = None
    
    def is_logged_in(self):
        """Check if user is logged in"""
        return self.current_user is not None
    
    def get_current_user(self):
        """Get current logged in user"""
        return self.current_user