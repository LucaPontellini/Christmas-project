import json
from tabulate import tabulate
from get_data_from_JSON import user_data

class PaymentMethod:
    def __init__(self, name, transaction_fee):
        self.name = name
        self.transaction_fee = transaction_fee

    #Funzione per convertire i dettagli del metodo di pagamento in un dizionario
    def to_dict(self):
        
        """Converte i dettagli del metodo di pagamento in un dizionario.
        
        Questa funzione restituisce un dizionario contenente il nome del metodo di pagamento
        e la sua commissione di transazione."""
        
        return {
            "name": self.name,
            "transaction_fee": self.transaction_fee
        }

class PaymentManager:
    def __init__(self):
        self.payment_methods = []

    #Funzione per aggiungere un metodo di pagamento
    def add_payment_method(self, payment_method):
        
        """Aggiunge un nuovo metodo di pagamento alla lista e lo salva nel file JSON.
        
        Questa funzione prende un oggetto PaymentMethod e lo aggiunge alla lista dei metodi di pagamento,
        quindi salva l'elenco aggiornato nel file JSON."""

        self.payment_methods.append(payment_method)
        self.save_to_json('\\Christmas-project\\json\\payment_methods.json')

    #Funzione per rimuovere un metodo di pagamento per nome
    def remove_payment_method(self, name):
        
        """Rimuove un metodo di pagamento dalla lista in base al nome e salva le modifiche nel file JSON.
        
        Questa funzione rimuove il metodo di pagamento che corrisponde al nome specificato dalla lista dei metodi
        di pagamento, quindi salva l'elenco aggiornato nel file JSON."""

        new_payment_methods = []
        for pm in self.payment_methods:
            if pm.name != name:
                new_payment_methods.append(pm)
        self.payment_methods = new_payment_methods
        self.save_to_json('\\Christmas-project\\json\\payment_methods.json')

    #Funzione per ottenere un metodo di pagamento per nome
    def get_payment_method(self, name):
        
        """Restituisce un metodo di pagamento in base al nome.
        
        Questa funzione cerca nella lista dei metodi di pagamento e restituisce quello che corrisponde
        al nome specificato. Se non viene trovato, restituisce None."""

        for pm in self.payment_methods:
            if pm.name == name:
                return pm
        return None

    #Funzione per caricare i metodi di pagamento da un file JSON
    def load_from_json(self, file_path):
        
        """Carica i metodi di pagamento da un file JSON.
        
        Questa funzione legge un file JSON e carica i metodi di pagamento nella lista dei metodi di pagamento."""

        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            for pm in data:
                self.add_payment_method(PaymentMethod(pm['name'], pm['transaction_fee']))

    #Funzione per salvare i metodi di pagamento in un file JSON
    def save_to_json(self, file_path):
        
        """Salva i metodi di pagamento in un file JSON.
        
        Questa funzione converte la lista dei metodi di pagamento in un formato JSON e la salva nel file specificato."""

        with open(file_path, 'w') as json_file:
            data = [pm.to_dict() for pm in self.payment_methods]
            json.dump(data, json_file, indent=4)

class CasinoCashier:
    def __init__(self, payment_manager):
        self.payment_manager = payment_manager

    #Funzione per scambiare denaro per fiches
    def exchange_money_for_chips(self, amount, payment_method_name):
        
        """Scambia denaro per fiches utilizzando un metodo di pagamento specifico.
        
        Questa funzione calcola il numero di fiches ottenibili in base all'importo fornito e alla commissione
        di transazione del metodo di pagamento specificato."""

        payment_method = self.payment_manager.get_payment_method(payment_method_name)
        if payment_method:
            final_amount = amount - (amount * payment_method.transaction_fee / 100)
            chips = final_amount // 1  #Si assume che 1 fiche valga $1
            return chips
        else:
            return 0

    #Funzione per scambiare fiches per denaro
    def exchange_chips_for_money(self, chips, payment_method_name):
        
        """Scambia fiches per denaro utilizzando un metodo di pagamento specifico.
        
        Questa funzione calcola l'importo di denaro ottenibile in base al numero di fiches fornite e alla commissione
        di transazione del metodo di pagamento specificato."""

        payment_method = self.payment_manager.get_payment_method(payment_method_name)
        if payment_method:
            amount = chips * 1  #Si assume che 1 fiche valga $1
            final_amount = amount - (amount * payment_method.transaction_fee / 100)
            return final_amount
        else:
            return 0