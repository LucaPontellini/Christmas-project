```mermaid

classDiagram
    %% admin_data.py
    class AdminData {
        +__init__(admin_file_path: str)
        +load_admin_data(): dict
        +save_admin_data(): void
        +hash_password(password: str): str
        +verify_admin(email: str, password: str): bool
        +set_admin(email: str, password: str): void
        +create_admin_if_not_exists(email: str, password: str): void
    }
    FlaskApp --> AdminData

    %% cashier.py
    class PaymentMethod {
        +__init__(name: str, transaction_fee: float)
        +to_dict(): dict
    }

    class PaymentManager {
        +__init__()
        +add_payment_method(payment_method: PaymentMethod): void
        +remove_payment_method(name: str): void
        +get_payment_method(name: str): PaymentMethod
        +load_from_json(file_path: str): void
        +save_to_json(file_path: str): void
    }

    class CasinoCashier {
        +__init__(payment_manager: PaymentManager)
        +exchange_money_for_chips(amount: float, payment_method_name: str): float
        +exchange_chips_for_money(chips: float, payment_method_name: str): float
    }

    PaymentManager "1" -- "n" PaymentMethod : manages
    CasinoCashier "1" -- "1" PaymentManager : uses
    FlaskApp --> PaymentManager
    FlaskApp --> CasinoCashier

    %% deck_data.py
    class DeckData {
        +__init__(deck_file_path: str)
        +load_deck_data(): dict
        +save_deck_data(): void
        +create_default_deck_data(): dict
    }
    FlaskApp --> DeckData

    %% get_data_from_JSON.py
    class UserData {
        +__init__(user_file: str)
        +add_user(user_id: str, name: str, balance: float, email: str, password: str): void
        +data: dict
    }
    FlaskApp --> UserData

    %% password_manager.py
    class PasswordManager {
        +__init__(user_file_path: str)
        +load_user_data(): dict
        +save_user_data(): void
        +hash_password(password: str): str
        +generate_reset_token(email: str): str
        +verify_reset_token(token: str): str
        +reset_password(token: str, new_password: str): bool
    }
    FlaskApp --> PasswordManager

    %% plot_casino_revenue.py
    class CasinoUserData {
        +__init__(file_path: str)
        +load_data(): dict
        +create_empty_file(): void
        +read_data(): dict
        +add_user(user_id: str, name: str, balance: float, email: str, password: str): void
        +add_win_loss(user_id: str, game: str, result: int): void
        +update_balance(user_id: str, amount: float): void
        +save_data(): void
    }

    class Main {
        +get_user_ids(user_data: CasinoUserData): list
        +get_user_balance(user_data: CasinoUserData, user_id: str): float
        +get_user_revenues(user_data: CasinoUserData, user_ids: list): list
        +plot_casino_revenue(user_data: CasinoUserData): void
        +create_bar_chart(user_ids: list, revenues: list): void
    }

    Main --> CasinoUserData
    FlaskApp --> CasinoUserData

    %% plot_user_growth.py
    class UserRegistrationData {
        +__init__(file_path: str)
        +load_data(): dict
        +create_empty_file(): void
        +add_user(user_id: str, name: str, balance: float, email: str, password: str, registration_date: str): void
        +save_data(): void
    }

    class Main {
        +get_registration_dates(user_data: UserRegistrationData): list
        +convert_dates(registration_dates: list): list
        +calculate_cumulative_registrations(dates: list): list
        +plot_user_registrations(user_data: UserRegistrationData): void
        +plot_graph(dates: list, cumulative_registrations: list): void
    }

    Main --> UserRegistrationData
    FlaskApp --> UserRegistrationData

    %% plot_user_wins_losses.py
    class CasinoData {
        +__init__(file_path: str)
        +load_data(): dict
        +create_empty_file(): void
        +add_user(user_id: str, name: str, balance: float, email: str, password: str): void
        +add_win_loss(user_id: str, game: str, result: int): void
        +update_balance(user_id: str, result: float): void
        +save_data(): void
    }

    class Main {
        +get_user_ids(user_data: CasinoData): list
        +get_user_win_loss(user_data: CasinoData, user_id: str): int
        +get_user_wins_losses(user_data: CasinoData, user_ids: list): list
        +plot_user_wins_losses(user_data: CasinoData): void
        +create_bar_chart(user_ids: list, wins_losses: list): void
        +get_bar_colors(wins_losses: list): list
        +get_bar_color(win_loss: int): str
        +plot_bar_chart(user_ids: list, wins_losses: list, colors: list): void
    }

    Main --> CasinoData
    FlaskApp --> CasinoData

    %% user_data.py
    class UserData {
        +__init__(user_file_path: str)
        +load_data(): dict
        +create_default_data(): void
        +save_data(): void
        +hash_password(password: str): str
        +add_user(user_id: str, name: str, balance: float, email: str, password: str): void
        +authenticate_user(user_id: str, password: str): bool
        +update_password(user_id: str, new_password: str): bool
        +process_transaction(user_id: str, amount: float, transaction_type: str): void
        +update_balance(user_id: str, amount: float): void
        +delete_user(user_id: str): bool
    }
    FlaskApp --> UserData

    %% casino.py
    class FlaskApp {
        +load_user_data(): dict
        +save_user_data(data: dict): void
        +load_plain_password(email: str): str
        +save_plain_password(email: str, password: str): void
        +hash_password(password: str): str
        +create_admin_if_not_exists(): void
        +load_admin_data(): dict
        +verify_admin(email: str, password: str): bool
        +load_deleted_user_data(): dict
        +save_deleted_user_data(data: dict): void
        +welcome(): str
        +return_to_welcome(): str
        +casino_home(): str
        +return_to_casino_home(): str
        +register(): str
        +login(): str
        +logout(): str
        +forgot_password(): str
        +reset_password(token: str): str
        +poker_rules(): str
        +cashier_dashboard(): str
        +convert_to_chips(): str
        +home_poker(): str
        +play(): str
        +update_total_money(): str
        +clear_all_data(): str
        +reconvert(): str
        +user_dashboard(): str
        +admin_login(): str
        +admin_dashboard(): str
        +earnings(): str
        +registrations(): str
        +account(): str
        +delete_account(): str
        +serve_json(filename: str): str
    }
    
    FlaskApp --> UserData
    FlaskApp --> PasswordManager