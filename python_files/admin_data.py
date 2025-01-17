import json
import os
import hashlib

class AdminData:
    def __init__(self, admin_file_path):
        self.admin_file_path = admin_file_path
        self.admin_data = self.load_admin_data()

    #Funzione per caricare i dati dell'amministratore dal file JSON
    def load_admin_data(self):
        
        """Carica i dati dell'amministratore dal file JSON.
        
        Questa funzione tenta di leggere il file JSON contenente i dati
        dell'amministratore. Se il file non esiste o è vuoto, viene restituito
        un dizionario con una chiave "admin" vuota."""
        
        try:
            with open(self.admin_file_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"admin": {}}

    #Funzione per salvare i dati dell'amministratore nel file JSON
    def save_admin_data(self):
        
        """Salva i dati dell'amministratore nel file JSON.
        Questa funzione scrive i dati dell'amministratore nel file specificato
        utilizzando una struttura JSON indentata per migliorare la leggibilità."""

        with open(self.admin_file_path, 'w') as f:
            json.dump(self.admin_data, f, indent=4)

    #Funzione per hashare una password utilizzando SHA-256
    def hash_password(self, password):
        
        """Crea un hash della password utilizzando l'algoritmo SHA-256.
        Questa funzione prende una password in chiaro, la codifica e genera
        un hash sicuro utilizzando SHA-256, rendendola sicura per l'archiviazione."""

        return hashlib.sha256(password.encode()).hexdigest()

    #Funzione per verificare le credenziali dell'amministratore
    def verify_admin(self, email, password):
        
        """Verifica le credenziali dell'amministratore.
        
        Questa funzione confronta l'email e la password fornite con quelle
        memorizzate nel file JSON. Restituisce True se le credenziali sono
        corrette, altrimenti False."""

        admin = self.admin_data.get("admin")
        if admin and admin["email"] == email and admin["password"] == self.hash_password(password):
            return True
        return False

    #Funzione per impostare le credenziali dell'amministratore
    def set_admin(self, email, password):
        
        """Imposta le credenziali dell'amministratore.
        
        Questa funzione memorizza l'email e la password hashata nel file JSON
        per l'amministratore. Utilizzata per configurare inizialmente o
        aggiornare le credenziali amministrative."""

        self.admin_data["admin"] = {
            "email": email,
            "password": self.hash_password(password)
        }
        self.save_admin_data()

    #Funzione per creare le credenziali dell'amministratore se non esistono
    def create_admin_if_not_exists(self, email, password):
        
        """Crea le credenziali dell'amministratore se non esistono.
        
        Questa funzione verifica se il file JSON con le credenziali
        amministrative esiste. Se non esiste, imposta le credenziali
        amministrative con l'email e la password fornite."""

        if not os.path.exists(self.admin_file_path):
            self.set_admin(email, password)
            print(f"Admin credentials created: {email} / {password}")

#Esempio di utilizzo dell'amministratore
if __name__ == "__main__":
    admin_file_path = os.path.join(os.path.dirname(__file__), '../json', 'admin.json')
    admin_data = AdminData(admin_file_path)
    
    #Inserimento delle credenziali dell'amministratore tramite il terminale
    email = input("Enter admin email: ")
    password = input("Enter admin password: ")
    
    admin_data.set_admin(email, password)
    print("Admin credentials set successfully.")
    
    #Verifica delle credenziali dell'amministratore
    email_verifica = input("Verify - Enter admin email: ")
    password_verifica = input("Verify - Enter admin password: ")
    
    if admin_data.verify_admin(email_verifica, password_verifica):
        print("Verification successful: credentials are correct.")
    else: print("Verification failed: credentials are incorrect.")