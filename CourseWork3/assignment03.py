import tkinter as tk  # Import the tkinter module as tk for way to easy reference.
from tkinter import ttk  # Import ttk submodule from tkinter for themed widgets.
from datetime import datetime  # Import the datetime class from the datetime module.
import json  # Import the json module for file handling.

class FinanceTrackerGUI:
    def __init__(self, root):
        self.root = root  # Assign the Tkinter root window to an instance variable.
        self.root.title("Personal Finance Tracker")  # create the window title
        self.create_widgets()  # Call the method to create GUI widgets.
        self.root.geometry("600x700")  # set window size
        self.transactions = self.load_transactions("transactions.json")  # load file for transaction
        self.expense_labels = {}  # Initialize expense labels dictionary
        # Inside the __init__ method, create a label for the "not found" message
        self.not_found_label = tk.Label(self.root, text="", font=("Adobe Caslon Pro Bold", 12), fg="red")
        self.not_found_label.pack()

    def create_widgets(self):
        # Create and configure GUI widgets
        # Define a custom style for the buttons
        self.style = ttk.Style()
        self.style.configure('Custom.TButton', font=('Adobe Caslon Pro Bold', 10), fg='black', bg='#808080')

        # Label for title
        self.label = tk.Label(self.root, text="Personal Financial Tracker ($)", font=("Adobe Caslon Pro Bold", 10),pady=30, padx=30)
        self.label.pack()

        # Label for description
        self.label = tk.Label(self.root,text="Click the + button next to each category to view the amount and date.",font=("Adobe Garamond Pro", 13))
        self.label.pack()

        # Frame for table and scrollbar
        self.table_frame = tk.Frame(self.root, bd=10, bg="dark gray")
        self.table_frame.pack(fill=tk.BOTH, expand=1)

        # Canvas widget to hold the inner frame
        self.canvas = tk.Canvas(self.table_frame)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        # Inner frame to hold the Treeview widget
        self.inner_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor=tk.NW)

        # Treeview for displaying transactions
        self.tree = ttk.Treeview(self.inner_frame, columns=("Date", "Amount"))
        self.tree.column("#0", width=120, anchor=tk.W)
        self.tree.column("Date", width=230, anchor=tk.CENTER)
        self.tree.column("Amount", width=230, anchor=tk.CENTER)
        self.tree.heading("#0", text="Category", anchor=tk.W, command=lambda: self.sort_by_column("#0", False))
        self.tree.heading("Date", text="Date", anchor=tk.CENTER, command=lambda: self.sort_by_column("Date", False))
        self.tree.heading("Amount", text="Amount", anchor=tk.CENTER,command=lambda: self.sort_by_column("Amount", False))
        self.tree.pack(fill=tk.BOTH, expand=1)

        # Scrollbar for the Treeview
        tree_scroll = ttk.Scrollbar(self.table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=tree_scroll.set)

        # Search bar and button
        self.label_search = tk.Label(self.root, text="Search here...\nDate ex(YYYY|MM|DD)",
                                      font=("Adobe Caslon Pro Bold", 10), fg="#808080")
        self.label_search.pack(pady=10)

        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(self.root, textvariable=self.search_var, width=15, borderwidth=3)
        self.search_entry.pack(fill=tk.X, padx=10, pady=5)

        self.search_button = ttk.Button(self.root, text="Search", style="Custom.TButton",
                                         command=self.search_transactions)
        self.search_button.pack()

        # button for summary of expense
        self.expense_button = ttk.Button(self.root, text="Show Summary", style="Custom.TButton",
                                          command=self.show_summary_expense)
        self.expense_button.pack()

        # button for exit the window
        self.exit_button = ttk.Button(self.root, text="Exit", style="Custom.TButton", command=self.root.destroy)
        self.exit_button.pack()

        # Configure canvas scrolling
        self.inner_frame.bind("<Configure>", self.frame_configure)

    def frame_configure(self, event):
        # Reset the scroll region to encompass the inner frame
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def load_transactions(self, filename):
        try:
            with open(filename, "r") as file:  # Open the JSON file for reading.
                transactions = json.load(file)  # Load JSON data into a Python dictionary
            return transactions  # Return the loaded transactions.
        except FileNotFoundError:
            return {}  # Return an empty dictionary if the file is not found.

    def show_summary_expense(self):
        # Clear existing labels
        for label in self.expense_labels.values():
            label.destroy()
        self.expense_labels = {}

        # Calculate and display expenses for each category
        for category, items in self.transactions.items():
            category_total = sum(item["amount"] for item in items)
            label_text = f"{category}: LKR {category_total:.2f}"
            label = tk.Label(self.root, text=label_text, font=("Adobe Caslon Pro Bold", 12), fg="black")
            label.pack()
            self.expense_labels[category] = label

    def display_transactions(self, transactions):
        # Clear existing entries
        self.tree.delete(*self.tree.get_children())

        # Add transactions to the treeview
        for category, items in transactions.items():
            sorted_items = sorted(items, key=lambda x: datetime.strptime(x['date'], '%Y|%m|%d'))
            category_node = self.tree.insert("", "end", text=category)
            for item in sorted_items:
                # Convert date format to YYYY|MM|DD
                formatted_date = datetime.strptime(item['date'], '%Y|%m|%d').strftime('%Y|%m|%d')
                child_node = self.tree.insert(category_node, "end")
                self.tree.set(child_node, "Date", formatted_date)
                self.tree.set(child_node, "Amount", item["amount"])

    def search_transactions(self):
        # Search for transactions based on user input
        search_term = self.search_var.get().strip().lower()
        if search_term:
            results = {}
            for category, items in self.transactions.items():
                matched_items = [item for item in items if
                             search_term in item.get("date", "").lower() or
                             search_term in str(item.get("amount", "")).lower()]
                if matched_items:
                    results[category] = matched_items

            # Check if the search term matches the parent category names
            matched_categories = [category for category in self.transactions.keys() if search_term in category.lower()]
            for category in matched_categories:
                if category not in results:
                    results[category] = self.transactions[category]

            # Check if the search term matches the child categories' dates
            child_category_matches = {}
            for category, items in self.transactions.items():
                child_matched_items = [item for item in items if search_term in item.get("date", "").lower()]
                if child_matched_items:
                    child_category_matches[category] = child_matched_items
            results.update(child_category_matches)

            if not results:
                self.not_found_label.config(text="No matching transactions found!")
            else:
                self.not_found_label.config(text="")
            self.display_transactions(results)
        else:
            self.not_found_label.config(text="")
            self.display_transactions(self.transactions)
            
    def sort_by_column(self, column, reverse):
        # Define a key function based on the column
        if column == "Date":
            key_func = lambda x: (datetime.strptime(x[0], '%Y|%m|%d') if x[0] else datetime.min)
        else:
            key_func = lambda x: (float(x[0]) if x[0] else float('inf'))

        # Get all the items in the current column
        categories = self.tree.get_children('')

        for category in categories:
            children = self.tree.get_children(category)
            sorted_children = [(self.tree.set(child, column), child) for child in children]
            # Sort the items based on the key function and reverse flag
            sorted_children.sort(key=lambda x: key_func(x), reverse=reverse)

            new_index = 0
            for value, new_child in sorted_children:
                # Rearrange the items in the Treeview based on the sorted order
                self.tree.move(new_child, category, new_index)
                new_index += 1

                # Sort child nodes within each category
                if column == "Date":
                    grandchildren = self.tree.get_children(new_child)
                    sorted_grandchildren = [(self.tree.set(grandchild, column), grandchild) for grandchild in grandchildren]
                    # Sort the child nodes based on the key function and reverse flag
                    sorted_grandchildren.sort(key=lambda x: key_func(x), reverse=reverse)

                    new_grand_index = 0
                    for v, new_grand_child in sorted_grandchildren:
                        # Rearrange the child nodes in the Treeview based on the sorted order
                        self.tree.move(new_grand_child, new_child, new_grand_index)
                        new_grand_index += 1

        # Reverse the sort order for the next time the column is clicked
        self.tree.heading(column, command=lambda: self.sort_by_column(column, not reverse))

        
def main():
    root = tk.Tk()  # Create the Tkinter root window
    app = FinanceTrackerGUI(root)  # Create an instance of the FinanceTrackerGUI class.
    app.display_transactions(app.transactions)  # Display transactions in the GUI.
    root.mainloop()  # Start the Tkinter event loop.

if __name__ == "__main__":
    main()