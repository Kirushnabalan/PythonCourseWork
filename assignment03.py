import tkinter as tk
from tkinter import ttk
from datetime import datetime
import json

class FinanceTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Tracker")
        self.root.geometry("700x800")
        self.root.minsize(500, 600)
        
        # Define styles
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Arial', 10), padding=10)
        self.style.configure('TLabel', font=('Arial', 12))
        self.style.configure('TFrame', background='#e0f7fa')
        
        self.transactions = self.load_transactions("transactions.json")
        self.expense_labels = {}
        
        self.create_widgets()

    def create_widgets(self):
        # Title
        title_frame = ttk.Frame(self.root, padding=(10, 10))
        title_frame.grid(row=0, column=0, sticky='ew')
        
        title_label = ttk.Label(title_frame, text="Personal Financial Tracker", font=("Arial", 18, "bold"))
        title_label.pack(pady=(20, 10))

        # Description
        desc_label = ttk.Label(title_frame, text="Click the + button next to each category to view details.", font=("Arial", 12))
        desc_label.pack(pady=(0, 20))

        # Treeview Frame
        table_frame = ttk.Frame(self.root, padding=(10, 0))
        table_frame.grid(row=1, column=0, sticky='nsew')

        # Treeview for displaying transactions
        self.tree = ttk.Treeview(table_frame, columns=("Date", "Amount"), show="headings")
        self.tree.heading("Date", text="Date", command=lambda: self.sort_by_column("Date", False))
        self.tree.heading("Amount", text="Amount", command=lambda: self.sort_by_column("Amount", False))
        self.tree.column("Date", anchor=tk.CENTER)
        self.tree.column("Amount", anchor=tk.CENTER)
        self.tree.grid(row=0, column=0, sticky='nsew')

        # Scrollbar for the Treeview
        tree_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=tree_scroll.set)
        tree_scroll.grid(row=0, column=1, sticky='ns')

        # Configure resizing behavior
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        # Search bar
        search_frame = ttk.Frame(self.root, padding=(10, 10))
        search_frame.grid(row=2, column=0, sticky='ew')
        
        search_label = ttk.Label(search_frame, text="Search here (YYYY|MM|DD):", font=("Arial", 12))
        search_label.pack(side=tk.LEFT)
        
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 20))
        
        search_button = ttk.Button(search_frame, text="Search", command=self.search_transactions)
        search_button.pack(side=tk.RIGHT)

        # Summary Button
        button_frame = ttk.Frame(self.root, padding=(10, 10))
        button_frame.grid(row=3, column=0, sticky='ew')

        summary_button = ttk.Button(button_frame, text="Show Summary", command=self.show_summary_expense)
        summary_button.pack(side=tk.LEFT, padx=(0, 20))

        exit_button = ttk.Button(button_frame, text="Exit", command=self.root.destroy)
        exit_button.pack(side=tk.RIGHT)

    def load_transactions(self, filename):
        try:
            with open(filename, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def show_summary_expense(self):
        for label in self.expense_labels.values():
            label.destroy()
        self.expense_labels = {}

        for category, items in self.transactions.items():
            category_total = sum(item["amount"] for item in items)
            label_text = f"{category}: ${category_total:.2f}"
            label = ttk.Label(self.root, text=label_text, font=("Arial", 12, "bold"))
            label.grid(sticky='w', padx=20, pady=5)
            self.expense_labels[category] = label

    def display_transactions(self, transactions):
        self.tree.delete(*self.tree.get_children())
        for category, items in transactions.items():
            sorted_items = sorted(items, key=lambda x: datetime.strptime(x['date'], '%Y|%m|%d'))
            for item in sorted_items:
                self.tree.insert("", "end", values=(item["date"], item["amount"]))

    def search_transactions(self):
        search_term = self.search_var.get().strip().lower()
        if search_term:
            results = {}
            for category, items in self.transactions.items():
                matched_items = [item for item in items if search_term in item.get("date", "").lower()]
                if matched_items:
                    results[category] = matched_items
            self.display_transactions(results)
        else:
            self.display_transactions(self.transactions)
            
    def sort_by_column(self, column, reverse):
        categories = [(self.tree.set(k, column), k) for k in self.tree.get_children('')]
        categories.sort(reverse=reverse)
        for index, (val, k) in enumerate(categories):
            self.tree.move(k, '', index)
        self.tree.heading(column, command=lambda: self.sort_by_column(column, not reverse))

def main():
    root = tk.Tk()
    app = FinanceTrackerGUI(root)
    app.display_transactions(app.transactions)
    root.mainloop()

if __name__ == "__main__":
    main()
