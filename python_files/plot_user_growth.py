import json
import matplotlib.pyplot as plt
from random import randint, choice
import os

class CasinoUserData:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self.load_data()

    def load_data(self):
        with open(self.file_path, 'r') as f:
            return json.load(f)

    def add_user(self, user_id, name, balance, email, password):
        self.data["users"][user_id] = {
            "name": name,
            "balance": balance,
            "email": email,
            "password": password,
            "wins_losses": {}
        }
        self.save_data()

    def add_win_loss(self, user_id, game, result):
        if game in self.data["users"][user_id]["wins_losses"]:
            self.data["users"][user_id]["wins_losses"][game] += result
        else:
            self.data["users"][user_id]["wins_losses"][game] = result
        self.save_data()

    def update_balance(self, user_id, amount):
        self.data["users"][user_id]["balance"] += amount
        self.save_data()

    def save_data(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.data, f)

user_file = '../json/users_data.json'

# Aggiungi un controllo per verificare se il file JSON è vuoto o non valido
if os.stat(user_file).st_size == 0:
    with open(user_file, 'w') as f:
        json.dump({"users": {}}, f)

user_data = CasinoUserData(user_file)

def simulate_casino(user_data, games, num_users, num_rounds):
    for i in range(1, num_users + 1):
        user_id = f"user{i}"
        user_data.add_user(user_id, f"User {i}", randint(100, 1000), f"user{i}@example.com", "password")

    for _ in range(num_rounds):
        for user_id in user_data.data["users"]:
            game = choice(games)
            result = randint(-100, 100)
            user_data.add_win_loss(user_id, game, result)
            user_data.update_balance(user_id, result)

# Funzione per creare un grafico a barre per l'andamento degli utenti
def plot_user_growth(user_data):
    user_ids = list(user_data.data["users"].keys())
    balances = [user_data.data["users"][user_id]['balance'] for user_id in user_ids]
    plt.bar(user_ids, balances)
    plt.xlabel('User ID')
    plt.ylabel('Balance')
    plt.title('User Growth')
    plt.grid(True)
    plt.savefig('user_growth.png')
    plt.show()

# Creare un set di dati di esempio e simulare l'andamento del casinò
games = ["Blackjack", "Caribbean Stud Poker", "Craps", "Poker Texas Hold'em", "Roulette", "Slot Machine", "Video Poker"]
simulate_casino(user_data, games, num_users=10, num_rounds=100)

# Esempio di utilizzo della funzione di grafico
plot_user_growth(user_data)