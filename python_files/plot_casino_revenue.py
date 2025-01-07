import json
import os
from matplotlib import pyplot as plt

class CasinoUserData:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self.load_data()

    #Funzione per caricare i dati dal file JSON
    def load_data(self):
        
        """Carica i dati dal file JSON.
        
        Questa funzione verifica se il file esiste e, in caso contrario, crea un file JSON vuoto.
        Successivamente legge e restituisce i dati dal file JSON."""

        if not os.path.exists(self.file_path):
            self.create_empty_file()
        return self.read_data()

    #Funzione per creare un file JSON vuoto
    def create_empty_file(self):
        
        """Crea un file JSON vuoto.
        
        Questa funzione crea un nuovo file JSON con una struttura iniziale vuota
        per contenere i dati degli utenti."""

        with open(self.file_path, 'w') as f:
            json.dump({"users": {}}, f, indent=4)

    #Funzione per leggere i dati dal file JSON
    def read_data(self):
        
        """Legge i dati dal file JSON.
        
        Questa funzione apre il file JSON e legge i dati contenuti,
        restituendoli come un dizionario."""

        with open(self.file_path, 'r') as f:
            return json.load(f)

    #Funzione per aggiungere un nuovo utente
    def add_user(self, user_id, name, balance, email, password):
        
        """Aggiunge un nuovo utente.
        
        Questa funzione aggiunge un nuovo utente ai dati memorizzati, utilizzando
        le informazioni fornite, e salva i dati aggiornati nel file JSON."""
        
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
        
        """Aggiunge una vincita o una perdita per un gioco specifico.
        
        Questa funzione aggiorna i dati di vincite e perdite di un utente
        per il gioco specificato, sommando il risultato al valore corrente."""

        if game in self.data["users"][user_id]["wins_losses"]:
            self.data["users"][user_id]["wins_losses"][game] += result
        else:
            self.data["users"][user_id]["wins_losses"][game] = result
        self.save_data()

    #Funzione per aggiornare il saldo di un utente
    def update_balance(self, user_id, amount):
        
        """Aggiorna il saldo di un utente.
        
        Questa funzione aggiunge un importo specificato al saldo corrente
        dell'utente e salva i dati aggiornati nel file JSON."""

        self.data["users"][user_id]["balance"] += amount
        self.save_data()

    #Funzione per salvare i dati nel file JSON
    def save_data(self):
        
        """Salva i dati nel file JSON.
        
        Questa funzione scrive i dati aggiornati degli utenti nel file JSON,
        utilizzando una struttura JSON indentata per migliorare la leggibilità."""

        with open(self.file_path, 'w') as f:
            json.dump(self.data, f, indent=4)

user_file = '../json/users.json'

#Creazione del file JSON se non esiste
if not os.path.exists(user_file):
    with open(user_file, 'w') as f:
        json.dump({"users": {}}, f, indent=4)

user_data = CasinoUserData(user_file)

#Funzione per ottenere gli ID degli utenti
def get_user_ids(user_data):
    
    """Ottiene gli ID degli utenti.
    
    Questa funzione restituisce una lista degli ID degli utenti presenti nei dati."""
    
    return list(user_data.data["users"].keys())

#Funzione per ottenere il saldo di un utente
def get_user_balance(user_data, user_id):
    
    """Ottiene il saldo di un utente.
    
    Questa funzione restituisce il saldo corrente di un utente specificato."""

    return user_data.data["users"][user_id]['balance']

#Funzione per ottenere i ricavi degli utenti
def get_user_revenues(user_data, user_ids):
    
    """Ottiene i ricavi degli utenti.
    
    Questa funzione restituisce una lista dei saldi degli utenti specificati."""

    revenues = []
    for user_id in user_ids:
        balance = get_user_balance(user_data, user_id)
        revenues.append(balance)
    return revenues

#Funzione per creare e mostrare il grafico dei ricavi del casinò
def plot_casino_revenue(user_data):
    
    """Crea e mostra il grafico dei ricavi del casinò.
    
    Questa funzione genera un grafico a barre che rappresenta i ricavi degli utenti del casinò,
    utilizzando i dati di bilancio attuali."""

    if not user_data.data["users"]:
        print("No users found. Cannot create the graph.")
        return

    user_ids = get_user_ids(user_data)
    revenues = get_user_revenues(user_data, user_ids)
    create_bar_chart(user_ids, revenues)

#Funzione per creare un grafico a barre
def create_bar_chart(user_ids, revenues):
    
    """Crea un grafico a barre.
    
    Questa funzione genera un grafico a barre utilizzando gli ID degli utenti e i loro rispettivi ricavi."""

    plt.bar(user_ids, revenues)
    plt.xlabel('User ID')
    plt.ylabel('Revenue')
    plt.title('Casino Revenue')
    plt.grid(True)
    plt.savefig('casino_revenue.png')
    plt.show()

if __name__ == "__main__":
    plot_casino_revenue(user_data)