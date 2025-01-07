import json
import os
import hashlib
import time

class PasswordManager:
    def __init__(self, user_file_path):
        self.user_file_path = user_file_path
        self.user_data = self.load_user_data()

    #Funzione per caricare i dati degli utenti da un file JSON
    def load_user_data(self):
        
        """Carica i dati degli utenti da un file JSON.
        
        Questa funzione legge il file JSON specificato e carica i dati
        degli utenti. Se il file non esiste o è corrotto, viene
        restituito un dizionario con una chiave "users" vuota."""

        try:
            with open(self.user_file_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"users": {}}

    #Funzione per salvare i dati degli utenti in un file JSON
    def save_user_data(self):
        
        """Salva i dati degli utenti in un file JSON.
        
        Questa funzione scrive i dati degli utenti nel file JSON specificato,
        utilizzando una struttura JSON indentata per migliorare la leggibilità."""

        with open(self.user_file_path, 'w') as f:
            json.dump(self.user_data, f, indent=4)

    #Funzione per hashare una password utilizzando SHA-256
    def hash_password(self, password):
        
        """Crea un hash della password utilizzando l'algoritmo SHA-256.
        
        Questa funzione prende una password in chiaro, la codifica e genera
        un hash sicuro utilizzando SHA-256, rendendola sicura per l'archiviazione."""

        return hashlib.sha256(password.encode()).hexdigest()

    #Funzione per generare un token di reset per una password
    def generate_reset_token(self, email):
        
        """Genera un token di reset per la password di un utente.
        
        Questa funzione crea un token di reset univoco utilizzando l'email
        dell'utente e il timestamp corrente. Il token viene memorizzato nei
        dati dell'utente e restituito."""

        if email in self.user_data['users']:
            timestamp = str(int(time.time()))
            token = hashlib.sha256((email + timestamp).encode()).hexdigest()
            self.user_data['users'][email]['reset_token'] = token
            self.save_user_data()
            return token
        return None

    #Funzione per verificare un token di reset
    def verify_reset_token(self, token):
        
        """Verifica un token di reset della password.
        
        Questa funzione verifica se un token di reset corrisponde a uno
        memorizzato nei dati degli utenti. Restituisce l'email dell'utente
        se il token è valido, altrimenti None."""

        for email, user in self.user_data['users'].items():
            if user.get('reset_token') == token:
                return email
        return None

    #Funzione per resettare la password utilizzando un token di reset
    def reset_password(self, token, new_password):
        
        """Resetta la password di un utente utilizzando un token di reset.
        
        Questa funzione verifica il token di reset, aggiorna la password
        dell'utente con una nuova password hashata e rimuove il token di reset
        dai dati dell'utente."""

        email = self.verify_reset_token(token)
        if email:
            self.user_data['users'][email]['password'] = self.hash_password(new_password)
            del self.user_data['users'][email]['reset_token']
            self.save_user_data()
            return True
        return False