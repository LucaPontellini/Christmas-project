import json
import os
from random import choice, randint
from matplotlib import pyplot as plt

class CasinoUserData:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self.load_data()

    def load_data(self):
        if not os.path.exists(self.file_path):
            self.create_empty_file()
        return self.read_data()

    def create_empty_file(self):
        with open(self.file_path, 'w') as f:
            json.dump({"users": {}}, f, indent=4)

    def read_data(self):
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
            json.dump(self.data, f, indent=4)

user_file = '../json/users_data.json'

if not os.path.exists(user_file):
    with open(user_file, 'w') as f:
        json.dump({"users": {}}, f, indent=4)

user_data = CasinoUserData(user_file)

def simulate_casino(user_data, games, num_users, num_rounds):
    add_users(user_data, num_users)
    play_games(user_data, games, num_rounds)

def add_users(user_data, num_users):
    for i in range(1, num_users + 1):
        user_id = f"user{i}"
        user_data.add_user(user_id, f"User {i}", randint(100, 1000), f"user{i}@example.com", "password")

def play_games(user_data, games, num_rounds):
    for _ in range(num_rounds):
        for user_id in user_data.data["users"]:
            game = choice(games)
            result = randint(-100, 100)
            user_data.add_win_loss(user_id, game, result)
            user_data.update_balance(user_id, result)

def get_user_ids(user_data):
    return list(user_data.data["users"].keys())

def get_user_balance(user_data, user_id):
    return user_data.data["users"][user_id]['balance']

def get_user_revenues(user_data, user_ids):
    revenues = []
    for user_id in user_ids:
        balance = get_user_balance(user_data, user_id)
        revenues.append(balance)
    return revenues

#Funzione per creare un grafico a barre per il guadagno del casinò
def plot_casino_revenue(user_data):
    user_ids = get_user_ids(user_data)
    revenues = get_user_revenues(user_data, user_ids)
    create_bar_chart(user_ids, revenues)

def create_bar_chart(user_ids, revenues):
    plt.bar(user_ids, revenues)
    plt.xlabel('User ID')
    plt.ylabel('Revenue')
    plt.title('Casino Revenue')
    plt.grid(True)
    plt.savefig('casino_revenue.png')
    plt.show()

#Creazione di un set di dati di esempio e simulazione dell'andamento del casinò
games = ["Blackjack", "Caribbean Stud Poker", "Craps", "Poker Texas Hold'em", "Roulette", "Slot Machine", "Video Poker"]
simulate_casino(user_data, games, num_users=10, num_rounds=100)

#Esempio di utilizzo della funzione del grafico
plot_casino_revenue(user_data)