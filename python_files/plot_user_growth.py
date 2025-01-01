import json
import os
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

class UserRegistrationData:
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

    def add_user(self, user_id, name, balance, email, password, registration_date):
        self.data["users"][user_id] = {
            "name": name,
            "balance": balance,
            "email": email,
            "password": password,
            "registration_date": registration_date
        }
        self.save_data()

    def save_data(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.data, f, indent=4)

user_file = '../json/users_data.json'
user_data = UserRegistrationData(user_file)

def get_registration_dates(user_data):
    registration_dates = []
    for user_id in user_data.data["users"]:
        registration_date = user_data.data["users"][user_id]['registration_date']
        registration_dates.append(registration_date)
    return registration_dates

def convert_dates(registration_dates):
    registration_dates.sort()
    dates = []
    for date in registration_dates:
        dates.append(datetime.strptime(date, "%Y-%m-%d %H:%M:%S"))
    return dates

def calculate_cumulative_registrations(dates):
    cumulative = []
    total = 0
    for date in dates:
        total += 1
        cumulative.append(total)
    return cumulative

def plot_user_registrations(user_data):
    if not user_data.data["users"]:
        print("No users found. Cannot create the graph.")
        return

    registration_dates = get_registration_dates(user_data)
    dates = convert_dates(registration_dates)
    cumulative_registrations = calculate_cumulative_registrations(dates)
    plot_graph(dates, cumulative_registrations)

def plot_graph(dates, cumulative_registrations):
    if dates:
        plt.figure(figsize=(10, 6))
        plt.plot(dates, cumulative_registrations, marker='o', linestyle='-', color='b', markersize=4)
        plt.fill_between(dates, cumulative_registrations, color='skyblue', alpha=0.4)
        plt.axhline(0, color='black', linewidth=0.5)
        
        min_value = min(cumulative_registrations) - 10
        max_value = max(cumulative_registrations) + 10
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

if __name__ == "__main__":
    plot_user_registrations(user_data)