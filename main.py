import os
import tkinter as tk
from tkinter import ttk, messagebox

def add_expense():
    """Adds an expense to the file and updates the display."""
    date = date_entry.get().strip()
    category = category_entry.get().strip()
    amount = amount_entry.get().strip()

    if not date or not category or not amount:
        status_label.config(text="Please fill all the fields!", fg="red")
        return

    try:
        amount = float(amount)    # Validate numeric input for amount
    except ValueError:
        status_label.config(text="Amount must be a valid number!", fg="red")
        return

    with open("expenses.txt", "a") as file:
        file.write(f"{date},{category},{amount:.2f}\n")

    status_label.config(text="Expense added successfully!", fg="green")
    
    # Clear input fields
    date_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    
    view_expenses()  # Refresh the list

def delete_expense():
    """Deletes the selected expense from the file and updates the display."""
    selected_item = expenses_tree.selection()
    if not selected_item:
        status_label.config(text="Please select an expense to delete!", fg="red")
        return

    item_text = expenses_tree.item(selected_item, "values")
    date, category, amount = item_text

    # Read existing data
    with open("expenses.txt", "r") as file:
        lines = file.readlines()

    # Write back all data except the selected one
    with open("expenses.txt", "w") as file:
        file.writelines(line for line in lines if line.strip() != f"{date},{category},{amount}")

    status_label.config(text="Expense deleted successfully!", fg="green")
    view_expenses()  # Refresh the list

def view_expenses():
    """Displays all expenses and calculates total expense."""
    if not os.path.exists("expenses.txt"):
        total_label.config(text="No expenses recorded.")
        expenses_tree.delete(*expenses_tree.get_children())
        return

    total_expense = 0
    expenses_tree.delete(*expenses_tree.get_children())  # Clear existing data

    with open("expenses.txt", "r") as file:
        for line in file:
            date, category, amount = line.strip().split(",")
            expenses_tree.insert("", tk.END, values=(date, category, f"₹{amount}"))
            total_expense += float(amount)

    total_label.config(text=f"Total Expense: ₹{total_expense:.2f}")

# Create the main application window
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("450x400")

# Create labels and entry fields
tk.Label(root, text="Date (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
date_entry = tk.Entry(root)
date_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Category:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
category_entry = tk.Entry(root)
category_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Amount (₹):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
amount_entry = tk.Entry(root)
amount_entry.grid(row=2, column=1, padx=5, pady=5)

# Buttons
tk.Button(root, text="Add Expense", command=add_expense, bg="lightblue").grid(row=3, column=0, columnspan=2, pady=10)

# Treeview for displaying expenses
columns = ("Date", "Category", "Amount")
expenses_tree = ttk.Treeview(root, columns=columns, show="headings")
expenses_tree.heading("Date", text="Date")
expenses_tree.heading("Category", text="Category")
expenses_tree.heading("Amount", text="Amount")
expenses_tree.column("Date", width=100)
expenses_tree.column("Category", width=120)
expenses_tree.column("Amount", width=80)
expenses_tree.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

# Labels for total expense and status messages
total_label = tk.Label(root, text="", font=("Arial", 10, "bold"))
total_label.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

status_label = tk.Label(root, text="", fg="green")
status_label.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

# Buttons for viewing and deleting expenses
tk.Button(root, text="View Expenses", command=view_expenses, bg="lightgreen").grid(row=7, column=0, padx=5, pady=10)
tk.Button(root, text="Delete Expense", command=delete_expense, bg="red", fg="white").grid(row=7, column=1, padx=5, pady=10)

# Ensure 'expenses.txt' exists
if not os.path.exists("expenses.txt"):
    with open("expenses.txt", "w"):
        pass

# Load existing expenses
view_expenses()


root.mainloop()