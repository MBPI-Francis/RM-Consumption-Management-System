import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import requests
from backend.settings.database import server_ip
from ttkbootstrap.tooltip import ToolTip
from ttkbootstrap.dialogs.dialogs import Messagebox
from datetime import datetime, timedelta
from .table import NoteTable
from .validation import EntryValidation


def entry_fields(note_form_tab):
    def get_selected_product_kind_id():
        selected_name = product_kind_combobox.get()
        selected_id = name_to_id.get(selected_name)  # Get the corresponding ID
        if selected_id:
            return selected_id
        else:
            return None

        # Function to clear all entry fields
    def clear_fields():

        product_code_entry.delete(0, ttk.END)
        lot_number_entry.delete(0, ttk.END)
        product_kind_combobox.set("")

    def submit_data():

        # Collect the form data
        product_code = product_code_entry.get()
        lot_number = lot_number_entry.get()
        product_kind_id = get_selected_product_kind_id()
        consumption_date = date_entry.entry.get()

        # Convert date to YYYY-MM-DD
        try:
            consumption_date = datetime.strptime(consumption_date, "%m/%d/%Y").strftime("%Y-%m-%d")
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

        # Validate the data entries in front-end side
        if EntryValidation.entry_validation(data):
            error_text = EntryValidation.entry_validation(data)
            Messagebox.show_error(f"There is no data in these fields {error_text}.", "Data Entry Error", alert=True)
            return

            # Send a POST request to the API
        try:
            response = requests.post(f"{server_ip}/api/notes/temp/create/", json=data)
            if response.status_code == 200:  # Successfully created
                clear_fields()

                note_table.load_data()
                # refresh_table()  # Refresh the table
        except requests.exceptions.RequestException as e:
            Messagebox.show_info(e, "Data Entry Error")

        # Function to get the selected item's ID




    # Function to send POST request

    # Create a frame for the form inputs
    form_frame = ttk.Frame(note_form_tab)
    form_frame.pack(fill=X, pady=10, padx=20)

    # Product Code Entry Field
    product_code_label = ttk.Label(form_frame, text="Product Code:", font=("Helvetica", 10, "bold"))
    product_code_label.grid(row=0, column=0, padx=5, pady=5, sticky=W)
    product_code_entry = ttk.Entry(form_frame, width=30)
    product_code_entry.grid(row=1, column=0, padx=5, pady=5)
    ToolTip(product_code_entry, text="Enter the product code")

    # Lot Number Entry Field
    lot_number_label = ttk.Label(form_frame, text="Lot Number:", font=("Helvetica", 10, "bold"))
    lot_number_label.grid(row=0, column=1, padx=5, pady=5, sticky=W)
    lot_number_entry = ttk.Entry(form_frame, width=30)
    lot_number_entry.grid(row=1, column=1, padx=5, pady=5)
    ToolTip(lot_number_entry, text="Enter the lot number")

    # Product Kind JSON-format choices (coming from the API)
    product_kinds = get_product_kinds_api()
    name_to_id = {item["name"]: item["id"] for item in product_kinds}
    product_kind_names = list(name_to_id.keys())

    # Combobox for Product Kind Drop Down
    product_kind_label = ttk.Label(form_frame, text="Product Kind:", font=("Helvetica", 10, "bold"))
    product_kind_label.grid(row=0, column=3, padx=5, pady=5, sticky=W)
    product_kind_combobox = ttk.Combobox(
        form_frame,
        values=product_kind_names,
        state="readonly",
        width=20,
    )
    product_kind_combobox.grid(row=1, column=3, columnspan=2, pady=10, padx=10)
    ToolTip(product_kind_combobox, text="Choose a product kind")

    # Date Entry field
    date_label = ttk.Label(form_frame, text="Consumption Date:", font=("Helvetica", 10, "bold"))
    date_label.grid(row=0, column=5, padx=5, pady=5, sticky=W)

    # Calculate yesterday's date
    yesterday_date = datetime.now() - timedelta(days=1)

    date_entry = ttk.DateEntry(
        form_frame,
        bootstyle=PRIMARY,
        dateformat="%m/%d/%Y",
        startdate=yesterday_date,  # Set yesterday's date
        width=30
    )

    date_entry.grid(row=1, column=5, padx=5, pady=5, sticky=W)
    ToolTip(date_entry, text="This is the date when raw materials stock moved")

    # Add button to submit data
    btn_submit = ttk.Button(
        form_frame,
        text="+ Add",
        command=submit_data,
    )
    btn_submit.grid(row=1, column=6, columnspan=2, pady=10)


    note_table = NoteTable(note_form_tab)


def get_product_kinds_api():
    url = server_ip + "/api/product_kinds/temp/list/"
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse JSON response
        data = response.json()
        print("Data fetched successfully!")
        return data
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")










