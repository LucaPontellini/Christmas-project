import json
from tabulate import tabulate
from get_data_from_JSON import user_data

class PaymentMethod:
    def __init__(self, name, transaction_fee):
        self.name = name
        self.transaction_fee = transaction_fee

    def to_dict(self):
        return {
            "name": self.name,
            "transaction_fee": self.transaction_fee
        }

class PaymentManager:
    def __init__(self):
        self.payment_methods = []

    def add_payment_method(self, payment_method):
        self.payment_methods.append(payment_method)
        self.save_to_json('\\Christmas-project\\json\\payment_methods.json')

    def remove_payment_method(self, name):
        self.payment_methods = [pm for pm in self.payment_methods if pm.name != name]
        self.save_to_json('\\Christmas-project\\json\\payment_methods.json')

    def get_payment_method(self, name):
        for pm in self.payment_methods:
            if pm.name == name:
                return pm
        return None

    def load_from_json(self, file_path):
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            for pm in data:
                self.add_payment_method(PaymentMethod(pm['name'], pm['transaction_fee']))

    def save_to_json(self, file_path):
        with open(file_path, 'w') as json_file:
            data = [pm.to_dict() for pm in self.payment_methods]
            json.dump(data, json_file, indent=4)

class CasinoCashier:
    def __init__(self, payment_manager):
        self.payment_manager = payment_manager

    def exchange_money_for_chips(self, amount, payment_method_name):
        payment_method = self.payment_manager.get_payment_method(payment_method_name)
        if payment_method:
            final_amount = amount - (amount * payment_method.transaction_fee / 100)
            chips = final_amount // 1  # Assuming 1 chip is worth $1
            return chips
        else:
            return 0

    def exchange_chips_for_money(self, chips, payment_method_name):
        payment_method = self.payment_manager.get_payment_method(payment_method_name)
        if payment_method:
            amount = chips * 1  # Assuming 1 chip is worth $1
            final_amount = amount - (amount * payment_method.transaction_fee / 100)
            return final_amount
        else:
            return 0