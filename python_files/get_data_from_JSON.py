import json
from tabulate import tabulate
from user_data import UserData
from deck_data import DeckData

#File JSON dei dati dell'utente e dei dati del mazzo
user_file = '\\Christmas-project\\json\\users.json'
deck_file = '\\Christmas-project\\json\\deck_into_json.json'

user_data = UserData(user_file)
deck_data = DeckData(deck_file)

#Funzione per i dati delle fiches
def chips_data():
    
    """Restituisce i dati delle fiches.
    
    Questa funzione crea un dizionario contenente i valori delle fiches
    in base ai loro colori."""

    return {
        "value_of_chips": {
            "bianco": 1,
            "rosso": 5,
            "blu": 10,
            "verde": 25,
            "nero": 100,
            "viola": 500,
            "giallo": 1000,
            "rosa": 5000,
            "azzurro": 10000
        }
    }

#Funzione per aggiungere un nuovo utente
def add_new_user():
    
    """Aggiunge un nuovo utente al sistema.
    
    Questa funzione raccoglie le informazioni dell'utente dal terminale,
    verifica se l'ID utente esiste già e, in caso contrario, aggiunge
    l'utente ai dati salvati."""

    user_id = input("Inserisci l'ID utente: ")
    if user_id not in user_data.data["users"]:
        first_name = input("Inserisci il nome dell'utente: ")
        last_name = input("Inserisci il cognome dell'utente: ")
        email = input("Inserisci l'email dell'utente: ")
        password = input("Inserisci la password dell'utente: ")
        while True:
            try:
                balance = float(input("Inserisci il saldo iniziale: "))
                break
            except ValueError:
                print("Errore: Inserisci un numero valido per il saldo iniziale.")
        payment_method = input("Inserisci il metodo di pagamento: ")
        user_data.add_user(user_id, f"{first_name} {last_name}", balance, email, password)
        print(f"Utente {first_name} {last_name} aggiunto con successo!")
    else:
        print(f"L'ID utente {user_id} esiste già.")

if __name__ == '__main__':
    add_new_user()

    #Ordina i valori delle fiches nell'ordine desiderato
    chip_order = ["bianco", "rosso", "blu", "verde", "nero", "viola", "giallo", "rosa", "azzurro"]
    sorted_chip_values = {}

    chips = chips_data()
    if "value_of_chips" in chips:
        for chip in chip_order:
            if chip in chips["value_of_chips"]:
                sorted_chip_values[chip] = chips["value_of_chips"][chip]

    #Crea una tabella per i valori delle fiches
    chip_table = []
    for chip in chip_order:
        if chip in sorted_chip_values:
            chip_table.append([chip, sorted_chip_values[chip]])

    print("Valori delle fiches:")
    print(tabulate(chip_table, headers=["Colore", "Valore"], tablefmt="grid"))

    #Crea una tabella per i dati degli utenti
    user_table = [["ID", "Nome", "Saldo", "Totale denaro", "Denaro rimanente", "Email", "Metodo di pagamento"]]
    for user_id, user_info in user_data.data["users"].items():
        user_table.append([
            user_id, 
            user_info["name"], 
            user_info["balance"], 
            user_info.get("total_money", "N/A"), 
            user_info.get("remaining_money", "N/A"), 
            user_info["email"], 
            user_info.get("payment_method", "N/A")  #Si usa "N/A" se "payment_method" non è presente
        ])

    print("\nDati degli utenti:")
    print(tabulate(user_table, headers="firstrow", tablefmt="grid"))

    #Ordina i valori delle carte per ordine di seme
    suit_order = ["Cuori", "Quadri", "Fiori", "Picche"]
    sorted_deck_data = {}

    for suit in suit_order:
        if suit in deck_data.deck_data:
            sorted_deck_data[suit] = deck_data.deck_data[suit]

    #Crea una tabella per i cuori
    hearts_table = []
    for card in sorted_deck_data["Cuori"]:
        hearts_table.append(["Cuori", card["value"]])

    #Crea una tabella per i quadri
    diamonds_table = []
    for card in sorted_deck_data["Quadri"]:
        diamonds_table.append(["Quadri", card["value"]])

    #Crea una tabella per i fiori
    clubs_table = []
    for card in sorted_deck_data["Fiori"]:
        clubs_table.append(["Fiori", card["value"]])

    #Crea una tabella per i picche
    spades_table = []
    for card in sorted_deck_data["Picche"]:
        spades_table.append(["Picche", card["value"]])

    #Stampa le tabelle affiancate
    print("\nDati del mazzo:")
    hearts_str = tabulate(hearts_table, headers=["Seme", "Valore"], tablefmt="grid").split("\n")
    diamonds_str = tabulate(diamonds_table, headers=["Seme", "Valore"], tablefmt="grid").split("\n")
    clubs_str = tabulate(clubs_table, headers=["Seme", "Valore"], tablefmt="grid").split("\n")
    spades_str = tabulate(spades_table, headers=["Seme", "Valore"], tablefmt="grid").split("\n")

    for h, d, c, s in zip(hearts_str, diamonds_str, clubs_str, spades_str):
        print(f"{h:<20} {d:<20} {c:<20} {s:<20}")