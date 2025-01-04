import json
import hashlib
import os

class AdminData:
    def __init__(self, admin_file_path):
        self.admin_file_path = admin_file_path
        self.admin_data = self.load_admin_data()

    def load_admin_data(self):
        try:
            with open(self.admin_file_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"admin": {}}

    def save_admin_data(self):
        os.makedirs(os.path.dirname(self.admin_file_path), exist_ok=True)
        with open(self.admin_file_path, 'w') as f:
            json.dump(self.admin_data, f, indent=4)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_admin(self, email, password):
        admin = self.admin_data.get("admin")
        if admin and admin["email"] == email and admin["password"] == self.hash_password(password):
            return True
        return False

    def set_admin(self, email, password):
        self.admin_data["admin"] = {
            "email": email,
            "password": self.hash_password(password)
        }
        self.save_admin_data()

if __name__ == "__main__":
    admin_file_path = os.path.join(os.path.dirname(__file__), '../json', 'admin.json')
    admin_data = AdminData(admin_file_path)
    
    email = input("Enter admin email: ")
    password = input("Enter admin password: ")
    
    admin_data.set_admin(email, password)
    print("Admin credentials set successfully.")
    
    email_verifica = input("Verify - Enter admin email: ")
    password_verifica = input("Verify - Enter admin password: ")
    
    if admin_data.verify_admin(email_verifica, password_verifica):
        print("Verification successful: credentials are correct.")
    else:
        print("Verification failed: credentials are incorrect.")