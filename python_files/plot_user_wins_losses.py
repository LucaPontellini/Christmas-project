import json
import os
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

class CasinoData:
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
    def add_user(self, user_id, name, balance, email, password):
        
        """Aggiunge un nuovo utente ai dati e salva nel file JSON."""

        self.data["users"][user_id] = {
            "name": name,
            "balance": balance,
            "email": email,
            "password": password,
            "wins_losses": {}
        }
        self.save_data()

    #Funzione per aggiungere una vincita o una perdita per un gioco specifico
    def add_win_loss(self, user_id, game, result):
        
        """Aggiunge una vincita o una perdita per un gioco specifico."""

        if game not in self.data["users"][user_id]["wins_losses"]:
            self.data["users"][user_id]["wins_losses"][game] = 0
        self.data["users"][user_id]["wins_losses"][game] += result
        self.save_data()

    #Funzione per aggiornare il saldo di un utente
    def update_balance(self, user_id, result):
        
        """Aggiorna il saldo di un utente."""

        self.data["users"][user_id]["balance"] += result
        self.save_data()

    #Funzione per salvare i dati nel file JSON
    def save_data(self):
        
        """Salva i dati nel file JSON."""

        with open(self.file_path, 'w') as f:
            json.dump(self.data, f, indent=4)

user_file = '../json/users.json'
user_data = CasinoData(user_file)

#Funzione per ottenere gli ID degli utenti
def get_user_ids(user_data):
    
    """Ottiene gli ID degli utenti."""

    return list(user_data.data["users"].keys())

#Funzione per ottenere la somma delle vincite e delle perdite di un utente
def get_user_win_loss(user_data, user_id):
    
    """Ottiene la somma delle vincite e delle perdite di un utente."""

    return sum(user_data.data["users"][user_id]['wins_losses'].values())

#Funzione per ottenere la somma delle vincite e delle perdite per una lista di utenti
def get_user_wins_losses(user_data, user_ids):
    
    """Ottiene la somma delle vincite e delle perdite per una lista di utenti."""

    wins_losses = []
    for user_id in user_ids:
        win_loss = get_user_win_loss(user_data, user_id)
        wins_losses.append(win_loss)
    return wins_losses

#Funzione per creare e mostrare il grafico delle vincite e delle perdite degli utenti
def plot_user_wins_losses(user_data):
    
    """Crea e mostra il grafico delle vincite e delle perdite degli utenti."""

    if not user_data.data["users"]:
        print("No users found. Cannot create the graph.")
        return

    user_ids = get_user_ids(user_data)
    wins_losses = get_user_wins_losses(user_data, user_ids)
    create_bar_chart(user_ids, wins_losses)

#Funzione per creare un grafico a barre
def create_bar_chart(user_ids, wins_losses):
    
    """Crea un grafico a barre utilizzando i dati delle vincite e delle perdite degli utenti."""

    colors = get_bar_colors(wins_losses)
    plot_bar_chart(user_ids, wins_losses, colors)

#Funzione per ottenere i colori delle barre del grafico
def get_bar_colors(wins_losses):
    
    """Ottiene i colori delle barre del grafico in base ai risultati."""

    colors = []
    for win_loss in wins_losses:
        color = get_bar_color(win_loss)
        colors.append(color)
    return colors

#Funzione per determinare il colore di una barra in base al risultato
def get_bar_color(win_loss):
    
    """Determina il colore di una barra in base al risultato (verde per vincite, rosso per perdite)."""

    return 'green' if win_loss >= 0 else 'red'

#Funzione per creare e mostrare un grafico a barre
def plot_bar_chart(user_ids, wins_losses, colors):
    
    """Crea e mostra un grafico a barre con i dati delle vincite e delle perdite degli utenti."""

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