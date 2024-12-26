import json
from tabulate import tabulate
from user_data import UserData
from deck_data import DeckData

user_file = '\\Christmas-project\\json\\users.json'  # Assicurati che il file sia users.json
deck_file = '\\Christmas-project\\json\\deck_into_json.json'

user_data = UserData(user_file)
deck_data = DeckData(deck_file)

def chips_data():
    return {
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

# Function to add a new user
def add_new_user():
    user_id = input("Enter user ID: ")
    if user_id not in user_data.data["users"]:
        first_name = input("Enter user's first name: ")
        last_name = input("Enter user's last name: ")
        email = input("Enter user's email: ")
        password = input("Enter user's password: ")
        while True:
            try:
                balance = float(input("Enter initial balance: "))
                break
            except ValueError:
                print("Error: Please enter a valid number for the initial balance.")
        payment_method = input("Enter payment method: ")
        user_data.add_user(user_id, f"{first_name} {last_name}", balance, email, password)
        print(f"User {first_name} {last_name} added successfully!")
    else:
        print(f"User ID {user_id} already exists.")

if __name__ == '__main__':
    # Add a new user via terminal input
    add_new_user()

    # Sort chip values in the desired order
    chip_order = ["white", "red", "blue", "green", "black", "purple", "yellow", "pink", "light blue"]
    sorted_chip_values = {}

    chips = chips_data()
    if "value_of_chips" in chips:
        for chip in chip_order:
            if chip in chips["value_of_chips"]:
                sorted_chip_values[chip] = chips["value_of_chips"][chip]

    # Create a table for chip values
    chip_table = []
    for chip in chip_order:
        if chip in sorted_chip_values:
            chip_table.append([chip, sorted_chip_values[chip]])

    print("Chip values:")
    print(tabulate(chip_table, headers=["Color", "Value"], tablefmt="grid"))

    # Create a table for user data
    user_table = [["ID", "Name", "Balance", "Total Money", "Remaining Money", "Email", "Payment Method"]]
    for user_id, user_info in user_data.data["users"].items():
        user_table.append([
            user_id, 
            user_info["name"], 
            user_info["balance"], 
            user_info.get("total_money", "N/A"), 
            user_info.get("remaining_money", "N/A"), 
            user_info["email"], 
            user_info.get("payment_method", "N/A")  # Usa "N/A" se "payment_method" non è presente
        ])

    print("\nUser data:")
    print(tabulate(user_table, headers="firstrow", tablefmt="grid"))

    # Sort card values by suit order
    suit_order = ["Hearts", "Diamonds", "Clubs", "Spades"]
    sorted_deck_data = {}

    for suit in suit_order:
        if suit in deck_data.deck_data:
            sorted_deck_data[suit] = deck_data.deck_data[suit]

    # Create a table for hearts
    hearts_table = []
    for card in sorted_deck_data["Hearts"]:
        hearts_table.append(["Hearts", card["value"]])

    # Create a table for diamonds
    diamonds_table = []
    for card in sorted_deck_data["Diamonds"]:
        diamonds_table.append(["Diamonds", card["value"]])

    # Create a table for clubs
    clubs_table = []
    for card in sorted_deck_data["Clubs"]:
        clubs_table.append(["Clubs", card["value"]])

    # Create a table for spades
    spades_table = []
    for card in sorted_deck_data["Spades"]:
        spades_table.append(["Spades", card["value"]])

    # Print the tables side by side
    print("\nDeck data:")
    hearts_str = tabulate(hearts_table, headers=["Suit", "Value"], tablefmt="grid").split("\n")
    diamonds_str = tabulate(diamonds_table, headers=["Suit", "Value"], tablefmt="grid").split("\n")
    clubs_str = tabulate(clubs_table, headers=["Suit", "Value"], tablefmt="grid").split("\n")
    spades_str = tabulate(spades_table, headers=["Suit", "Value"], tablefmt="grid").split("\n")

    for h, d, c, s in zip(hearts_str, diamonds_str, clubs_str, spades_str):
        print(f"{h:<20} {d:<20} {c:<20} {s:<20}")