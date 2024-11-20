import re
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize the MongoDB client and specify the database.
db_client = MongoClient('mongodb://localhost:27017/')
db = db_client['my_flask_app']

class User:
    def __init__(self, username, password, email, json_path=None, logo_path=None, hashed=False):
        self.username = username
        if hashed:
            self.password = password
        else:
            self.password = generate_password_hash(password)
        self.email = email
        self.json_path = json_path
        self.logo_path = logo_path

    def save_to_db(self):
        user_data = {
            "username": self.username,
            "password": self.password,
            "email": self.email,
            "json_path": self.json_path,
            "logo_path": self.logo_path
        }
        # db.users.update_one({"email": self.email}, {"$set": user_data}, upsert=True)
        db.users.insert_one(user_data)

    def update_db(self):
        user_data = {
            "username": self.username,
            "password": self.password,
            "email": self.email,
            "json_path": self.json_path,
            "logo_path": self.logo_path
        }
        db.users.update_one({"email": self.email}, {"$set": user_data}, upsert=True)
    

    def verify_password(self, password):
        return check_password_hash(self.password, password)
    
    @staticmethod
    def find_by_email(email):
        user_data = db.users.find_one({"email": email})
        if user_data:
            return User(user_data['username'], user_data['password'], user_data['email'], user_data.get('json_path'), user_data.get('logo_path'), hashed=True)
        return None

    @staticmethod
    def is_valid_email(email):
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, email) is not None
