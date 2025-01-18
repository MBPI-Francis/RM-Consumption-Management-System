import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import requests
from backend.settings.database import server_ip
from ttkbootstrap.tooltip import ToolTip
from ttkbootstrap.dialogs.dialogs import Messagebox
from datetime import datetime as d_datetime
import datetime
from .table import table


# def entry_fields(note_form_tab):
#
#     # Function to get the selected item's ID
#     def get_selected_product_kind_id():
#         selected_name = product_kind_combobox.get()
#         selected_id = name_to_id.get(selected_name)  # Get the corresponding ID
#         if selected_id:
#             print(f"Selected: ID={selected_id}, Name={selected_name}")
#             return selected_id
#         else:
#             print("No selection made.")
#
#         # Function to send POST request
#
#     def submit_data():
#         # Collect the form data
#         product_code = product_code_entry.get()
#         lot_number = lot_number_entry.get()
#         product_kind_id = get_selected_product_kind_id()
#         print("THE ID: ", product_kind_id)
#         consumption_date = date_entry.get()
#         # Convert it from MM/DD/YYYY to YYYY-MM-DD
#         consumption_date = d_datetime.strptime(consumption_date, "%m/%d/%Y").strftime("%Y-%m-%d")
#
#         # Create a dictionary with the data
#         data = {
#             "product_code": product_code,
#             "lot_number": lot_number,
#             "product_kind_id": product_kind_id,
#             "stock_change_date": consumption_date
#         }
#         # Send a POST request to the API
#         try:
#             response = requests.post(f"{server_ip}/api/notes/temp/create/", json=data)  # Adjust the URL
#             if response.status_code == 200:  # Successfully created
#
#                 Messagebox.show_info("Success", "Data added successfully!")  # Success message
#                 entry_fields(note_form_tab) # Call the table
#
#             else:
#                 Messagebox.show_error("Error", f"Failed to add data. {response.status_code}")  # Error message
#
#         except requests.exceptions.RequestException as e:
#             Messagebox.show_error("Error", f"An error occurred: {e}")  # Error message
#
#     # Create a frame for the form inputs
#     form_frame = ttk.Frame(note_form_tab)
#     form_frame.pack(fill=X, pady=10, padx=20)
#
#     # Product Code Entry
#     product_code_label = ttk.Label(form_frame, text="Product Code:", font=("Helvetica", 10,"bold"))
#     product_code_label.grid(row=0, column=0, padx=5, pady=5, sticky=W)
#     product_code_entry = ttk.Entry(form_frame, width=40)
#     product_code_entry.grid(row=1, column=0, padx=5, pady=5)
#
#     # default tooltip
#     ToolTip(product_code_entry, text="Enter the product code")
#
#
#
#     # Lot Number Entry
#     lot_number_label = ttk.Label(form_frame, text="Lot Number:", font=("Helvetica", 10,"bold"))
#     lot_number_label.grid(row=0, column=1, padx=5, pady=5, sticky=W)
#     lot_number_entry = ttk.Entry(form_frame, width=40)
#     lot_number_entry.grid(row=1, column=1, padx=5, pady=5)
#     # tooltip
#     ToolTip(lot_number_entry, text="Enter the lot number")
#
#     # JSON-format choices
#     product_kinds = get_product_kinds_api()
#
#     # Map names to IDs for easy lookup
#     name_to_id = {item["name"]: item["id"] for item in product_kinds}
#
#     # Extract names for the combobox
#     product_kind_names = list(name_to_id.keys())
#
#     # Add a combobox
#     lot_number_label = ttk.Label(form_frame, text="Product Kind:", font=("Helvetica", 10,"bold"))
#     lot_number_label.grid(row=0, column=3, padx=5, pady=5, sticky=W)
#     product_kind_combobox = ttk.Combobox(
#         form_frame,
#         values=product_kind_names,  # Use names as display values
#         state="readonly",  # Initial state is dropdown-only
#         width=40,
#     )
#     # product_kind_combobox.pack(pady=10, padx=10)
#     product_kind_combobox.grid(row=1, column=3, columnspan=2, pady=10, padx=10)
#     # tooltip
#     ToolTip(product_kind_combobox, text="Choose a product kind")
#
#     # Label for Date Entry
#
#     date_label = ttk.Label(form_frame, text="Consumption Date:", font=("Helvetica", 10,"bold"))
#     date_label.grid(row=0, column=5, padx=5, pady=5, sticky=W)
#
#     # Date Entry field
#     # Get yesterday's date
#     yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
#     yesterday_date = yesterday.strftime("%m/%d/%Y")  # Format as MM/DD/YYYY
#
#     # Date Entry field with yesterday's date pre-filled
#     date_entry = ttk.Entry(form_frame, width=20)
#     date_entry.insert(0, yesterday_date)
#     date_entry.config(state="readonly")
#     date_entry.grid(row=1, column=5, padx=5, pady=5, sticky=W)
#
#     # Default tooltip
#     ToolTip(date_entry, text="This is the date when raw materials stock moved")
#
#
#     # Add a button to print the selected product kind's ID
#     btn_get_selected = ttk.Button(
#         form_frame,
#         text="+ Add",
#         command=submit_data,  # Call the function to submit the data,
#     )
#     # btn_get_selected.pack(pady=10)
#     btn_get_selected.grid(row=1, column=6, columnspan=2, pady=10)
#
# def get_product_kinds_api():
#     url = server_ip+"/api/product_kinds/temp/list/"
#     response = requests.get(url)
#
#     # Check if the request was successful
#     if response.status_code == 200:
#         # Parse JSON response
#         data = response.json()
#         print("Data fetched successfully!")
#         return data
#     else:
#         print(f"Failed to fetch data. Status code: {response.status_code}")



def entry_fields(note_form_tab):

    # Function to get the selected item's ID
    def get_selected_product_kind_id():
        selected_name = product_kind_combobox.get()
        selected_id = name_to_id.get(selected_name)  # Get the corresponding ID
        if selected_id:
            print(f"Selected: ID={selected_id}, Name={selected_name}")
            return selected_id
        else:
            print("No selection made.")
            return None

    # Function to clear all entry fields
    def clear_fields():
        product_code_entry.delete(0, ttk.END)
        lot_number_entry.delete(0, ttk.END)
        product_kind_combobox.set("")
        yesterday_date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%m/%d/%Y")
        date_entry.config(state="normal")
        date_entry.delete(0, ttk.END)
        date_entry.insert(0, yesterday_date)
        date_entry.config(state="readonly")

    def get_product_kinds_api():
        url = server_ip+"/api/product_kinds/temp/list/"
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse JSON response
            data = response.json()
            print("Data fetched successfully!")
            return data
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")

    # Function to refresh the table after data submission
    def refresh_table():
        # Clear and re-initialize the table
        table(note_form_tab)

    # Function to send POST request
    def submit_data():
        # Collect the form data
        product_code = product_code_entry.get()
        lot_number = lot_number_entry.get()
        product_kind_id = get_selected_product_kind_id()
        consumption_date = date_entry.get()

        # Convert date to YYYY-MM-DD
        try:
            consumption_date = d_datetime.strptime(consumption_date, "%m/%d/%Y").strftime("%Y-%m-%d")
        except ValueError:
            Messagebox.show_error("Error", "Invalid date format. Please use MM/DD/YYYY.")
            return

        # Create a dictionary with the data
        data = {
            "product_code": product_code,
            "lot_number": lot_number,
            "product_kind_id": product_kind_id,
            "stock_change_date": consumption_date
        }

        # Send a POST request to the API
        try:
            response = requests.post(f"{server_ip}/api/notes/temp/create/", json=data)
            if response.status_code == 200:  # Successfully created
                Messagebox.show_info("Success", "Data added successfully!")
                clear_fields()  # Clear all fields

                refresh_table()  # Refresh the table
            else:
                Messagebox.show_error("Error", f"Failed to add data. {response.status_code}")
        except requests.exceptions.RequestException as e:
            Messagebox.show_error("Error", f"An error occurred: {e}")

    # Create a frame for the form inputs
    form_frame = ttk.Frame(note_form_tab)
    form_frame.pack(fill=X, pady=10, padx=20)

    # Product Code Entry
    product_code_label = ttk.Label(form_frame, text="Product Code:", font=("Helvetica", 10, "bold"))
    product_code_label.grid(row=0, column=0, padx=5, pady=5, sticky=W)
    product_code_entry = ttk.Entry(form_frame, width=40)
    product_code_entry.grid(row=1, column=0, padx=5, pady=5)
    ToolTip(product_code_entry, text="Enter the product code")

    # Lot Number Entry
    lot_number_label = ttk.Label(form_frame, text="Lot Number:", font=("Helvetica", 10, "bold"))
    lot_number_label.grid(row=0, column=1, padx=5, pady=5, sticky=W)
    lot_number_entry = ttk.Entry(form_frame, width=40)
    lot_number_entry.grid(row=1, column=1, padx=5, pady=5)
    ToolTip(lot_number_entry, text="Enter the lot number")

    # JSON-format choices
    product_kinds = get_product_kinds_api()
    name_to_id = {item["name"]: item["id"] for item in product_kinds}
    product_kind_names = list(name_to_id.keys())

    # Add a combobox
    product_kind_label = ttk.Label(form_frame, text="Product Kind:", font=("Helvetica", 10, "bold"))
    product_kind_label.grid(row=0, column=3, padx=5, pady=5, sticky=W)
    product_kind_combobox = ttk.Combobox(
        form_frame,
        values=product_kind_names,
        state="readonly",
        width=40,
    )
    product_kind_combobox.grid(row=1, column=3, columnspan=2, pady=10, padx=10)
    ToolTip(product_kind_combobox, text="Choose a product kind")

    # Date Entry field
    date_label = ttk.Label(form_frame, text="Consumption Date:", font=("Helvetica", 10, "bold"))
    date_label.grid(row=0, column=5, padx=5, pady=5, sticky=W)

    yesterday_date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%m/%d/%Y")
    date_entry = ttk.Entry(form_frame, width=20)
    date_entry.insert(0, yesterday_date)
    date_entry.config(state="readonly")
    date_entry.grid(row=1, column=5, padx=5, pady=5, sticky=W)
    ToolTip(date_entry, text="This is the date when raw materials stock moved")

    # Add button to submit data
    btn_submit = ttk.Button(
        form_frame,
        text="+ Add",
        command=submit_data,
    )
    btn_submit.grid(row=1, column=6, columnspan=2, pady=10)






