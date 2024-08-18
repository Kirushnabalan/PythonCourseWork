import json
from datetime import datetime

# Global list to store transactions
transactions = []

# File handling functions
# Function to load transactions
def load_transactions():
    try:
        with open("transactions.json", "r") as file:
            file_load = json.load(file)
        transactions.extend(file_load)
    except FileNotFoundError:
        print("No existing transactions found.")
    except json.JSONDecodeError:
        print("Error decoding JSON from the file.")

# Function to save transactions
def save_transactions():
    try:
        with open("transactions.json", "w") as file:
            json.dump(transactions, file)
    except IOError:
        print("Error saving transactions.")

# Feature implementations
# Function to add a transaction
def add_transaction():
    while True:
        try: 
            amount = float(input("Enter amount: "))
            if amount < 0:
                raise ValueError("Amount cannot be negative.")
            break
        except ValueError: 
            print(f"Invalid input. Please enter a valid number.")

    while True:
        category = input("Enter category: ")
        if category:
            break
        else:
            print("Invalid category. Please enter a valid category.")

    while True:
        transaction_type = input("Enter type (Income/Expense): ").title()
        if transaction_type in ["Income", "Expense"]:
            break
        else:
            print("Invalid type. Please enter 'Income' or 'Expense'.")

    while True:
        date = input("Enter date (YYYY-MM-DD): ")
        try:
            datetime.strptime(date, "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

    transaction = [amount, category, transaction_type, date]
    transactions.append(transaction)
    print("Transaction added successfully.")

# Function to view transactions
def view_transactions():
    if transactions:
        for count, transaction in enumerate(transactions, start=1):
            print(f"{count}. Amount: {transaction[0]}, Category: {transaction[1]}, Type: {transaction[2]}, Date: {transaction[3]}")
    else:
        print("No transactions found.")

# Function to update a transaction
def update_transaction():
    if transactions:
        try:
            index = int(input("Enter the index of the transaction to update: ")) - 1
            if 0 <= index < len(transactions):
                while True:
                    try: 
                        amount = float(input("Enter new amount: "))
                        break
                    except ValueError: 
                        print("Invalid input. Please enter a valid number.")

                category = input("Enter new category: ")
                transaction_type = input("Enter new type (Income/Expense): ").title()

                while True:
                    date = input("Enter new date (YYYY-MM-DD): ")
                    try:
                        datetime.strptime(date, "%Y-%m-%d")
                        break
                    except ValueError:
                        print("Invalid date format. Please use YYYY-MM-DD.")

                transactions[index] = [amount, category, transaction_type, date]
                print("Transaction updated successfully.")
            else:
                print("Invalid index. Please try again.")
        except (IndexError, ValueError):
            print("Invalid input. Please try again.")
    else:
        print("No transactions found.")

# Function to delete a transaction
def delete_transaction():
    if transactions:
        try:
            index = int(input("Enter the index of the transaction to delete: ")) - 1
            if 0 <= index < len(transactions):
                del transactions[index]
                print("Transaction deleted successfully.")
            else:
                print("Invalid index. Please try again.")
        except (IndexError, ValueError):
            print("Invalid input. Please try again.")
    else:
        print("No transactions found.")

# Function to display summary of transactions
def display_summary():
    total_income = 0
    total_expense = 0

    for transaction in transactions:
        transaction_type = transaction[2]
        amount = transaction[0]
        if transaction_type == "Income":
            total_income += amount  
        elif transaction_type == "Expense":
            total_expense += amount 

    print(f"Total Income: {total_income}")
    print(f"Total Expense: {total_expense}")
    print(f"Balance: {total_income - total_expense}")

# Function to display the main menu
def main_menu():
    load_transactions()
    while True:
        print("\nPersonal Finance Tracker")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Update Transaction")
        print("4. Delete Transaction")
        print("5. Display Summary")
        print("6. Save and Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            add_transaction()
        elif choice == '2':
            view_transactions()
        elif choice == '3':
            update_transaction()
        elif choice == '4':
            delete_transaction()
        elif choice == '5':
            display_summary()
        elif choice == '6':
            save_transactions()
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")

# Entry point of the program
if __name__ == "__main__":
    main_menu()
