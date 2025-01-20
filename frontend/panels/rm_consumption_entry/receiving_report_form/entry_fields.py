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

    def get_selected_warehouse_id():
        selected_name = warehouse_combobox.get()
        selected_id = warehouse_to_id.get(selected_name)  # Get the corresponding ID
        if selected_id:
            return selected_id
        else:
            return None

    def get_selected_rm_code_id():
        selected_name = rm_codes_combobox.get()
        selected_id = code_to_id.get(selected_name)  # Get the corresponding ID
        if selected_id:
            return selected_id
        else:
            return None

        # Function to clear all entry fields
    def clear_fields(flag=None):

        warehouse_combobox.set("")
        rm_codes_combobox.set("")
        ref_number_entry.delete(0, ttk.END)
        qty_entry.delete(0, ttk.END)

        # yesterday_date = (datetime.now() - timedelta(days=1)).strftime("%m/%d/%Y")
        # received_date_entry.config(state="normal")
        # received_date_entry.delete(0, ttk.END)
        # received_date_entry.insert(0, yesterday_date)
        # received_date_entry.config(state="readonly")


    # You need to finish this code. This code is for the
    def get_selected_latest_rm_api():

        url = server_ip + "/api/stock_on_hand/list/"
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse JSON response
            data = response.json()
            print("Data fetched successfully!")
            return data
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")

    def submit_data():

        # Collect the form data
        warehouse_id = get_selected_warehouse_id()
        rm_code_id = get_selected_rm_code_id()
        ref_number = ref_number_entry.get()
        qty = qty_entry.get()
        received_date = received_date_entry.entry.get()


        # Convert date to YYYY-MM-DD
        try:
            received_date = datetime.strptime(received_date, "%m/%d/%Y").strftime("%Y-%m-%d")
        except ValueError:
            Messagebox.show_error("Error", "Invalid date format. Please use MM/DD/YYYY.")
            return

        # Create a dictionary with the data
        data = {
            "rm_code_id": rm_code_id,
            "warehouse_id": warehouse_id,
            "ref_number": ref_number,
            "receiving_date": received_date,
            "qty_kg": qty,
        }

        print("This is the data: ", data)

        # Validate the data entries in front-end side
        if EntryValidation.entry_validation(data):
            error_text = EntryValidation.entry_validation(data)
            Messagebox.show_error(f"There is no data in these fields {error_text}.", "Data Entry Error", alert=True)
            return

            # Send a POST request to the API
        try:
            response = requests.post(f"{server_ip}/api/receiving_reports/temp/create/", json=data)
            if response.status_code == 200:  # Successfully created
                clear_fields()

                note_table.refresh_table()
                # refresh_table()  # Refresh the table
        except requests.exceptions.RequestException as e:
            Messagebox.show_info(e, "Data Entry Error")



    # Create a frame for the form inputs
    form_frame = ttk.Frame(note_form_tab)
    form_frame.pack(fill=X, pady=10, padx=20)


    # Warehouse JSON-format choices (coming from the API)
    warehouses = get_warehouse_api()
    warehouse_to_id = {item["wh_name"]: item["id"] for item in warehouses}
    warehouse_names = list(warehouse_to_id.keys())

    # Combobox for Warehouse Drop Down
    warehouse_label = ttk.Label(form_frame, text="Warehouse:", font=("Helvetica", 10, "bold"))
    warehouse_label.grid(row=0, column=0, padx=5, pady=5, sticky=W)
    warehouse_combobox = ttk.Combobox(
        form_frame,
        values=warehouse_names,
        state="readonly",
        width=30,
    )
    warehouse_combobox.grid(row=1, column=0, columnspan=2, pady=10, padx=10)
    ToolTip(warehouse_combobox, text="Choose a warehouse")




    # REF Number Entry Field
    ref_number_label = ttk.Label(form_frame, text="Reference Number:", font=("Helvetica", 10, "bold"))
    ref_number_label.grid(row=2, column=0, padx=5, pady=5, sticky=W)
    ref_number_entry = ttk.Entry(form_frame, width=30)
    ref_number_entry.grid(row=3, column=0, padx=5, pady=5)
    ToolTip(ref_number_entry, text="Enter the Reference Number")



    #RM CODE JSON-format choices (coming from the API)
    rm_codes = get_rm_code_api()
    code_to_id = {item["rm_code"]: item["id"] for item in rm_codes}
    rm_names = list(code_to_id.keys())


    # Combobox for RM CODE Drop Down
    rm_codes_label = ttk.Label(form_frame, text="Raw Material:", font=("Helvetica", 10, "bold"))
    rm_codes_label.grid(row=4, column=0, padx=5, pady=5, sticky=W)
    rm_codes_combobox = ttk.Combobox(
        form_frame,
        values=rm_names,
        state="normal",
        width=30,
    )
    rm_codes_combobox.grid(row=5, column=0, columnspan=2, pady=10, padx=10)
    ToolTip(rm_codes_combobox, text="Choose a warehouse")



    # Quantity Entry Field
    qty_label = ttk.Label(form_frame, text="Quantity:", font=("Helvetica", 10, "bold"))
    qty_label.grid(row=4, column=3, padx=5, pady=5, sticky=W)
    qty_entry = ttk.Entry(form_frame, width=30)
    qty_entry.grid(row=5, column=3, padx=5, pady=5)
    ToolTip(qty_entry, text="Enter the Quantity(kg)")

    # Date Entry field
    date_label = ttk.Label(form_frame, text="Receiving Date:", font=("Helvetica", 10, "bold"))
    date_label.grid(row=4, column=5, padx=5, pady=5, sticky=W)

    # Calculate yesterday's date
    yesterday_date = datetime.now() - timedelta(days=1)

    # Create the DateEntry widget with yesterday's date as the default value
    received_date_entry = ttk.DateEntry(
        form_frame,
        bootstyle=PRIMARY,
        dateformat="%m/%d/%Y",
        startdate=yesterday_date,  # Set yesterday's date
        width=30
    )
    received_date_entry.grid(row=5, column=5, padx=5, pady=5, sticky=W)

    ToolTip(received_date_entry, text="This is the receiving date.")

    # Add button to submit data
    btn_submit = ttk.Button(
        form_frame,
        text="+ Add",
        command=submit_data,
    )
    btn_submit.grid(row=5, column=6, columnspan=2, pady=10)

    # Calling the table
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




def get_warehouse_api():
    url = server_ip + "/api/warehouses/list/"
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse JSON response
        data = response.json()
        print("Data fetched successfully!")
        return data
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")



def get_rm_code_api():
    url = server_ip + "/api/raw_materials/list/"
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse JSON response
        data = response.json()
        print("Data fetched successfully!")
        return data
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")











