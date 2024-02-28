import tkinter as tk
from tkinter import ttk
import csv
from datetime import datetime

class MoneyTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Money Tracker")
        self.total_balance = 0

        # Header
        self.header_label = ttk.Label(root, text="Money Tracker", font=('Helvetica', 18, 'bold'))
        self.header_label.grid(row=0, column=0, columnspan=3, pady=10)

        # Expense Input Fields
        self.amount_label = ttk.Label(root, text="Amount:")
        self.amount_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.amount_entry = ttk.Entry(root)
        self.amount_entry.grid(row=1, column=1, padx=5, pady=5)

        self.description_label = ttk.Label(root, text="Description:")
        self.description_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.description_entry = ttk.Entry(root)
        self.description_entry.grid(row=2, column=1, padx=5, pady=5)

        # Buttons
        self.add_expense_button = ttk.Button(root, text="Add Expense", command=self.add_expense)
        self.add_expense_button.grid(row=3, column=0, padx=5, pady=5)

        self.add_income_button = ttk.Button(root, text="Add Income", command=self.add_income)
        self.add_income_button.grid(row=3, column=1, padx=5, pady=5)

        # Total Balance Label
        self.balance_label = ttk.Label(root, text="Total Balance: 0.00")
        self.balance_label.grid(row=3, column=2, padx=5, pady=5)

        # Table
        self.tree = ttk.Treeview(root, columns=('Date', 'Description', 'Amount'), show='headings')
        self.tree.heading('Date', text='Date')
        self.tree.heading('Description', text='Description')
        self.tree.heading('Amount', text='Amount')
        self.tree.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

        # Scrollbars
        y_scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.tree.yview)
        y_scrollbar.grid(row=4, column=3, sticky='ns')
        self.tree.configure(yscrollcommand=y_scrollbar.set)

        x_scrollbar = ttk.Scrollbar(root, orient="horizontal", command=self.tree.xview)
        x_scrollbar.grid(row=5, column=0, columnspan=3, sticky='ew')
        self.tree.configure(xscrollcommand=x_scrollbar.set)

        # Load data from file (if exists)
        self.load_data()

    def add_expense(self):
        self.add_transaction("Expense")

    def add_income(self):
        self.add_transaction("Income")

    def add_transaction(self, transaction_type):
        # Get input data
        amount = float(self.amount_entry.get())
        description = self.description_entry.get()

        # Adding date
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Add to the table
        self.tree.insert('', 'end', values=(date, description, amount))

        # Save data to file
        with open('money_tracker.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([date, description, amount])
            if transaction_type == "Expense":
                self.total_balance -= amount  # Subtract the amount from the total balance for expenses
            else:
                self.total_balance += amount  # Add the amount to the total balance for incomes
            writer.writerow(["Total Balance", self.total_balance])

        self.update_balance()

    def load_data(self):
        try:
            with open('money_tracker.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row:
                        if row[0] == "Total Balance":
                            self.total_balance = float(row[1])
                            self.update_balance()
                        else:
                            self.tree.insert('', 'end', values=(row[0], row[1], row[2]))
        except FileNotFoundError:
            # If file not found, do nothing
            pass

    def update_balance(self):
        self.balance_label.config(text="Total Balance: {:.2f}".format(self.total_balance))

def main():
    root = tk.Tk()
    app = MoneyTrackerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
