import json
import os
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

class UserRegistrationData:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self.load_data()

    #Funzione per caricare i dati dal file JSON
    def load_data(self):

        """Carica i dati dal file JSON. Crea un file vuoto se non esiste."""

        if not os.path.exists(self.file_path):
            self.create_empty_file()
        with open(self.file_path, 'r') as f:
            return json.load(f)

    #Funzione per creare un file JSON vuoto
    def create_empty_file(self):
        
        """Crea un file JSON vuoto con un dizionario vuoto."""

        with open(self.file_path, 'w') as f:
            json.dump({"users": {}}, f, indent=4)

    #Funzione per aggiungere un nuovo utente
    def add_user(self, user_id, name, balance, email, password, registration_date):
        
        """Aggiunge un nuovo utente ai dati e salva nel file JSON."""

        self.data["users"][user_id] = {
            "name": name,
            "balance": balance,
            "email": email,
            "password": password,
            "registration_date": registration_date
        }
        self.save_data()

    #Funzione per salvare i dati nel file JSON
    def save_data(self):
        
        """Salva i dati nel file JSON."""

        with open(self.file_path, 'w') as f:
            json.dump(self.data, f, indent=4)

user_file = '../json/users.json'
user_data = UserRegistrationData(user_file)

#Funzione per ottenere le date di registrazione degli utenti
def get_registration_dates(user_data):
    
    """Ottiene le date di registrazione degli utenti."""

    registration_dates = []
    for user_id in user_data.data["users"]:
        registration_date = user_data.data["users"][user_id]['registration_date']
        registration_dates.append(registration_date)
    return registration_dates

#Funzione per convertire le date in oggetti datetime e ordinarle
def convert_dates(registration_dates):
    
    """Converte le date in oggetti datetime e le ordina."""

    registration_dates.sort()
    dates = []
    for date in registration_dates:
        dates.append(datetime.strptime(date, "%Y-%m-%d %H:%M:%S"))
    return dates

#Funzione per calcolare le registrazioni cumulative
def calculate_cumulative_registrations(dates):
    
    """Calcola le registrazioni cumulative."""

    cumulative = []
    total = 0
    for date in dates:
        total += 1
        cumulative.append(total)
    return cumulative

#Funzione per creare e mostrare il grafico delle registrazioni degli utenti
def plot_user_registrations(user_data):
    
    """Crea e mostra il grafico delle registrazioni degli utenti."""

    if not user_data.data["users"]:
        print("No users found. Cannot create the graph.")
        return

    registration_dates = get_registration_dates(user_data)
    dates = convert_dates(registration_dates)
    cumulative_registrations = calculate_cumulative_registrations(dates)
    plot_graph(dates, cumulative_registrations)

#Funzione per creare un grafico
def plot_graph(dates, cumulative_registrations):
    
    """Crea un grafico delle registrazioni degli utenti."""
    
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
    else: print("No registration dates available to plot.")

if __name__ == "__main__":
    plot_user_registrations(user_data)