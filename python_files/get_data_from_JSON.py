import json
from tabulate import tabulate
from user_data import UserData
from deck_data import DeckData

user_file = '../json/users_data.json'
deck_file = '../json/deck_into_json.json'

user_data = UserData(user_file)
deck_data = DeckData(deck_file)
user_data.add_user('001', 'Mario Rossi', 1000, 'mario.rossi@example.com', 'credit card')

# Ordina i valori delle fiches in base all'ordine desiderato
chip_order = ["white", "red", "blue", "green", "black", "purple", "yellow", "pink", "light blue"]
sorted_chip_values = {}

# Crea i valori delle fiches
chips_data = {
    "value_of_chips": {
        "white": 1,
        "red": 5,
        "blue": 10,
        "green": 25,
        "black": 100,
        "purple": 500,
        "yellow": 1000,
        "pink": 5000,
        "light blue": 10000
    }
}

if "value_of_chips" in chips_data:
    for chip in chip_order:
        if chip in chips_data["value_of_chips"]:
            sorted_chip_values[chip] = chips_data["value_of_chips"][chip]

# Crea una tabella per i valori delle fiches
chip_table = []
for chip in chip_order:
    if chip in sorted_chip_values:
        chip_table.append([chip, sorted_chip_values[chip]])

print("Chip values:")
print(tabulate(chip_table, headers=["Color", "Value"], tablefmt="grid"))

# Crea una tabella per i dati dell'utente
user_table = [["ID", "Name", "Balance", "Total Money", "Remaining Money", "Email", "Payment Method"], 
              ["001", user_data.data["users"]["001"]["name"], user_data.data["users"]["001"]["balance"], 
               user_data.data["users"]["001"]["total_money"], user_data.data["users"]["001"]["remaining_money"], 
               user_data.data["users"]["001"]["email"], user_data.data["users"]["001"]["payment_method"]]]
print("\nUser data:")
print(tabulate(user_table, headers="firstrow", tablefmt="grid"))

# Ordina i valori delle carte in base all'ordine dei semi
suit_order = ["Hearts", "Diamonds", "Clubs", "Spades"]
sorted_deck_data = {}

for suit in suit_order:
    if suit in deck_data.deck_data:
        sorted_deck_data[suit] = deck_data.deck_data[suit]

# Crea una tabella per i cuori
hearts_table = []
for card in sorted_deck_data["Hearts"]:
    hearts_table.append(["Hearts", card["value"]])

# Crea una tabella per i diamanti
diamonds_table = []
for card in sorted_deck_data["Diamonds"]:
    diamonds_table.append(["Diamonds", card["value"]])

# Crea una tabella per i fiori
clubs_table = []
for card in sorted_deck_data["Clubs"]:
    clubs_table.append(["Clubs", card["value"]])

# Crea una tabella per le picche
spades_table = []
for card in sorted_deck_data["Spades"]:
    spades_table.append(["Spades", card["value"]])

# Stampa le tabelle affiancate
print("\nDeck data:")
hearts_str = tabulate(hearts_table, headers=["Suit", "Value"], tablefmt="grid").split("\n")
diamonds_str = tabulate(diamonds_table, headers=["Suit", "Value"], tablefmt="grid").split("\n")
clubs_str = tabulate(clubs_table, headers=["Suit", "Value"], tablefmt="grid").split("\n")
spades_str = tabulate(spades_table, headers=["Suit", "Value"], tablefmt="grid").split("\n")

for h, d, c, s in zip(hearts_str, diamonds_str, clubs_str, spades_str):
    print(f"{h:<20} {d:<20} {c:<20} {s:<20}")