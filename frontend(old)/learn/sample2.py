import requests
import ttkbootstrap as tb
from ttkbootstrap.tableview import Tableview
from tkinter import StringVar, ttk, messagebox
from datetime import datetime

# API Base URL (Replace with your actual API endpoint)
API_BASE_URL = "http://127.0.0.1:8000/api/notes/temp/list/"

# Initialize main application window
root = tb.Window(themename="superhero")
root.title("Notes Management")
root.geometry("700x500")

# Variables for form fields
product_code_var = StringVar()
lot_number_var = StringVar()
product_kind_var = StringVar()
stock_change_date_var = StringVar()

# Track selected row ID
selected_row_id = None

# Function to fetch and display data in TableView
def fetch_data():
    response = requests.get(API_BASE_URL)
    if response.status_code == 200:
        data = response.json()
        table.delete_rows()  # Corrected line
        for note in data:
            table.insert_row(values=(
                note['id'],
                note['product_code'],
                note['lot_number'],
                note['product_kind_id'],
                note['stock_change_date']
            ))

# Function to create a new note
def create_note():
    API_CREATE_URL = "http://127.0.0.1:8000/api/notes/temp/create/"
    payload = {
        "product_code": product_code_var.get(),
        "lot_number": lot_number_var.get(),
        "product_kind_id": product_kind_var.get(),
        "stock_change_date": stock_change_date_var.get()
    }
    response = requests.post(API_CREATE_URL, json=payload)
    if response.status_code == 201:
        fetch_data()

# Function to delete a note
def delete_note():
    API_DELETE_URL = "http://127.0.0.1:8000/api/notes/temp/delete"

    if selected_row_id is None:
        messagebox.showwarning("Warning", "No item selected.")
        return

    response = requests.delete(f"{API_DELETE_URL}/{selected_row_id}")
    if response.status_code == 204:  # 204 means successful deletion
        messagebox.showinfo("Success", "Record deleted successfully!")
        fetch_data()  # Refresh table after deletion
        hide_buttons()  # Hide buttons after deletion
    else:
        messagebox.showerror("Error", "Failed to delete record.")

# Function to update a note
def update_note():
    API_UPDATE_URL = "http://127.0.0.1:8000/api/notes/temp/update"
    if selected_row_id is not None:
        payload = {
            "product_code": product_code_var.get(),
            "lot_number": lot_number_var.get(),
            "product_kind_id": product_kind_var.get(),
            "stock_change_date": stock_change_date_var.get()
        }
        response = requests.put(f"{API_UPDATE_URL}/{selected_row_id}", json=payload)
        if response.status_code == 200:
            fetch_data()
            hide_buttons()  # Hide buttons after update
        else:
            messagebox.showerror("Error", "Failed to update record.")

# Function to handle row click event
def on_row_click(event):
    global selected_row_id
    selected_item = table.view.selection()
    if selected_item:
        selected_row_id = table.view.item(selected_item[0])["values"][0]
        show_buttons()  # Show buttons when a row is clicked
    else:
        hide_buttons()  # Hide buttons if no row is selected

# Function to show the buttons
def show_buttons():
    btn_update.grid(row=0, column=1, padx=5, pady=5)
    btn_delete.grid(row=0, column=2, padx=5, pady=5)

# Function to hide the buttons
def hide_buttons():
    btn_update.grid_forget()
    btn_delete.grid_forget()

# UI Components
frame = ttk.Frame(root)
frame.pack(pady=10)

# Product Code Entry
ttk.Label(frame, text="Product Code:").grid(row=0, column=0, padx=5, pady=5)
ttk.Entry(frame, textvariable=product_code_var).grid(row=0, column=1, padx=5, pady=5)

# Lot Number Entry
ttk.Label(frame, text="Lot Number:").grid(row=1, column=0, padx=5, pady=5)
ttk.Entry(frame, textvariable=lot_number_var).grid(row=1, column=1, padx=5, pady=5)

# Product Kind Dropdown
ttk.Label(frame, text="Product Kind:").grid(row=2, column=0, padx=5, pady=5)
kinds = ["MB", "DC"]
ttk.Combobox(frame, textvariable=product_kind_var, values=kinds).grid(row=2, column=1, padx=5, pady=5)

# Stock Change Date Entry
ttk.Label(frame, text="Stock Change Date:").grid(row=3, column=0, padx=5, pady=5)
ttk.Entry(frame, textvariable=stock_change_date_var).grid(row=3, column=1, padx=5, pady=5)

# Buttons frame
btn_frame = ttk.Frame(root)
btn_frame.pack(pady=10)

btn_add = tb.Button(btn_frame, text="Add", command=create_note, bootstyle="success")
btn_add.grid(row=0, column=0, padx=5)

btn_update = tb.Button(btn_frame, text="Update", command=update_note, bootstyle="warning")
btn_delete = tb.Button(btn_frame, text="Delete", command=delete_note, bootstyle="danger")

# Initially hide the Update and Delete buttons
btn_update.grid_forget()
btn_delete.grid_forget()

# Refresh button
btn_refresh = tb.Button(btn_frame, text="Refresh", command=fetch_data, bootstyle="info")
btn_refresh.grid(row=0, column=3, padx=5)

# TableView to display notes
table_columns = ["ID", "Product Code", "Lot Number", "Product Kind", "Stock Change Date"]
table = Tableview(root, coldata=table_columns, searchable=True, bootstyle="primary")
table.pack(fill="both", expand=True, padx=10, pady=10)

# Bind the click event on the table rows
table.view.bind("<ButtonRelease-1>", on_row_click)

# Initially hide the buttons if no row is selected
hide_buttons()

fetch_data()
root.mainloop()
