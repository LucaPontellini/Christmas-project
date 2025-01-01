import json
import os

def generate_earnings_json(file_path):
    user_file = '../json/users.json'
    
    if not os.path.exists(user_file):
        with open(user_file, 'w') as f:
            json.dump({"users": {}}, f, indent=4)
    
    with open(user_file, 'r') as f:
        user_data = json.load(f)
    
    if not user_data["users"]:
        print("No users found. Cannot generate earnings data.")
        return
    
    # Calcolo dei guadagni basati sui dati simulati
    earnings_data = {}
    months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    
    for month in months:
        monthly_earnings = 0
        for user_id in user_data["users"]:
            monthly_earnings += user_data["users"][user_id]['balance']
        earnings_data[month] = monthly_earnings

    # Scrittura dei dati dei guadagni nel file JSON
    with open(file_path, 'w') as json_file:
        json.dump(earnings_data, json_file, indent=4)
    print(f"Earnings data has been written to {file_path}")

if __name__ == "__main__":
    generate_earnings_json('../json/earnings.json')