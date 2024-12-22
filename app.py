import sys
import os
from Flask import Flask, json, request, jsonify, render_template, redirect, url_for, flash

# Aggiungi il percorso della directory contenente user_data.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'python_files')))

from user_data import UserData
from deck_data import DeckData

app = Flask(__name__)
app.secret_key = "supersecretkey"

user_file = 'json/users_data.json'
deck_file = 'json/deck_into_json.json'

# Creazione automatica del file JSON degli utenti
if not os.path.exists(user_file):
    with open(user_file, 'w') as f:
        json.dump({"users": {}}, f, indent=4)

user_data = UserData(user_file)
deck_data = DeckData(deck_file)

@app.route("/")
def welcome():
    return render_template("welcome.html")

@app.route("/return_to_welcome")
def return_to_welcome():
    return render_template("return_to_welcome.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        password = request.form['psw']
        user_id = email  # Utilizziamo l'email come user_id
        balance = 1000  # Default balance

        if user_id in user_data.data["users"]:
            flash('Email already registered.')
        else:
            user_data.add_user(user_id, f"{fname} {lname}", balance, email, password)
            flash('User registered successfully.')
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['psw']

        if user_data.authenticate_user(email, password):
            flash('Login successful.')
            return redirect(url_for('welcome'))
        else:
            flash('Invalid email or password.')

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)