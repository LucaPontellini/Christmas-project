import json
import matplotlib.pyplot as plt
import os
from datetime import datetime, timedelta
import random

class UserRegistrationData:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self.load_data()

    def load_data(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump({"users": {}}, f, indent=4)
        with open(self.file_path, 'r') as f:
            return json.load(f)

    def add_user(self, user_id, name, balance, email, password, registration_date):
        self.data["users"][user_id] = {
            "name": name,
            "balance": balance,
            "email": email,
            "password": password,
            "wins_losses": {},
            "registration_date": registration_date.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.save_data()

    def save_data(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.data, f, indent=4)

user_file = '../json/users_data.json'

if not os.path.exists(user_file):
    with open(user_file, 'w') as f:
        json.dump({"users": {}}, f, indent=4)

user_data = UserRegistrationData(user_file)

def simulate_user_registrations(user_data, num_users):
    start_date = datetime.now() - timedelta(days=365 * 10)
    for i in range(1, num_users + 1):
        user_id = f"user{i}"
        random_days = random.randint(0, 365 * 10)
        registration_date = start_date + timedelta(days=random_days)
        user_data.add_user(user_id, f"User {i}", 0, f"user{i}@example.com", "password", registration_date)

def generate_random_registrations(dates):
    registrations = []
    for _ in range(len(dates)):
        registrations.append(random.randint(-10, 10))
    return registrations

def calculate_cumulative_registrations(registrations):
    cumulative = []
    total = 0
    for reg in registrations:
        total += reg
        cumulative.append(total)
    return cumulative

def get_registration_dates(user_data):
    registration_dates = []
    for user_id in user_data.data["users"]:
        registration_dates.append(user_data.data["users"][user_id]['registration_date'])
    return registration_dates

def convert_dates(registration_dates):
    registration_dates.sort()
    dates = []
    for date in registration_dates:
        dates.append(datetime.strptime(date, "%Y-%m-%d %H:%M:%S"))
    return dates

def plot_user_registrations(user_data):
    registration_dates = get_registration_dates(user_data)
    dates = convert_dates(registration_dates)
    registrations = generate_random_registrations(dates)
    cumulative_registrations = calculate_cumulative_registrations(registrations)
    plot_graph(dates, cumulative_registrations)

def plot_graph(dates, cumulative_registrations):
    if dates:
        plt.figure(figsize=(10, 6))
        plt.plot(dates, cumulative_registrations, marker='o', linestyle='-', color='b', markersize=4)
        plt.fill_between(dates, cumulative_registrations, color='skyblue', alpha=0.4)
        plt.axhline(0, color='black', linewidth=0.5)
        
        #Calcolo del valore minimo e massimo delle registrazioni cumulative
        min_value = min(cumulative_registrations) - 10
        max_value = max(cumulative_registrations) + 10
        
        #Intervallo di valori per l'asse y
        yticks_values = range(min_value, max_value, 10)
        plt.yticks(yticks_values)
        
        plt.xticks(rotation=45)
        plt.xlabel('Date')
        plt.ylabel('Number of Registrations')
        plt.title('User Registrations Over Time')
        plt.grid(True)
        plt.savefig('user_registrations.png')
        plt.show()
    else:
        print("No registration dates available to plot.")

#Simulazione delle registrazioni degli utenti
simulate_user_registrations(user_data, num_users=1000)

#Esempio di utilizzo della funzione del grafico
plot_user_registrations(user_data)