import json
import os
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

class CasinoData:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self.load_data()

    def load_data(self):
        if not os.path.exists(self.file_path):
            self.create_empty_file()
        with open(self.file_path, 'r') as f:
            return json.load(f)

    def create_empty_file(self):
        with open(self.file_path, 'w') as f:
            json.dump({"users": {}}, f, indent=4)

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
        if game not in self.data["users"][user_id]["wins_losses"]:
            self.data["users"][user_id]["wins_losses"][game] = 0
        self.data["users"][user_id]["wins_losses"][game] += result
        self.save_data()

    def update_balance(self, user_id, result):
        self.data["users"][user_id]["balance"] += result
        self.save_data()

    def save_data(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.data, f, indent=4)

user_file = '../json/users.json'
user_data = CasinoData(user_file)

def get_user_ids(user_data):
    return list(user_data.data["users"].keys())

def get_user_win_loss(user_data, user_id):
    return sum(user_data.data["users"][user_id]['wins_losses'].values())

def get_user_wins_losses(user_data, user_ids):
    wins_losses = []
    for user_id in user_ids:
        win_loss = get_user_win_loss(user_data, user_id)
        wins_losses.append(win_loss)
    return wins_losses

def plot_user_wins_losses(user_data):
    if not user_data.data["users"]:
        print("No users found. Cannot create the graph.")
        return

    user_ids = get_user_ids(user_data)
    wins_losses = get_user_wins_losses(user_data, user_ids)
    create_bar_chart(user_ids, wins_losses)

def create_bar_chart(user_ids, wins_losses):
    colors = get_bar_colors(wins_losses)
    plot_bar_chart(user_ids, wins_losses, colors)

def get_bar_colors(wins_losses):
    colors = []
    for win_loss in wins_losses:
        color = get_bar_color(win_loss)
        colors.append(color)
    return colors

def get_bar_color(win_loss):
    return 'green' if win_loss >= 0 else 'red'

def plot_bar_chart(user_ids, wins_losses, colors):
    plt.bar(user_ids, wins_losses, color=colors)
    plt.xlabel('User ID')
    plt.ylabel('Win/Loss')
    plt.title('User Wins and Losses')
    plt.grid(True)
    
    green_patch = Patch(color='green', label='Wins')
    red_patch = Patch(color='red', label='Losses')
    plt.legend(handles=[green_patch, red_patch])
    
    plt.savefig('user_wins_losses.png')
    plt.show()

if __name__ == "__main__":
    plot_user_wins_losses(user_data)