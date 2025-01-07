import json
import os

class DeckData:
    def __init__(self, deck_file_path):
        self.deck_file_path = deck_file_path
        self.deck_data = self.load_deck_data()

    #Funzione per caricare i dati del mazzo di carte
    def load_deck_data(self):
        
        """Carica i dati del mazzo di carte dal file JSON.
        
        Questa funzione verifica se il file esiste e, in caso affermativo, 
        legge i dati del mazzo di carte dal file JSON. Altrimenti, crea un 
        mazzo di carte predefinito."""

        if os.path.exists(self.deck_file_path):
            with open(self.deck_file_path, 'r') as f:
                return json.load(f)
        else:
            return self.create_default_deck_data()

    #Funzione per salvare i dati del mazzo di carte in un file JSON
    def save_deck_data(self):
        
        """Salva i dati del mazzo di carte in un file JSON.
        
        Questa funzione scrive i dati del mazzo di carte nel file specificato 
        utilizzando una struttura JSON indentata per migliorare la leggibilità."""

        with open(self.deck_file_path, 'w') as f:
            json.dump(self.deck_data, f, indent=4)

    #Funzione per creare i dati predefiniti del mazzo di carte
    def create_default_deck_data(self):
        
        """Crea i dati predefiniti del mazzo di carte.
        
        Questa funzione genera i dati predefiniti per un mazzo di carte, 
        includendo sia i valori numerici che quelli delle figure per ogni seme."""

        #Crea una lista di valori numerici per le carte
        numeric_values = []
        for i in range(2, 11):
            numeric_values.append(str(i))
        print(numeric_values)

        #Crea una lista di valori delle figure per le carte
        face_values = ["J", "Q", "K", "A"]

        #Combina i valori numerici e delle figure
        all_values = numeric_values + face_values

        #Funzione per creare i dati del seme
        def create_suit_data(values):
            
            """Crea i dati del seme.
            
            Questa funzione genera una lista di dizionari, ognuno dei quali rappresenta una carta 
            con il valore specificato."""

            suit_data = []
            for value in values:
                card = {"value": value}
                suit_data.append(card)
            return suit_data

        #Usa la funzione per creare i dizionari per ogni seme
        hearts = create_suit_data(all_values)
        diamonds = create_suit_data(all_values)
        clubs = create_suit_data(all_values)
        spades = create_suit_data(all_values)

        #Combina i dizionari in un unico dizionario per il mazzo di carte
        deck_data = {
            "Hearts": hearts,
            "Diamonds": diamonds,
            "Clubs": clubs,
            "Spades": spades
        }

        self.deck_data = deck_data
        self.save_deck_data()
        return deck_data