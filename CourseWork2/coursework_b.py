import json
import tkinter as tk
from datetime import datetime

transactions = {}

# Function to validate the date format and ensure it's not empty
def validate_date(date_str, date_format="%Y|%m|%d"):
    if not date_str.strip():  # Check for empty or whitespace-only string
        return False
    try:
        datetime.strptime(date_str, date_format)
        return True
    except ValueError:
        return False

# Function to load transactions from a JSON file
def load_transactions():
    try:
        with open("transactions.json", "r") as file:
            data = json.load(file)
            transactions.update(data)
    except FileNotFoundError:
        print("File not found!")
    except json.JSONDecodeError:
        print("Error: Could not decode the JSON file.")
    except Exception as e:
        print(f"Unexpected error while loading transactions: {e}")

# Function to save transactions to a JSON file
def save_transactions():
    try:
        with open("transactions.json", "w") as file:
            json.dump(transactions, file)
    except FileNotFoundError:
        print("File not found!")
    except IOError:
        print("Error: Unable to write to the file.")
    except Exception as e:
        print(f"Unexpected error while saving transactions: {e}")

# Function to add transactions from a text file
def read_bulk_transactions_from_file(filename):
    if not filename.strip():
        print("Filename cannot be empty.")
        return
    
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()

            for line in lines:
                data = line.strip().split(',')
                category, amount_str, date = data[0], data[1], data[2]

                if not category.strip() or not amount_str.strip() or not date.strip():
                    print(f"Invalid data in line: {line}")
                    continue

                try:
                    amount = float(amount_str)
                except ValueError:
                    print(f"Invalid amount in line: {line}")
                    continue

                if not validate_date(date):
                    print(f"Invalid date format in line: {line}")
                    continue

                if category in transactions:
                    transactions[category].append({"amount": amount, "date": date})
                else:
                    transactions[category] = [{"amount": amount, "date": date}]
            print("Transactions data saved successfully.")
    except FileNotFoundError:
        print(f"Error: {filename} not found!")
    except Exception as e:
        print(f"Unexpected error while reading transactions: {e}")

# Function to add a new transaction
def add_transaction():
    try:
        category = input("Enter category: ").strip()
        if not category:
            print("Category cannot be empty.")
            return
        
        amount_str = input("Enter amount: ").strip()
        if not amount_str:
            print("Amount cannot be empty.")
            return

        try:
            amount = float(amount_str)
        except ValueError:
            print("Invalid amount. Please enter a valid number.")
            return

        date = input("Enter date (YYYY|MM|DD): ").strip()
        if not validate_date(date):
            print("Invalid date format. Please use YYYY|MM|DD.")
            return

        new_transaction = {"amount": amount, "date": date}
        if category in transactions:
            transactions[category].append(new_transaction)
        else:
            transactions[category] = [new_transaction]

        print("Transaction added successfully.")
    except Exception as e:
        print(f"Unexpected error while adding a transaction: {e}")

# Function to view all transactions
def view_transactions():
    if transactions:
        i = 1
        for category, details_list in transactions.items():
            print(f"{i}. Category: {category}")
            j = 1
            for details in details_list:
                print(f"   {j}. Amount: {details['amount']}\n      Date: {details['date']}")
                j += 1
            i += 1
    else:
        print("No transactions found.")

# Function to update a transaction
def update_transaction():
    view_transactions()
    if transactions:
        try:
            category_index = input("Enter the index of the category to update: ").strip()
            if not category_index.isdigit():
                print("Invalid index. Please enter a valid number.")
                return
            category_index = int(category_index) - 1

            category = list(transactions.keys())[category_index]

            transaction_index = input("Enter the index of the transaction to update: ").strip()
            if not transaction_index.isdigit():
                print("Invalid index. Please enter a valid number.")
                return
            transaction_index = int(transaction_index) - 1

            amount_str = input("Enter amount: ").strip()
            if not amount_str:
                print("Amount cannot be empty.")
                return
            amount = float(amount_str)

            date = input("Enter date (YYYY|MM|DD): ").strip()
            if not validate_date(date):
                print("Invalid date format. Please use YYYY|MM|DD.")
                return

            transactions[category][transaction_index]["amount"] = amount
            transactions[category][transaction_index]["date"] = date

            print("Transaction updated successfully.")
        except (IndexError, ValueError):
            print("Invalid input. Please enter valid indices and amounts.")
        except Exception as e:
            print(f"Unexpected error while updating the transaction: {e}")
    else:
        print("No transactions found.")

# Function to delete a transaction
def delete_transaction():
    view_transactions()
    if transactions:
        try:
            category_index = input("Enter the index of the category: ").strip()
            if not category_index.isdigit():
                print("Invalid index. Please enter a valid number.")
                return
            category_index = int(category_index) - 1

            category = list(transactions.keys())[category_index]

            transaction_index = input("Enter the index of the transaction to delete: ").strip()
            if not transaction_index.isdigit():
                print("Invalid index. Please enter a valid number.")
                return
            transaction_index = int(transaction_index) - 1

            if 0 <= transaction_index < len(transactions[category]):
                deleted_transaction = transactions[category].pop(transaction_index)
                print("Transaction deleted successfully:", deleted_transaction)
            else:
                print("Invalid index. Please try again.")
        except (ValueError, IndexError):
            print("Invalid input. Please enter valid indices.")
        except Exception as e:
            print(f"Unexpected error while deleting the transaction: {e}")
    else:
        print("No transactions found.")

# Function to display a summary of all transactions
def display_summary():
    print("Summary:")
    for category, expenses in transactions.items():
        total_amount = sum(expense['amount'] for expense in expenses)
        print(f"{category}: Total amount spent - LKR{total_amount:.2f}")

# Function to launch the GUI
def view_for_GUI():
    try:
        print("Opening window...")
        root = tk.Tk()
        app = FinanceTrackerGUI(root)
        app.display_transactions(app.transactions)
        root.mainloop()
    except Exception as e:
        print(f"Unexpected error while opening the GUI: {e}")

# Main menu function to interact with the user
def main_menu():
    load_transactions()

    while True:
        print("\nPersonal Finance Tracker")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Update Transaction")
        print("4. Delete Transaction")
        print("5. Display Summary")
        print("6. Add Transactions from File")
        print("7. View GUI Window")
        print("8. Save and Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_transaction()
        elif choice == "2":
            view_transactions()
        elif choice == "3":
            update_transaction()
        elif choice == "4":
            delete_transaction()
        elif choice == "5":
            display_summary()
        elif choice == "6":
            filename = input("Enter filename to load transactions from: ").strip()
            read_bulk_transactions_from_file(filename)
            save_transactions()
        elif choice == "7":
            view_for_GUI()
        elif choice == "8":
            print("Exiting...")
            save_transactions()
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
