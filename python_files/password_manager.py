import json
import os
import hashlib
import time

class PasswordManager:
    def __init__(self, user_file_path):
        self.user_file_path = user_file_path
        self.user_data = self.load_user_data()

    def load_user_data(self):
        try:
            with open(self.user_file_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"users": {}}

    def save_user_data(self):
        with open(self.user_file_path, 'w') as f:
            json.dump(self.user_data, f, indent=4)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def generate_reset_token(self, email):
        if email in self.user_data['users']:
            timestamp = str(int(time.time()))
            token = hashlib.sha256((email + timestamp).encode()).hexdigest()
            self.user_data['users'][email]['reset_token'] = token
            self.save_user_data()
            return token
        return None

    def verify_reset_token(self, token):
        for email, user in self.user_data['users'].items():
            if user.get('reset_token') == token:
                return email
        return None

    def reset_password(self, token, new_password):
        email = self.verify_reset_token(token)
        if email:
            self.user_data['users'][email]['password'] = self.hash_password(new_password)
            del self.user_data['users'][email]['reset_token']
            self.save_user_data()
            return True
        return False