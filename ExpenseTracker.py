# Importing the necessary modules and libraries
import datetime
import sqlite3
from tkinter import *
import tkinter.messagebox as mb
import tkinter.ttk as ttk

# Connecting to the database and creating the table
connector = sqlite3.connect("Expense Tracker.db")
cursor = connector.cursor()
connector.execute(
    "CREATE TABLE IF NOT EXISTS ExpenseTracker (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, Date DATETIME, Payee TEXT, Description TEXT, Amount FLOAT, ModeOfPayment TEXT)"
)
connector.commit()

# Creating the GUI window
root = Tk()
root.title("Expense Tracker")
root.geometry("800x600")
root.resizable(0, 0)

# Creating the labels and entries
Label(root, text="Date", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10)
date_entry = Entry(root, font=("Arial", 12))
date_entry.grid(row=0, column=1, padx=10, pady=10)

Label(root, text="Payee", font=("Arial", 12)).grid(row=0, column=2, padx=10, pady=10)
payee_entry = Entry(root, font=("Arial", 12))
payee_entry.grid(row=0, column=3, padx=10, pady=10)

Label(root, text="Description", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10)
description_entry = Entry(root, font=("Arial", 12))
description_entry.grid(row=1, column=1, padx=10, pady=10)

Label(root, text="Amount", font=("Arial", 12)).grid(row=1, column=2, padx=10, pady=10)
amount_entry = Entry(root, font=("Arial", 12))
amount_entry.grid(row=1, column=3, padx=10, pady=10)

Label(root, text="Mode of Payment", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=10)
mode_entry = Entry(root, font=("Arial", 12))
mode_entry.grid(row=2, column=1, padx=10, pady=10)

# Creating the buttons
add_btn = Button(root, text="Add", font=("Arial", 12), command=add_expense)
add_btn.grid(row=2, column=2, padx=10, pady=10)

delete_btn = Button(root, text="Delete", font=("Arial", 12), command=delete_expense)
delete_btn.grid(row=2, column=3, padx=10, pady=10)

update_btn = Button(root, text="Update", font=("Arial", 12), command=update_expense)
update_btn.grid(row=3, column=0, padx=10, pady=10)

view_btn = Button(root, text="View All", font=("Arial", 12), command=view_expense)
view_btn.grid(row=3, column=1, padx=10, pady=10)

report_btn = Button(root, text="Report", font=("Arial", 12), command=generate_report)
report_btn.grid(row=3, column=2, padx=10, pady=10)

exit_btn = Button(root, text="Exit", font=("Arial", 12), command=root.destroy)
exit_btn.grid(row=3, column=3, padx=10, pady=10)

# Creating the treeview widget to display the data
tree = ttk.Treeview(root, columns=(1, 2, 3, 4, 5, 6), show="headings", height=15)
tree.grid(row=4, column=0, columnspan=4, padx=10, pady=10)

tree.heading(1, text="ID")
tree.heading(2, text="Date")
tree.heading(3, text="Payee")
tree.heading(4, text="Description")
tree.heading(5, text="Amount")
tree.heading(6, text="Mode of Payment")

tree.column(1, width=50)
tree.column(2, width=100)
tree.column(3, width=100)
tree.column(4, width=200)
tree.column(5, width=100)
tree.column(6, width=100)

# Defining the functions to add, delete, update, and view the expenses
def add_expense():
    # Getting the user input
    date = date_entry.get()
    payee = payee_entry.get()
    description = description_entry.get()
    amount = amount_entry.get()
    mode = mode_entry.get()

    # Validating the user input
    if date == "" or payee == "" or description == "" or amount == "" or mode == "":
        mb.showerror("Error", "Please fill in all the fields")
        return
    try:
        amount = float(amount)
    except ValueError:
        mb.showerror("Error", "Please enter a valid amount")
        return

    # Inserting the data into the table
    connector.execute(
        "INSERT INTO ExpenseTracker (Date, Payee, Description, Amount, ModeOfPayment) VALUES (?, ?, ?, ?, ?)",
        (date, payee, description, amount, mode),
    )
    connector.commit()

    # Clearing the entries
    date_entry.delete(0, END)
    payee_entry.delete(0, END)
    description_entry.delete(0, END)
    amount_entry.delete(0, END)
    mode_entry.delete(0, END)

    # Showing a success message
    mb.showinfo("Success", "Expense added successfully")

    # Updating the treeview
    view_expense()


def delete_expense():
    # Getting the selected item
    selected_item = tree.selection()[0]

    # Getting the ID of the selected item
    id = tree.item(selected_item)["values"][0]

    # Asking for confirmation
    answer = mb.askyesno("Confirm", "Are you sure you want to delete this expense?")

    # Deleting the item from the table
    if answer:
        connector.execute("DELETE FROM ExpenseTracker WHERE ID = ?", (id,))
        connector.commit()

        # Showing a success message
        mb.showinfo("Success", "Expense deleted successfully")

        # Updating the treeview
        view_expense()


def update_expense():
    # Getting the selected item
    selected_item = tree.selection()[0]

    # Getting the ID of the selected item
    id = tree.item(selected_item)["values"][0]

    # Getting the user input
    date = date_entry.get()
    payee = payee_entry.get()
    description = description_entry.get()
    amount = amount_entry.get()
    mode = mode_entry.get()

    # Validating the user input
    if date == "" or payee == "" or description == "" or amount == "" or mode == "":
        mb.showerror("Error", "Please fill in all the fields")
        return
    try:
        amount = float(amount)
    except ValueError:
        mb.showerror("Error", "Please enter a valid amount")
        return

    # Updating the data in the table
    connector.execute(
        "UPDATE ExpenseTracker SET Date = ?, Payee = ?, Description = ?, Amount = ?, ModeOfPayment = ? WHERE ID = ?",
        (date, payee, description, amount, mode, id),
    )
    connector.commit()

    # Clearing the entries
    date_entry.delete(0, END)
    payee_entry.delete(0, END)
    description_entry.delete(0, END)
    amount_entry.delete(0, END)
    mode_entry.delete(0, END)

    # Showing a success message
    mb.showinfo("Success", "Expense updated successfully")

    # Updating the treeview
    view_expense()


def view_expense():
    # Deleting the existing data from the treeview
    for row in tree.get_children():
        tree.delete(row)

    # Fetching the data from the table
    cursor.execute("SELECT * FROM ExpenseTracker")
    rows = cursor.fetchall()

    # Inserting the data into the treeview
    for row in rows:
        tree.insert("", END, values=row)


def generate_report():
    # Creating a new window for the report
    report_window = Toplevel(root)
    report_window.title("Expense Report")
    report_window.geometry("800x600")
    report_window.resizable(0, 0)

    # Creating the labels and entries for the report
    Label(report_window, text="From Date", font=("Arial", 12)).grid(
        row=0, column=0, padx=10, pady=10
    )
    from_date_entry = Entry(report_window, font=("Arial", 12))
    from_date_entry.grid(row=0, column=1, padx=10, pady=10)
