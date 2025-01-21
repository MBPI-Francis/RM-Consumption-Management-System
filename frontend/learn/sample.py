import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import ttkbootstrap as ttkb
import psycopg2
from datetime import datetime

# Set up the database connection (use your own credentials)
def connect_db():
    try:
        return psycopg2.connect(
            host="192.168.1.13",  # your host
            dbname="test file",  # your database name (enclosed in quotes for spaces)
            user="postgres",  # your username
            password="mbpi"  # your password
        )
    except Exception as e:
        messagebox.showerror("Connection Error", f"Failed to connect to the database: {str(e)}")
        return None

# Function to validate form data
def validate_form():
    # Check for empty fields
    if not entry_ref.get() or not entry_date.get() or not entry_matcode.get() or not entry_qty.get() or not entry_area.get():
        messagebox.showwarning("Input Error", "All fields must be filled in!")
        return False

    # Validate date format
    try:
        datetime.strptime(entry_date.get(), "%Y-%m-%d")  # Assuming format is YYYY-MM-DD
    except ValueError:
        messagebox.showwarning("Date Error", "Please enter a valid date in YYYY-MM-DD format.")
        return False

    # Validate quantity is a number
    try:
        qty = int(entry_qty.get())
        if qty <= 0:
            messagebox.showwarning("Quantity Error", "Quantity must be a positive number.")
            return False
    except ValueError:
        messagebox.showwarning("Quantity Error", "Quantity must be a valid number.")
        return False

    return True

# Function to insert data into the database
def insert_data():
    if not validate_form():
        return

    try:
        conn = connect_db()
        if conn is None:  # Check if the connection was successful
            return
        cursor = conn.cursor()
        cursor.execute(""" 
            INSERT INTO tbl_rr (t_ref, t_date, t_matcode, t_qty, t_area)
            VALUES (%s, %s, %s, %s, %s)
        """, (entry_ref.get(), entry_date.get(), entry_matcode.get(), entry_qty.get(), entry_area.get()))
        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo("Success", "Data inserted successfully!")
        fetch_data()  # Refresh data after insertion
    except Exception as e:
        messagebox.showerror("Error", f"Failed to insert data: {str(e)}")

# Function to fetch data from the database and display it in the table
def fetch_data():
    try:
        conn = connect_db()
        if conn is None:  # Check if the connection was successful
            return
        cursor = conn.cursor()
        cursor.execute("SELECT t_ref, t_date, t_matcode, t_qty, t_area FROM tbl_rr")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        # Clear existing data in the table
        for row in tree.get_children():
            tree.delete(row)

        # Insert new rows into the table
        for row in rows:
            tree.insert("", "end", values=row)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch data: {str(e)}")

# Function to delete the selected data from the database
def delete_data():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select a row to delete.")
        return

    # Get the reference (t_ref) of the selected item
    t_ref = tree.item(selected_item, "values")[0]

    try:
        conn = connect_db()
        if conn is None:  # Check if the connection was successful
            return
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tbl_rr WHERE t_ref = %s", (t_ref,))
        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo("Success", "Data deleted successfully!")
        fetch_data()  # Refresh data after deletion
    except Exception as e:
        messagebox.showerror("Error", f"Failed to delete data: {str(e)}")

# Function to update the selected data in the database
def update_data():
    if not validate_form():
        return

    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select a row to update.")
        return

    # Get the reference (t_ref) of the selected item
    t_ref = tree.item(selected_item, "values")[0]

    try:
        conn = connect_db()
        if conn is None:  # Check if the connection was successful
            return
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE tbl_rr
            SET t_date = %s, t_matcode = %s, t_qty = %s, t_area = %s
            WHERE t_ref = %s
        """, (entry_date.get(), entry_matcode.get(), entry_qty.get(), entry_area.get(), t_ref))
        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo("Success", "Data updated successfully!")
        fetch_data()  # Refresh data after update
    except Exception as e:
        messagebox.showerror("Error", f"Failed to update data: {str(e)}")

# Set up the Tkinter window using ttkbootstrap
window = ttkb.Window(themename="superhero")  # Apply a theme
window.title("Database Input Form")

# Configure the grid layout to allow auto-sizing
window.grid_rowconfigure(0, weight=1)
window.grid_rowconfigure(1, weight=1)
window.grid_rowconfigure(2, weight=1)
window.grid_rowconfigure(3, weight=1)
window.grid_rowconfigure(4, weight=1)
window.grid_rowconfigure(5, weight=1)
window.grid_rowconfigure(6, weight=1)
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)
window.grid_columnconfigure(2, weight=1)

# Create labels and entry widgets using ttkbootstrap
label_ref = ttkb.Label(window, text="Reference (t_ref):")
label_ref.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
entry_ref = ttkb.Entry(window)
entry_ref.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

label_date = ttkb.Label(window, text="Date (t_date):")
label_date.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
entry_date = ttkb.Entry(window)
entry_date.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

label_matcode = ttkb.Label(window, text="Material Code (t_matcode):")
label_matcode.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
entry_matcode = ttkb.Entry(window)
entry_matcode.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

label_qty = ttkb.Label(window, text="Quantity (t_qty):")
label_qty.grid(row=3, column=0, padx=10, pady=5, sticky="ew")
entry_qty = ttkb.Entry(window)
entry_qty.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

label_area = ttkb.Label(window, text="Area (t_area):")
label_area.grid(row=4, column=0, padx=10, pady=5, sticky="ew")
entry_area = ttkb.Entry(window)
entry_area.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

# Buttons using ttkbootstrap
btn_insert = ttkb.Button(window, text="Insert Data", style="primary.TButton", command=insert_data)
btn_insert.grid(row=5, column=0, padx=10, pady=10, sticky="ew")

btn_update = ttkb.Button(window, text="Update Data", style="info.TButton", command=update_data)
btn_update.grid(row=5, column=1, padx=10, pady=10, sticky="ew")

btn_delete = ttkb.Button(window, text="Delete Data", style="danger.TButton", command=delete_data)
btn_delete.grid(row=5, column=2, padx=10, pady=10, sticky="ew")

# Treeview for displaying data using ttkbootstrap
tree = ttkb.Treeview(window, columns=("t_ref", "t_date", "t_matcode", "t_qty", "t_area"), show="headings")
tree.grid(row=6, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

# Define headings
tree.heading("t_ref", text="Reference (t_ref)")
tree.heading("t_date", text="Date (t_date)")
tree.heading("t_matcode", text="Material Code (t_matcode)")
tree.heading("t_qty", text="Quantity (t_qty)")
tree.heading("t_area", text="Area (t_area)")

# Set column widths
tree.column("t_ref", width=100, stretch=tk.YES)
tree.column("t_date", width=100, stretch=tk.YES)
tree.column("t_matcode", width=150, stretch=tk.YES)
tree.column("t_qty", width=100, stretch=tk.YES)
tree.column("t_area", width=150, stretch=tk.YES)

# Scrollbar for Treeview
scrollbar = ttkb.Scrollbar(window, orient="vertical", command=tree.yview)
scrollbar.grid(row=6, column=3, sticky="ns", padx=10)

tree.configure(yscrollcommand=scrollbar.set)

# Fetch data when the application starts
fetch_data()

# Run the application
window.mainloop()