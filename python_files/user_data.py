import json
import os
import hashlib

class UserData:
    def __init__(self, user_file_path):
        self.user_file_path = os.path.join('\\Christmas-project\\json', user_file_path)
        self.data = self.load_data()

    #Funzione per caricare i dati dal file JSON
    def load_data(self):

        """Carica i dati dal file JSON. Crea un file predefinito se non esiste."""
        
        if os.path.exists(self.user_file_path):
            with open(self.user_file_path, 'r') as f:
                return json.load(f)
        else:
            self.create_default_data()
            return {"users": {}}

    #Funzione per creare un file JSON con dati predefiniti
    def create_default_data(self):

        """Crea un file JSON con dati predefiniti."""

        default_data = {"users": {}}
        if os.path.dirname(self.user_file_path):
            os.makedirs(os.path.dirname(self.user_file_path), exist_ok=True)
        with open(self.user_file_path, 'w') as f:
            json.dump(default_data, f, indent=4)

    #Funzione per salvare i dati nel file JSON
    def save_data(self):

        """Salva i dati nel file JSON."""

        if os.path.dirname(self.user_file_path):
            os.makedirs(os.path.dirname(self.user_file_path), exist_ok=True)
        with open(self.user_file_path, 'w') as f:
            json.dump(self.data, f, indent=4)

    #Funzione per hashare una password utilizzando SHA-256
    def hash_password(self, password):

        """Genera un hash della password utilizzando SHA-256."""

        return hashlib.sha256(password.encode()).hexdigest()

    #Funzione per aggiungere un nuovo utente
    def add_user(self, user_id, name, balance, email, password):

        """Aggiunge un nuovo utente ai dati e salva nel file JSON."""

        if not user_id:
            raise ValueError("User ID is required.")
        if not name:
            raise ValueError("Name is required.")
        if not email:
            raise ValueError("Email is required.")
        if not password:
            raise ValueError("Password is required.")
        if user_id in self.data["users"]:
            raise ValueError("User ID already exists.")
        hashed_password = self.hash_password(password)
        self.data["users"][user_id] = {
            'name': name,
            'balance': balance,
            'total_money': balance,
            'remaining_money': balance,
            'email': email,
            'password': hashed_password,
            'payment_method': None,  #Imposta il metodo di pagamento a None inizialmente
            'wins_losses': {}
        }
        self.save_data()

    #Funzione per autenticare un utente
    def authenticate_user(self, user_id, password):

        """Autentica un utente utilizzando l'ID e la password."""

        if not user_id:
            raise ValueError("User ID is required.")
        if not password:
            raise ValueError("Password is required.")
        if user_id in self.data["users"]:
            stored_password = self.data["users"][user_id]['password']
            return stored_password == self.hash_password(password)
        return False

    #Funzione per aggiornare la password di un utente
    def update_password(self, user_id, new_password):

        """Aggiorna la password di un utente."""

        if not user_id:
            raise ValueError("User ID is required.")
        if not new_password:
            raise ValueError("New password is required.")
        if user_id in self.data["users"]:
            hashed_password = self.hash_password(new_password)
            self.data["users"][user_id]['password'] = hashed_password
            self.save_data()
            return True
        return False

    #Funzione per elaborare una transazione (deposito o prelievo)
    def process_transaction(self, user_id, amount, transaction_type):

        """Elabora una transazione di deposito o prelievo."""

        if not user_id:
            raise ValueError("User ID is required.")
        if amount is None:
            raise ValueError("Amount is required.")
        if user_id in self.data["users"]:
            if transaction_type == 'deposit':
                self.data["users"][user_id]['balance'] += amount
            elif transaction_type == 'withdraw':
                if self.data["users"][user_id]['balance'] >= amount:
                    self.data["users"][user_id]['balance'] -= amount
                else:
                    raise ValueError("Insufficient balance")
            self.save_data()
        else: raise ValueError("User ID does not exist.")

    #Funzione per aggiornare il saldo di un utente
    def update_balance(self, user_id, amount):

        """Aggiorna il saldo di un utente."""

        if not user_id:
            raise ValueError("User ID is required.")
        if amount is None:
            raise ValueError("Amount is required.")
        if user_id in self.data["users"]:
            self.data["users"][user_id]['balance'] += amount
            self.save_data()
        else: raise ValueError("User ID does not exist.")

    #Funzione per eliminare un utente
    def delete_user(self, user_id):

        """Elimina un utente dai dati."""

        if not user_id:
            raise ValueError("User ID is required.")
        if user_id in self.data["users"]:
            del self.data["users"][user_id]
            self.save_data()
            return True
        else: raise ValueError("User ID does not exist.")