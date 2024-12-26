import json

def generate_earnings_json(file_path):
    earnings_data = {
        "January": 5000,
        "February": 7000,
        "March": 8000,
        "April": 6000,
        "May": 9000,
        "June": 11000,
        "July": 10000,
        "August": 12000,
        "September": 9500,
        "October": 10500,
        "November": 11500,
        "December": 13000
    }

    with open(file_path, 'w') as json_file:
        json.dump(earnings_data, json_file, indent=4)
    print(f"Earnings data has been written to {file_path}")

if __name__ == "__main__":
    generate_earnings_json('earnings.json')