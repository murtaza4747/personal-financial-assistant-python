# Enhanced Financial Assistant Project Implementation

# Import necessary libraries
import csv
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox, Toplevel
import re
import os
import tkinter.ttk as ttk

# Function to add transaction data and save it to a CSV file
def add_transaction(description, category, amount, date):
    """
    Add a transaction by getting details from the user.
    Saves transaction data to a CSV file.
    """
    try:
        with open('transaction_data.csv', mode='a', newline='') as file:
            fieldnames = ['description', 'category', 'amount', 'date']
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            # Write header only if file is empty
            file.seek(0, 2)  # Move to the end of the file to avoid read error
            if file.tell() == 0:  # Check if file is empty
                writer.writeheader()

            writer.writerow({'description': description, 'category': category, 'amount': amount, 'date': date})
        print("Transaction added successfully!\n")
    except Exception as e:
        print(f"An error occurred while adding transaction: {e}")

# Load financial data from CSV file
def connect_to_financial_data():
    """
    Connect to the user's financial data.
    This function loads data from a CSV file.
    Returns:
        list: A list of transaction records (e.g., a list of dictionaries).
    """
    try:
        with open('transaction_data.csv', 'r') as file:
            reader = csv.DictReader(file)
            transactions = [row for row in reader]
            return transactions
    except FileNotFoundError:
        print("Financial data file not found. Please provide a valid data source.")
        return []

# Function to visualize spending data
def visualize_spending(transactions):
    """
    Visualize spending data using a bar chart.
    Args:
        transactions (list): List of financial transactions.
    """
    categories = {}
    for t in transactions:
        try:
            # Clean and normalize category names (case-insensitive)
            category = t['category'].strip().lower()
            amount = float(re.sub(r'[^0-9.]', '', t['amount']))  # Clean and convert amount to float
            categories[category] = categories.get(category, 0) + amount
        except ValueError:
            print(f"Skipping invalid amount value: {t['amount']}")

    # Log the aggregated categories for debugging purposes
    for category, total in categories.items():
        print(f"Category: {category}, Total Spending: {total}")

    # Plot the spending data
    plt.figure(figsize=(10, 5))
    plt.bar(categories.keys(), categories.values(), color='#32e0c4')
    plt.xlabel('Category', fontsize=12, color='black', fontweight='bold')
    plt.ylabel('Total Spending', fontsize=12, color='black', fontweight='bold')
    plt.title('Spending by Category', fontsize=16, color='black', fontweight='bold')
    plt.xticks(rotation=45, color='black', fontweight='bold')
    plt.yticks(color='black', fontweight='bold')
    plt.tight_layout()
    plt.gca().set_facecolor('#2e2e2e')
    plt.show()

# Function to show spending data in a table
def show_spending_table(transactions):
    """
    Show spending data in a tabular format.
    Args:
        transactions (list): List of financial transactions.
    """
    window = Toplevel()
    window.title("Spending Table")
    window.geometry("700x500")
    window.configure(bg='#2e2e2e')
    
    columns = ('Description', 'Category', 'Amount', 'Date')
    tree = ttk.Treeview(window, columns=columns, show='headings')
    
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150, anchor='center')
    
    for t in transactions:
        tree.insert('', tk.END, values=(t['description'], t['category'], t['amount'], t['date']))
    
    tree.pack(expand=True, fill='both', padx=10, pady=10)

    # Style the table
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('Treeview', background='#3c3c3c', foreground='#f1f1f1', rowheight=25, fieldbackground='#3c3c3c')
    style.map('Treeview', background=[('selected', '#32e0c4')])

    tk.Label(window, text="Developed by Murtaza Gohari", font=("Helvetica", 10, 'italic'), bg='#2e2e2e', fg='#aaaaaa').pack(side='bottom', pady=10)

# GUI to add transaction
def add_transaction_gui(root):
    """
    Open a Toplevel window to add a transaction.
    """
    def submit():
        description = desc_entry.get()
        category = cat_entry.get()
        amount = amount_entry.get()
        date = date_entry.get()

        # Validate amount to ensure it's numeric
        if not re.match(r'^[0-9]*\.?[0-9]+$', amount):
            messagebox.showwarning("Input Error", "Please enter a valid numeric value for the amount.")
            return

        if description and category and amount and date:
            add_transaction(description, category, amount, date)
            messagebox.showinfo("Success", "Transaction added successfully!")
            window.destroy()
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields.")

    window = Toplevel(root)
    window.title("Add Transaction")
    window.geometry("500x400")
    window.configure(bg='#2e2e2e')

    # Force window to grab focus
    window.grab_set()

    tk.Label(window, text="Description", bg='#2e2e2e', fg='black', font=("Helvetica", 14, 'bold')).grid(row=0, column=0, padx=10, pady=10, sticky='w')
    desc_entry = tk.Entry(window, width=35)
    desc_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(window, text="Category", bg='#2e2e2e', fg='#ffffff', font=("Helvetica", 14)).grid(row=1, column=0, padx=10, pady=10, sticky='w')
    cat_entry = ttk.Combobox(window, values=["Groceries", "Utilities", "Rent", "Entertainment", "Other"], width=33)
    cat_entry.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(window, text="Amount", bg='#2e2e2e', fg='#ffffff', font=("Helvetica", 14)).grid(row=2, column=0, padx=10, pady=10, sticky='w')
    amount_entry = tk.Entry(window, width=35)
    amount_entry.grid(row=2, column=1, padx=10, pady=10)

    tk.Label(window, text="Date (YYYY-MM-DD)", bg='#2e2e2e', fg='#ffffff', font=("Helvetica", 14)).grid(row=3, column=0, padx=10, pady=10, sticky='w')
    date_entry = tk.Entry(window, width=35)
    date_entry.grid(row=3, column=1, padx=10, pady=10)

    submit_button = tk.Button(window, text="Submit", command=submit, width=18, height=2, bg='#0d7377', fg='black', font=("Helvetica", 12, 'bold'))
    submit_button.grid(row=4, column=1, pady=20, sticky='e')

    tk.Label(window, text="Developed by Murtaza Gohari", font=("Helvetica", 10, 'italic'), bg='#2e2e2e', fg='#aaaaaa').grid(row=5, column=1, pady=10, sticky='e')

    # Force update to ensure the window and widgets are displayed properly
    window.update_idletasks()

# Function to reset all transactions
def reset_transactions():
    """
    Delete all transaction data by removing the CSV file.
    """
    if os.path.exists('transaction_data.csv'):
        os.remove('transaction_data.csv')
        print("All transactions have been reset.")
        messagebox.showinfo("Reset Successful", "All transactions have been reset.")
    else:
        messagebox.showinfo("No Data", "No transaction data found to reset.")

# Main function to kickstart the assistant
def main():
    transactions = connect_to_financial_data()

    def handle_add_transaction():
        add_transaction_gui(root)
        nonlocal transactions
        transactions = connect_to_financial_data()  # Reload transactions after adding new data

    def handle_view_spending():
        if transactions:
            visualize_spending(transactions)
        else:
            messagebox.showinfo("No Data", "No transactions available to view.")

    def handle_view_spending_table():
        if transactions:
            show_spending_table(transactions)
        else:
            messagebox.showinfo("No Data", "No transactions available to view.")

    def handle_reset_transactions():
        reset_transactions()
        nonlocal transactions
        transactions = connect_to_financial_data()  # Reload transactions after resetting data

    root = tk.Tk()
    root.title("Financial Assistant")
    root.geometry("500x600")
    root.configure(bg='#2e2e2e')

    tk.Label(root, text="Welcome to the Financial Assistant!", font=("Helvetica", 20), bg='#2e2e2e', fg='#32e0c4').pack(pady=20)

    add_button = tk.Button(root, text="Add Transaction", command=handle_add_transaction, width=30, height=2, bg='#0d7377', fg='black', font=("Helvetica", 14, 'bold'))
    add_button.pack(pady=10)

    view_button = tk.Button(root, text="View Spending Chart", command=handle_view_spending, width=30, height=2, bg='#0d7377', fg='black', font=("Helvetica", 14, 'bold'))
    view_button.pack(pady=10)

    view_table_button = tk.Button(root, text="View Spending Table", command=handle_view_spending_table, width=30, height=2, bg='#0d7377', fg='black', font=("Helvetica", 14, 'bold'))
    view_table_button.pack(pady=10)

    reset_button = tk.Button(root, text="Reset Transactions", command=handle_reset_transactions, width=30, height=2, bg='#d32f2f', fg='black', font=("Helvetica", 14, 'bold'))
    reset_button.pack(pady=10)

    exit_button = tk.Button(root, text="Exit", command=root.quit, width=30, height=2, bg='#455a64', fg='black', font=("Helvetica", 14, 'bold'))
    exit_button.pack(pady=10)

    tk.Label(root, text="Developed by Murtaza Gohari", font=("Helvetica", 10, 'italic'), bg='#2e2e2e', fg='#aaaaaa').pack(side='bottom', pady=10)

    root.mainloop()

# Run the program if the script is executed
if __name__ == "__main__":
    main()
