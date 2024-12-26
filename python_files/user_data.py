import json
import os
import hashlib
import matplotlib.pyplot as plt

class UserData:
    def __init__(self, user_file_path):
        self.user_file_path = os.path.join('json', user_file_path)
        self.data = self.load_data()

    def load_data(self):
        if os.path.exists(self.user_file_path):
            with open(self.user_file_path, 'r') as f:
                return json.load(f)
        else:
            self.create_default_data()
            return {"users": {}}

    def create_default_data(self):
        default_data = {"users": {}}
        if os.path.dirname(self.user_file_path):
            os.makedirs(os.path.dirname(self.user_file_path), exist_ok=True)
        with open(self.user_file_path, 'w') as f:
            json.dump(default_data, f, indent=4)

    def save_data(self):
        if os.path.dirname(self.user_file_path):
            os.makedirs(os.path.dirname(self.user_file_path), exist_ok=True)
        with open(self.user_file_path, 'w') as f:
            json.dump(self.data, f, indent=4)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def add_user(self, user_id, name, balance, email, password):
        if not user_id:
            raise ValueError("User ID is required.")
        if not name:
            raise ValueError("Name is required.")
        if not email:
            raise ValueError("Email is required.")
        if not password:
            raise ValueError("Password is required.")
        if user_id in self.data["users"]:
            raise ValueError("User ID already exists.")
        hashed_password = self.hash_password(password)
        self.data["users"][user_id] = {
            'name': name,
            'balance': balance,
            'total_money': 0,
            'remaining_money': 0,
            'email': email,
            'password': hashed_password,
            'wins_losses': {}
        }
        self.save_data()

    def authenticate_user(self, user_id, password):
        if not user_id:
            raise ValueError("User ID is required.")
        if not password:
            raise ValueError("Password is required.")
        if user_id in self.data["users"]:
            stored_password = self.data["users"][user_id]['password']
            return stored_password == self.hash_password(password)
        return False

    def update_password(self, user_id, new_password):
        if not user_id:
            raise ValueError("User ID is required.")
        if not new_password:
            raise ValueError("New password is required.")
        if user_id in self.data["users"]:
            hashed_password = self.hash_password(new_password)
            self.data["users"][user_id]['password'] = hashed_password
            self.save_data()
            return True
        return False

    def process_transaction(self, user_id, amount, transaction_type):
        if not user_id:
            raise ValueError("User ID is required.")
        if amount is None:
            raise ValueError("Amount is required.")
        if user_id in self.data["users"]:
            if transaction_type == 'deposit':
                self.data["users"][user_id]['balance'] += amount
            elif transaction_type == 'withdraw':
                if self.data["users"][user_id]['balance'] >= amount:
                    self.data["users"][user_id]['balance'] -= amount
                else:
                    raise ValueError("Insufficient balance")
            self.save_data()
        else:
            raise ValueError("User ID does not exist.")

    def update_balance(self, user_id, amount):
        if not user_id:
            raise ValueError("User ID is required.")
        if amount is None:
            raise ValueError("Amount is required.")
        if user_id in self.data["users"]:
            self.data["users"][user_id]['balance'] += amount
            self.save_data()
        else:
            raise ValueError("User ID does not exist.")

    def delete_user(self, user_id):
        if not user_id:
            raise ValueError("User ID is required.")
        if user_id in self.data["users"]:
            del self.data["users"][user_id]
            self.save_data()
            return True
        else:
            raise ValueError("User ID does not exist.")

    def plot_user_data(self, user_id):
        if user_id not in self.data["users"]:
            raise ValueError("User ID does not exist.")
        user = self.data["users"][user_id]
        labels = ['Balance', 'Total Money', 'Remaining Money']
        values = [user['balance'], user['total_money'], user['remaining_money']]
        plt.bar(labels, values)
        plt.title(f"User Data for {user['name']}")
        plt.show()