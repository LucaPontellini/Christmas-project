import json
import os
import hashlib

class UserData:
    def __init__(self, user_file_path):
        self.user_file_path = user_file_path
        self.data = self.load_data()

    def load_data(self):
        if os.path.exists(self.user_file_path):
            with open(self.user_file_path, 'r') as f:
                return json.load(f)
        else:
            return {"users": {}}

    def save_data(self):
        os.makedirs(os.path.dirname(self.user_file_path), exist_ok=True)
        with open(self.user_file_path, 'w') as f:
            json.dump(self.data, f, indent=4)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def add_user(self, user_id, name, balance, email, password):
        if user_id not in self.data["users"]:
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
        if user_id in self.data["users"]:
            stored_password = self.data["users"][user_id]['password']
            return stored_password == self.hash_password(password)
        return False

    def add_win_loss(self, user_id, game, result):
        if user_id in self.data["users"]:
            if game in self.data["users"][user_id]['wins_losses']:
                self.data["users"][user_id]['wins_losses'][game] += result
            else:
                self.data["users"][user_id]['wins_losses'][game] = result
            self.save_data()

    def process_transaction(self, user_id, amount, transaction_type):
        if user_id in self.data["users"]:
            if transaction_type == 'deposit':
                self.data["users"][user_id]['balance'] += amount
            elif transaction_type == 'withdraw':
                if self.data["users"][user_id]['balance'] >= amount:
                    self.data["users"][user_id]['balance'] -= amount
                else:
                    raise ValueError("Insufficient balance")
            self.save_data()