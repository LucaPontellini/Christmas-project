import json
import os

class DeckData:
    def __init__(self, deck_file_path):
        self.deck_file_path = deck_file_path
        self.deck_data = self.load_deck_data()

    def load_deck_data(self):
        if os.path.exists(self.deck_file_path):
            with open(self.deck_file_path, 'r') as f:
                return json.load(f)
        else:
            return self.create_default_deck_data()

    def save_deck_data(self):
        with open(self.deck_file_path, 'w') as f:
            json.dump(self.deck_data, f, indent=4)

    def create_default_deck_data(self):
        # Crea una lista di valori numerici per le carte
        numeric_values = [str(i) for i in range(2, 11)]

        # Crea una lista di valori delle figure per le carte
        face_values = ["J", "Q", "K", "A"]

        # Combina i valori numerici e delle figure
        all_values = numeric_values + face_values

        # Crea una funzione per generare il dizionario delle carte per un seme
        def create_suit_data(values):
            return [{"value": value} for value in values]

        # Usa la funzione per creare i dizionari per ogni seme
        hearts = create_suit_data(all_values)
        diamonds = create_suit_data(all_values)
        clubs = create_suit_data(all_values)
        spades = create_suit_data(all_values)

        # Combina i dizionari in un unico dizionario per il mazzo di carte
        deck_data = {
            "Hearts": hearts,
            "Diamonds": diamonds,
            "Clubs": clubs,
            "Spades": spades
        }

        self.deck_data = deck_data
        self.save_deck_data()
        return deck_data