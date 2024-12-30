import sys
import os
from flask import Flask, render_template, redirect, url_for, request
from flask_mail import Mail, Message
import json

# Aggiungi il percorso relativo alla directory python_files
sys.path.append(os.path.join(os.path.dirname(__file__), 'python_files'))
from user_data import UserData
from get_data_from_JSON import chips_data
from deck_data import DeckData

app = Flask(__name__)

# Configurazione di Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.example.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'your_email@example.com'
app.config['MAIL_PASSWORD'] = 'your_email_password'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

# Percorso del file JSON degli utenti
user_file_path = os.path.join(os.path.dirname(__file__), 'json', 'users.json')

# Percorso del file JSON del mazzo di carte
deck_file_path = os.path.join(os.path.dirname(__file__), 'json', 'deck_into_json.json')

user_data = UserData(user_file_path)
deck_data = DeckData(deck_file_path)

def load_user_data():
    if os.path.exists(user_file_path):
        with open(user_file_path, 'r') as f:
            return json.load(f)
    else:
        return {"users": {}}

def save_user_data(data):
    with open(user_file_path, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/return_to_welcome')
def return_to_welcome():
    return redirect(url_for('welcome'))

@app.route('/casino_home')
def casino_home():
    return render_template('casino_home.html')

@app.route('/return_to_casino_home')
def return_to_casino_home():
    return redirect(url_for('casino_home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_id = request.form['email']
        name = request.form['fname'] + ' ' + request.form['lname']
        email = request.form['email']
        password = request.form['psw']
        
        user_data = load_user_data()
        
        if 'users' not in user_data:
            user_data['users'] = {}

        if user_id in user_data['users']:
            return 'User already registered. Please use a different email or login.'

        user_data['users'][user_id] = {
            'name': name,
            'email': email,
            'password': password,
            'user_chips': {
                "white": 0,
                "red": 0,
                "blue": 0,
                "green": 0,
                "black": 0,
                "purple": 0,
                "yellow": 0,
                "pink": 0,
                "light blue": 0,
            },
            'total_money': 0,
            'remaining_money': 0
        }
        save_user_data(user_data)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['email']  # Utilizziamo l'email come user_id
        password = request.form['psw']
        user_data = load_user_data()
        if user_id in user_data['users'] and user_data['users'][user_id]['password'] == password:
            response = redirect(url_for('casino_home'))
            response.set_cookie('username', user_id)
            return response
        else:
            return 'Invalid credentials'
    return render_template('login.html')

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        user_data = load_user_data()
        
        # Verifica se l'utente esiste nel file JSON
        if email not in user_data['users']:
            return 'User not found. Please check your email or register for an account.'
        
        # Procedi con il recupero della password (ad esempio, invia un'email con un link per resettare la password)
        reset_link = url_for('reset_password', _external=True)
        email_body = f"Click the following link to reset your password: {reset_link}"
        
        msg = Message('Password Reset Request', sender='your_email@example.com', recipients=[email])
        msg.body = email_body
        try:
            mail.send(msg)
            return 'Password reset instructions have been sent to your email.'
        except Exception as e:
            return f'Failed to send email: {e}'
    return render_template('forgot_password.html')

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form['email']
        new_password = request.form['new_password']
        user_data = load_user_data()
        
        if email in user_data['users']:
            user_data['users'][email]['password'] = new_password
            save_user_data(user_data)
            return redirect(url_for('login'))
        else:
            return 'User not found'
    return render_template('reset_password.html')

@app.route('/poker_rules')
def poker_rules():
    return render_template('poker_rules.html')

@app.route('/cashier_operations', methods=['GET', 'POST'])
def cashier_dashboard():
    user_id = request.cookies.get('username')
    if user_id:
        user_data = load_user_data()
        user = user_data['users'].get(user_id)
        if user:
            total_money = user['total_money']
            remaining_money = user['remaining_money']
            if request.method == 'POST':
                total_money = request.form.get('total_money', type=int, default=total_money)
                remaining_money = request.form.get('remaining_money', type=int, default=remaining_money)
            return render_template('cashier_operations.html', value_of_chips=chips_data()["value_of_chips"], total_money=total_money, remaining_money=remaining_money)
        else:
            return redirect(url_for('register'))
    else:
        return redirect(url_for('register'))

@app.route('/convert_to_chips', methods=['POST'])
def convert_to_chips():
    user_id = request.cookies.get('username')
    if user_id:
        user_data = load_user_data()
        user = user_data['users'].get(user_id)
        if user:
            try:
                amount_str = request.form['amount']
                chip_color = request.form['chip-color']
                if not amount_str.strip():
                    raise ValueError("Please enter a valid amount.")
                amount = int(amount_str)
                chip_value = chips_data()["value_of_chips"].get(chip_color)
                if not chip_value:
                    raise ValueError("Invalid chip color selected.")
                total_cost = amount * chip_value
                if total_cost > user["remaining_money"]:
                    raise ValueError("Insufficient funds.")
            except KeyError:
                return render_template('cashier_operations.html', error_message="Please enter a valid amount and select a chip color.", value_of_chips=chips_data()["value_of_chips"], total_money=user['total_money'], remaining_money=user['remaining_money'])
            except ValueError as e:
                return render_template('cashier_operations.html', error_message=str(e), value_of_chips=chips_data()["value_of_chips"], total_money=user['total_money'], remaining_money=user['remaining_money'])

            user["remaining_money"] -= total_cost
            user["user_chips"][chip_color] += amount
            save_user_data(user_data)
            return redirect(url_for('cashier_dashboard_page'))
        else:
            return redirect(url_for('register'))
    else:
        return redirect(url_for('register'))

@app.route('/home_poker')
def home_poker():
    return render_template('home_poker.html')

@app.route('/play')
def play():
    user_id = request.cookies.get('username')
    if user_id:
        user_data = load_user_data()
        user = user_data['users'].get(user_id)
        if user:
            has_chips = any(amount > 0 for amount in user['user_chips'].values())
            if user['remaining_money'] > 0 or has_chips:
                return render_template('play.html')
            else:
                error_message = "You need to have some chips or remaining money to play."
                redirect_url = url_for('cashier_dashboard_page')
                return render_template('home_poker.html', error_message=error_message, redirect_url=redirect_url)
        else:
            error_message = "User not found. Please register to play."
            redirect_url = url_for('register')
            return render_template('home_poker.html', error_message=error_message, redirect_url=redirect_url)
    else:
        error_message = "You need to be logged in to play."
        redirect_url = url_for('register')
        return render_template('home_poker.html', error_message=error_message, redirect_url=redirect_url)

@app.route("/update_total_money", methods=["POST"])
def update_total_money():
    user_id = request.cookies.get('username')
    if user_id:
        user_data = load_user_data()
        user = user_data['users'].get(user_id)
        if user:
            payment_method = request.form.get('payment_method')
            if not payment_method:
                error_message = "Please select a payment method."
                return render_template(
                    "cashier_operations.html",
                    error_message=error_message,
                    value_of_chips=chips_data()["value_of_chips"],
                    total_money=user["total_money"],
                    remaining_money=user["remaining_money"]
                )

            new_total_money_str = request.form.get("total_money", "")
            if not new_total_money_str.strip():
                error_message = "Please enter a valid amount."
                return render_template(
                    "cashier_operations.html",
                    error_message=error_message,
                    value_of_chips=chips_data()["value_of_chips"],
                    total_money=user["total_money"],
                    remaining_money=user["remaining_money"],
                    payment_method=payment_method
                )

            try:
                new_total_money = int(new_total_money_str)
            except ValueError:
                error_message = "Error: The amount must be an integer."
                return render_template(
                    "cashier_operations.html",
                    error_message=error_message,
                    value_of_chips=chips_data()["value_of_chips"],
                    total_money=user["total_money"],
                    remaining_money=user["remaining_money"],
                    payment_method=payment_method
                )

            user["total_money"] = new_total_money
            user["remaining_money"] = new_total_money
            user["payment_method"] = payment_method

            save_user_data(user_data)
            return redirect(url_for("cashier_dashboard_page"))
        else:
            return 'User not found'
    else:
        return redirect(url_for('register'))

@app.route("/clear_all_data", methods=["POST"])
def clear_all_data():
    user_id = request.cookies.get('username')
    if user_id:
        user_data = load_user_data()
        user = user_data['users'].get(user_id)
        if user:
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
            return redirect(url_for("cashier_dashboard"))
        else:
            return 'User not found'
    else:
        return redirect(url_for('register'))

@app.route('/cashier_dashboard', methods=['GET', 'POST'])
def cashier_dashboard_page():
    user_id = request.cookies.get('username')
    if user_id:
        user_data = load_user_data()
        user = user_data['users'].get(user_id)
        if user:
            if request.method == "POST":
                new_total_money_str = request.form.get("total_money", "")
                if new_total_money_str.strip():
                    new_total_money = int(new_total_money_str)
                else:
                    new_total_money = 0

                difference = new_total_money - user["total_money"]

                user["remaining_money"] += difference
                user["total_money"] = new_total_money

                save_user_data(user_data)
                return redirect(url_for("cashier_dashboard_page"))
            else:
                value_of_chips = chips_data().get("value_of_chips", {})
                total_money = user.get("total_money", 0)
                remaining_money = user.get("remaining_money", 0)
                return render_template(
                    "cashier_operations.html",
                    value_of_chips=value_of_chips,
                    total_money=total_money,
                    remaining_money=remaining_money,
                )
        else:
            return 'User not found'
    else:
        return redirect(url_for('register'))

# Funzione per la rotta '/reconvert'
@app.route("/reconvert", methods=["POST"])
def reconvert():
    user_id = request.cookies.get('username')
    if user_id:
        user_data = load_user_data()
        user = user_data['users'].get(user_id)
        if user:
            value_of_chips = chips_data().get("value_of_chips", {})
            user_chips = user["user_chips"]
            total_money = convert_back(user_chips, value_of_chips)
            remaining_money = user["remaining_money"] + total_money  # Aggiorna remaining_money con il totale convertito

            # Resetta i chip dell'utente a zero dopo la riconversione
            for color in user_chips:
                user_chips[color] = 0

            user["total_money"] = user["total_money"]  # Mantieni il totale invariato
            user["remaining_money"] = remaining_money  # Aggiorna remaining_money con il totale convertito

            save_user_data(user_data)
            return redirect(url_for("user_dashboard"))
        else:
            return 'User not found'
    else:
        return redirect(url_for('register'))

def convert_back(chips_dict, value_of_chips):
    """This function converts chips back to money"""
    total_money = 0
    for color, number in chips_dict.items():
        chip_value = int(value_of_chips[color])
        total_money += number * chip_value
    return total_money

# Funzione per la rotta '/user_dashboard'
@app.route("/user_dashboard")
def user_dashboard():
    user_id = request.cookies.get('username')
    if user_id:
        user_data = load_user_data()
        user = user_data['users'].get(user_id)
        if user:
            user_chips = user["user_chips"]
            total_money = user["total_money"]
            remaining_money = user["remaining_money"]
            value_of_chips = chips_data()["value_of_chips"]

            return render_template(
                "user_dashboard.html",
                user_chips=user_chips,
                total_money=total_money,
                remaining_money=remaining_money,
                value_of_chips=value_of_chips,
            )
        else:
            return 'User not found'
    else:
        return redirect(url_for('register'))

if __name__ == '__main__':
    app.run(debug=True)