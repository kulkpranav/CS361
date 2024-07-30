import json
import requests

# Constants
API_KEY = "0JctAjeE7hy18259S8P4XmvAAALTPG51"
BASE_URL = "https://financialmodelingprep.com/api/v3"
USERS_FILE = "users.json"


# Functions for user management
def load_users():
    try:
        with open(USERS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_users(users):
    with open(USERS_FILE, "w") as file:
        json.dump(users, file)


def sign_up(users):
    print("Sign Up")
    username = input("Enter your username: ")
    if username in users:
        print("Username already exists. Try logging in.")
        return users

    password = input("Enter your password: ")
    confirm_password = input("Confirm your password: ")

    if password != confirm_password:
        print("Passwords do not match. Try again.")
        return users

    users[username] = password
    save_users(users)
    print("Sign up successful! Please log in.")
    return users


def log_in(users):
    print("Log In")
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    if username in users and users[username] == password:
        print("Login successful!")
        return username
    else:
        print("Invalid username or password.")
        return None


# Functions for stock prices
def fetch_stock_price(symbol):
    url = f"{BASE_URL}/quote/{symbol}?apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()


    if data:
        return data[0]["price"]
    else:
        # Print error message if API response does not contain expected data
        print(f"Error fetching data for {symbol}")
        return None


def fetch_company_info(symbol):
    url = f"{BASE_URL}/profile/{symbol}?apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    return data[0] if data else {}


def view_stock_prices():
    print("View Stock Prices")
    symbols = ["AAPL", "GOOGL", "AMZN"]
    for symbol in symbols:
        price = fetch_stock_price(symbol)
        if price:
            print(f"{symbol}: ${price}")
        else:
            print(f"Could not fetch price for {symbol}")

    learn_more = input("Would you like to learn more about any company? (yes/no): ").strip().lower()
    if learn_more == 'yes':
        symbol = input("Enter the stock symbol: ").strip().upper()
        company_info = fetch_company_info(symbol)
        if company_info:
            print(f"\nCompany Overview for {symbol}:")
            print(f"Name: {company_info.get('companyName', 'N/A')}")
            print(f"Description: {company_info.get('description', 'N/A')}")
            print(f"CEO: {company_info.get('ceo', 'N/A')}")
            print(f"Sector: {company_info.get('sector', 'N/A')}")
            print(f"Industry: {company_info.get('industry', 'N/A')}")
            print(f"Website: {company_info.get('website', 'N/A')}")
        else:
            print("Could not fetch company information.")


# Main CLI
def main():
    users = load_users()
    current_user = None

    while True:
        if current_user:
            print("\nMain Menu")
            print("1. View Stock Prices")
            print("2. Logout")
            choice = input("Enter the number of your choice: ")

            if choice == "1":
                view_stock_prices()
            elif choice == "2":
                current_user = None
            else:
                print("Invalid choice. Please try again.")

        else:
            print("\nWelcome to the Stock Trading CLI Application!")
            print("1. Sign Up (Only takes a few seconds!)")
            print("2. Login")
            print("3. Continue as Guest")
            choice = input("Enter your choice (1, 2, or 3): ")

            if choice == "1":
                users = sign_up(users)
            elif choice == "2":
                current_user = log_in(users)
            elif choice == "3":
                print("Continuing as Guest...")
                view_stock_prices()
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
