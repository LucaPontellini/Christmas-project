import sys
import os
from flask import Flask, jsonify, render_template, redirect, send_from_directory, url_for, request, make_response
import json
import hashlib
import logging
from datetime import datetime

# Configura il logging
logging.basicConfig(level=logging.DEBUG)

# Percorso relativo alla directory python_files
sys.path.append(os.path.join(os.path.dirname(__file__), 'python_files'))

from user_data import UserData
from get_data_from_JSON import chips_data
from deck_data import DeckData
from admin_data import AdminData
from password_manager import PasswordManager

app = Flask(__name__)
#Variabile temporanea per memorizzare la password in chiaro
temporary_password = None

# Percorso del file JSON degli utenti
user_file_path = os.path.join(os.path.dirname(__file__), 'json', 'users.json')

# Percorso del file JSON del mazzo di carte
deck_file_path = os.path.join(os.path.dirname(__file__), 'json', 'deck_into_json.json')

# Percorso del file JSON degli amministratori
admin_file_path = os.path.join(os.path.dirname(__file__), 'json', 'admin.json')

# Percorso del file JSON degli account eliminati
deleted_users_file_path = os.path.join(os.path.dirname(__file__), 'json', 'deleted_users.json')

user_data = UserData(user_file_path)
deck_data = DeckData(deck_file_path)
admin_data_instance = AdminData(admin_file_path)
password_manager = PasswordManager(user_file_path)

def load_user_data():
    try:
        with open(user_file_path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"users": {}}

def save_user_data(data):
    with open(user_file_path, 'w') as f:
        json.dump(data, f, indent=4)

def load_plain_password(email):
    json_path = os.path.join('json', 'plain_passwords.json')
    if not os.path.exists(json_path):
        with open(json_path, 'w') as file:
            json.dump({}, file)
    with open(json_path, 'r') as file:
        try:
            plain_passwords = json.load(file)
        except json.JSONDecodeError:
            plain_passwords = {}
    return plain_passwords.get(email)

# Funzione per salvare la password in chiaro in un file JSON separato
def save_plain_password(email, password):
    json_path = os.path.join('json', 'plain_passwords.json')
    if not os.path.exists(json_path):
        with open(json_path, 'w') as file:
            json.dump({}, file)
    with open(json_path, 'r') as file:
        try:
            plain_passwords = json.load(file)
        except json.JSONDecodeError:
            plain_passwords = {}
    plain_passwords[email] = password
    with open(json_path, 'w') as file:
        json.dump(plain_passwords, file, indent=4)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_admin_if_not_exists():
    admin_data_instance.create_admin_if_not_exists('admin@lucapontellini.com', 'Gp!7fhD^*3nVq9E')

def load_admin_data():
    with open('json/admin.json', 'r') as file:
        return json.load(file)

def verify_admin(email, password):
    admin_data = load_admin_data()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return email == admin_data['admin']['email'] and hashed_password == admin_data['admin']['password']

def load_deleted_user_data():
    json_path = os.path.join('json', 'deleted_users.json')
    if not os.path.exists(json_path):
        with open(json_path, 'w') as file:
            json.dump({"users": {}}, file)
    try:
        with open(json_path, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        return {"users": {}}

def save_deleted_user_data(data):
    json_path = os.path.join('json', 'deleted_users.json')
    with open(json_path, 'w') as file:
        json.dump(data, file, indent=4)

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/return_to_welcome')
def return_to_welcome():
    return redirect(url_for('welcome'))

@app.route('/casino_home')
def casino_home():
    email = request.cookies.get('email')
    is_admin = request.cookies.get('is_admin')
    logging.debug(f"casino_home: email={email}, is_admin={is_admin}")
    return render_template('casino_home.html', email=email, is_admin=is_admin)

@app.route('/return_to_casino_home')
def return_to_casino_home():
    return redirect(url_for('casino_home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    global temporary_password
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        
        if not email or not password or not name:
            return jsonify({'error_message': 'All fields are required.'})
        
        user_data = load_user_data()
        
        if email in user_data['users']:
            return jsonify({'error_message': 'Email already registered. Please log in.'})
        
        # Hash della password
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        user_data['users'][email] = {
            'name': name,
            'email': email,
            'password': password_hash,
            'is_admin': False,
            'user_chips': {
                'white': 0,
                'red': 0,
                'blue': 0,
                'green': 0,
                'black': 0,
                'purple': 0,
                'yellow': 0,
                'pink': 0,
                'light_blue': 0
            },
            'total_money': 0,
            'remaining_money': 0,
            'registration_date': datetime.now().strftime('%Y-%m-%d')
        }
        
        save_user_data(user_data)
        # Salva la password in chiaro nel file JSON separato
        save_plain_password(email, password)
        response = make_response(jsonify({'redirect_url': url_for('casino_home')}))
        response.set_cookie('email', email)
        response.set_cookie('is_admin', 'False')
        logging.debug(f"register: email={email} cookie set")
        return response
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    global temporary_password
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            return render_template('login.html', error_message='Email and password are required.')

        user_data = load_user_data()
        user = user_data['users'].get(email)
        
        if user:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            if hashed_password == user['password']:
                temporary_password = password
                response = make_response(redirect(url_for('account')))
                response.set_cookie('email', email)
                return response
        elif verify_admin(email, password):
            response = make_response(redirect(url_for('admin_dashboard')))
            response.set_cookie('email', email)
            response.set_cookie('is_admin', 'True')
            return response
        return render_template('login.html', error_message='Invalid email or password.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('welcome')))
    response.delete_cookie('email')
    response.delete_cookie('is_admin')
    return response

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        user_data = load_user_data()
        if email in user_data['users']:
            token = password_manager.generate_reset_token(email)
            if token:
                reset_link = url_for('reset_password', token=token, _external=True)
                logging.debug(f"Password reset link sent to {email}: {reset_link}")
                return render_template('forgot_password.html', success_message='Password reset link has been sent to your email.', reset_link=reset_link)
        else:
            return render_template('forgot_password.html', error_message='Email not found.')
    
    return render_template('forgot_password.html')

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if request.method == 'POST':
        new_password = request.form['new_password']
        email = password_manager.verify_reset_token(token)
        if email:
            user_data = load_user_data()
            if email in user_data['users']:
                user_data['users'][email]['password'] = hash_password(new_password)
                save_user_data(user_data)
                
                # Aggiorna anche il file JSON con le password in chiaro
                save_plain_password(email, new_password)
                
                logging.debug(f"Password reset for {email}")
                return redirect(url_for('login'))
        return render_template('reset_password.html', error_message='Invalid or expired token.')
    
    return render_template('reset_password.html', token=token)

@app.route('/poker_rules')
def poker_rules():
    return render_template('poker_rules.html')

@app.route('/cashier_dashboard', methods=['GET', 'POST'])
def cashier_dashboard():
    email = request.cookies.get('email')
    logging.debug(f"cashier_dashboard: email={email}")
    
    if not email: 
        return redirect(url_for('register'))
    
    user_data = load_user_data()
    user = user_data['users'].get(email)
    
    if not user: 
        return redirect(url_for('register'))
    
    total_money = user['total_money']
    remaining_money = user['remaining_money']
    
    if request.method == 'POST':
        total_money = request.form.get('total_money', type=int, default=total_money)
        remaining_money = request.form.get('remaining_money', type=int, default=remaining_money)
    
    return render_template(
        'cashier_operations.html',
        username=user['name'],
        value_of_chips=chips_data()["value_of_chips"],
        total_money=total_money,
        remaining_money=remaining_money)

@app.route('/convert_to_chips', methods=['POST'])
def convert_to_chips():
    email = request.cookies.get('email')
    logging.debug(f"convert_to_chips: email={email}")
    
    if not email:
        return jsonify({"error_message": "User not authenticated."})
    
    user_data = load_user_data()
    user = user_data['users'].get(email)
    
    if not user:
        return jsonify({"error_message": "User not found."})
    
    try:
        amount_str = request.form['amount']
        chip_color = request.form['chip-color']
        
        if not amount_str.strip():
            return jsonify({"error_message": "Please enter a valid amount."})
        
        amount = int(amount_str)
        chip_value = chips_data()["value_of_chips"].get(chip_color)
        
        if not chip_value:
            return jsonify({"error_message": "Invalid chip color selected."})
        
        total_cost = amount * chip_value
        
        if total_cost > user["remaining_money"]:
            return jsonify({"error_message": "Insufficient funds."})
    
    except KeyError:
        return jsonify({"error_message": "Please enter a valid amount and select a chip color."})
    
    except ValueError as e:
        return jsonify({"error_message": str(e)})
    
    user["remaining_money"] -= total_cost
    user["user_chips"][chip_color] += amount
    save_user_data(user_data)
    
    return jsonify({
        "error_message": "",
        "value_of_chips": chips_data()["value_of_chips"],
        "total_money": user["total_money"],
        "remaining_money": user["remaining_money"]
    })

@app.route('/home_poker')
def home_poker():
    return render_template('home_poker.html')

@app.route('/play')
def play():
    email = request.cookies.get('email')
    logging.debug(f"play: email={email}")
    
    if not email:
        error_message = "You need to be logged in to play."
        redirect_url = url_for('register')
        return render_template('home_poker.html', error_message=error_message, redirect_url=redirect_url)
    
    user_data = load_user_data()
    user = user_data['users'].get(email)
    
    if not user:
        error_message = "User not found."
        redirect_url = url_for('register')
        return render_template('home_poker.html', error_message=error_message, redirect_url=redirect_url)
    
    return render_template('play.html', user=user)

@app.route("/update_total_money", methods=["POST"])
def update_total_money():
    email = request.cookies.get('email')
    logging.debug(f"update_total_money: email={email}")
    
    if not email:
        return jsonify({"error_message": "User not authenticated."})
    
    user_data = load_user_data()
    user = user_data['users'].get(email)
    
    if not user:
        return jsonify({"error_message": "User not found."})
    
    payment_method = request.form.get('payment_method')
    if not payment_method:
        return jsonify({"error_message": "Please select a payment method."})
    
    new_total_money_str = request.form.get("total_money", "")
    if not new_total_money_str.strip():
        return jsonify({"error_message": "Please enter a valid amount."})
    
    try:
        new_total_money = int(new_total_money_str)
    except ValueError:
        return jsonify({"error_message": "Error: The amount must be an integer."})
    
    user["total_money"] = new_total_money
    user["remaining_money"] = new_total_money
    user["payment_method"] = payment_method

    save_user_data(user_data)
    
    return jsonify({
        "error_message": "",
        "value_of_chips": chips_data()["value_of_chips"],
        "total_money": user["total_money"],
        "remaining_money": user["remaining_money"]
    })

@app.route("/clear_all_data", methods=["POST"])
def clear_all_data():
    email = request.cookies.get('email')
    logging.debug(f"clear_all_data: email={email}")
    
    if not email:
        return jsonify({"error_message": "User not authenticated."})
    
    user_data = load_user_data()
    user = user_data['users'].get(email)
    
    if not user:
        return jsonify({"error_message": "User not found."})
    
    # Verifica se il denaro totale è zero
    total_money_is_zero = user["total_money"] == 0
    
    # Verifica se il denaro rimanente è zero
    remaining_money_is_zero = user["remaining_money"] == 0
    
    # Verifica se tutte le quantità di fiches sono zero
    all_chips_are_zero = all(quantity == 0 for quantity in user["user_chips"].values())
    
    # Se tutte le condizioni sono vere, non c'è nulla da eliminare
    if total_money_is_zero and remaining_money_is_zero and all_chips_are_zero:
        return jsonify({"error_message": "There is no data to clear."})
    
    # Procedi con la cancellazione dei dati
    user["user_chips"] = {
        "white": 0,
        "red": 0,
        "blue": 0,
        "green": 0,
        "black": 0,
        "purple": 0,
        "yellow": 0,
        "pink": 0,
        "light blue": 0,
    }
    user["total_money"] = 0
    user["remaining_money"] = 0
    
    save_user_data(user_data)
    
    return jsonify({
        "error_message": "",
        "value_of_chips": chips_data()["value_of_chips"],
        "total_money": user["total_money"],
        "remaining_money": user["remaining_money"]
    })

# Funzione per la rotta '/reconvert'
@app.route("/reconvert", methods=["POST"])
def reconvert():
    email = request.cookies.get('email')
    logging.debug(f"reconvert: email={email}")
    
    if not email:
        return jsonify({"error_message": "User not authenticated."})
    
    user_data = load_user_data()
    user = user_data['users'].get(email)
    
    if not user:
        return jsonify({"error_message": "User not found."})
    
    value_of_chips = chips_data().get("value_of_chips", {})
    user_chips = user["user_chips"]
    
    # Verifica che l'utente abbia delle fiches
    if all(quantity == 0 for quantity in user_chips.values()):
        return jsonify({"error_message": "You need to have some chips to reconvert to money."})
    
    total_money = convert_back(user_chips, value_of_chips)
    remaining_money = user["remaining_money"] + total_money  # Aggiorna remaining_money con il totale convertito

    # Resetta i chip dell'utente a zero dopo la riconversione
    for color in user_chips:
        user_chips[color] = 0

    user["total_money"] = user["total_money"]  # Mantiene il totale invariato
    user["remaining_money"] = remaining_money  # Aggiorna remaining_money con il totale convertito

    save_user_data(user_data)
    
    return jsonify({
        "error_message": "",
        "value_of_chips": chips_data()["value_of_chips"],
        "total_money": user["total_money"],
        "remaining_money": user["remaining_money"]
    })

def convert_back(chips_dict, value_of_chips):
    """This function converts chips back to money"""
    total_money = 0
    for color, number in chips_dict.items():
        chip_value = int(value_of_chips[color])
        total_money += number * chip_value
    return total_money

@app.route('/user_dashboard')
def user_dashboard():
    email = request.cookies.get('email')
    logging.debug(f"user_dashboard: email={email}")
    
    if not email:
        return redirect(url_for('login'))
    
    user_data = load_user_data()
    user_info = user_data['users'].get(email)
    
    if user_info:
        logging.debug(f"user_dashboard: user_info={user_info}")
        logging.debug(f"user_dashboard: user_chips={user_info['user_chips']}")
        logging.debug(f"user_dashboard: value_of_chips={chips_data()['value_of_chips']}")
        return render_template('user_dashboard.html', 
                               username=user_info['name'], 
                               email=email, 
                               total_money=user_info['total_money'], 
                               remaining_money=user_info['remaining_money'], 
                               user_chips=user_info['user_chips'],
                               value_of_chips=chips_data()["value_of_chips"])
    else:
        return redirect(url_for('register'))

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    return redirect(url_for('login'))

@app.route('/admin_dashboard')
def admin_dashboard():
    if request.cookies.get('is_admin') != 'True':
        return redirect(url_for('admin_login'))
    
    user_data = load_user_data()
    users = user_data['users']
    
    return render_template('admin_dashboard.html', users=users)

@app.route('/earnings')
def earnings():
    user_data = load_user_data()
    earnings = {}
    for user_id, user_info in user_data['users'].items():
        if not user_info['is_admin']:  # Gli amministratori sono esclusi dal conteggio delle registrazioni
            for transaction in user_info.get('transactions', []):
                date = transaction['date']
                month = date.split('-')[1]
                if month not in earnings:
                    earnings[month] = 0
                earnings[month] += transaction['amount']
    print('Earnings data:', earnings)
    return jsonify(earnings)

@app.route('/registrations')
def registrations():
    user_data = load_user_data()
    registrations = {}
    for user_id, user_info in user_data['users'].items():
        if not user_info['is_admin']:  # Gli amministratori sono esclusi dal conteggio delle registrazioni
            registration_date = user_info.get('registration_date')
            if registration_date:
                month = registration_date.split('-')[1]
                if month not in registrations:
                    registrations[month] = 0
                registrations[month] += 1
    print('Registrations data:', registrations)
    return jsonify(registrations)

@app.route('/account')
def account():
    email = request.cookies.get('email')
    if not email:
        return redirect(url_for('login'))

    user_data = load_user_data()
    user = user_data['users'].get(email)
    if not user:
        return redirect(url_for('login'))

    user_chips = user.get('user_chips', {})

    # Verifica se il file plain_passwords.json esiste e non è vuoto
    json_path = os.path.join('json', 'plain_passwords.json')
    if not os.path.exists(json_path):
        with open(json_path, 'w') as file:
            json.dump({}, file)

    # Recupera la password in chiaro
    password = load_plain_password(email)

    # Imposta il metodo di pagamento su "None" se non è presente
    payment_method = user.get('payment_method', 'None')

    return render_template(
        'account.html',
        username=user['name'],
        email=user['email'],
        user_data=user,
        password=password,
        payment_method=payment_method,
        total_money=user['total_money'],
        remaining_money=user['remaining_money'],
        user_chips=user_chips
    )

@app.route('/delete_account', methods=['POST'])
def delete_account():
    email = request.form.get('email')
    logging.debug(f"delete_account: email={email}")
    
    user_data = load_user_data()
    deleted_user_data = load_deleted_user_data()
    
    if email in user_data['users']:
        user_data['users'][email]['deletion_date'] = datetime.now().strftime('%Y-%m-%d')
        
        # Sposta l'utente eliminato nel file deleted_users.json
        deleted_user_data['users'][email] = user_data['users'][email]
        del user_data['users'][email]
        
        save_user_data(user_data)
        save_deleted_user_data(deleted_user_data)
        
        # Aggiornamento del file JSON con le password in chiaro
        try:
            with open(os.path.join('json', 'plain_passwords.json'), 'r') as file:
                plain_passwords = json.load(file)
        except FileNotFoundError:
            plain_passwords = {}

        if email in plain_passwords:
            del plain_passwords[email]

        with open(os.path.join('json', 'plain_passwords.json'), 'w') as file:
            json.dump(plain_passwords, file, indent=4)
        
        response = make_response(redirect(url_for('casino_home')))
        response.delete_cookie('email')
        response.delete_cookie('is_admin')
        return response
    else:
        return jsonify({"error_message": "User not found."})

@app.route('/json/<path:filename>')
def serve_json(filename):
    return send_from_directory('json', filename)

if __name__ == '__main__':
    create_admin_if_not_exists()
    load_deleted_user_data()
    app.run(debug=True)