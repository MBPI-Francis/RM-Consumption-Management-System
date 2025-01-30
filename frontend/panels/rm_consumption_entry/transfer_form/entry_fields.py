import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import requests
from backend.settings.database import server_ip
from ttkbootstrap.tooltip import ToolTip
from ttkbootstrap.dialogs.dialogs import Messagebox
from datetime import datetime, timedelta
from .table import NoteTable
from .validation import EntryValidation as TranferValidation
from tkinter import StringVar
from ..preparation_form.validation import EntryValidation as PrepValidation
from uuid import  UUID

def entry_fields(note_form_tab):
    

    def get_selected_warehouse_from_id():
        selected_name = warehouse_from_combobox.get()
        selected_id = warehouse_to_id.get(selected_name)  # Get the corresponding ID
        if selected_id:
            return selected_id
        else:
            return None

    def get_selected_status_id():
        selected_name = status_combobox.get()
        selected_id = status_to_id.get(selected_name)  # Get the corresponding ID
        if selected_id:
            return selected_id
        else:
            return None

    def get_selected_warehouse_to_id():
        selected_name = warehouse_to_combobox.get()
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
    def clear_fields():

        if not checkbox_reference_var.get():
            ref_number_entry.delete(0, ttk.END)

        if not checkbox_warehouse_var.get():
            warehouse_from_combobox.set("")
            warehouse_to_combobox.set("")

        status_combobox.set("")
        rm_codes_combobox.set("")
        qty_entry.delete(0, ttk.END)

    def check_raw_material(rm_id: UUID, warehouse_id: UUID, status_id: UUID = None):
        url = f"{server_ip}/api/check/raw_material/"  # Replace with the actual URL of your FastAPI server

        # Construct the query parameters
        params = {
            "rm_id": str(rm_id),  # Convert UUID to string for query parameter
            "warehouse_id": str(warehouse_id),
            "status_id": str(status_id) if status_id else None
        }

        try:
            # Send the GET request
            response = requests.get(url, params=params)

            # Check if the response was successful
            if response.status_code == 200:
                # Parse the response data (True or False)
                return response.json()  # This will return either True or False
            else:
                # Handle errors
                print(f"Error: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return False


    def submit_data():

        # Collect the form data
        warehouse_from_id = get_selected_warehouse_from_id()
        warehouse_to_id = get_selected_warehouse_to_id()

        # Validation for the two warehouse choices
        if warehouse_from_id == warehouse_to_id:
            Messagebox.show_error("The Warehouse (FROM) and Warehouse (TO) should be different.", "Data Entry Error")
            return

        rm_code_id = get_selected_rm_code_id()
        status_id = get_selected_status_id()
        ref_number = ref_number_entry.get()
        qty = qty_entry.get()
        transfer_date = transfer_date_entry.entry.get()

        # Convert date to YYYY-MM-DD
        try:
            transfer_date = datetime.strptime(transfer_date, "%m/%d/%Y").strftime("%Y-%m-%d")
        except ValueError:
            Messagebox.show_error("Error", "Invalid date format. Please use MM/DD/YYYY.")
            return

        # Create a dictionary with the data
        data = {
            "rm_code_id": rm_code_id,
            "from_warehouse_id": warehouse_from_id,
            "to_warehouse_id": warehouse_to_id,
            "ref_number": ref_number,
            "status_id": status_id,
            "transfer_date": transfer_date,
            "qty_kg": qty,
        }
        # Validate the data entries in front-end side
        if TranferValidation.entry_validation(data):
            error_text = TranferValidation.entry_validation(data)
            Messagebox.show_error(f"There is no data in these fields {error_text}.", "Data Entry Error", alert=True)
            return




        # Check if the record is existing in the inventory
        # Call the check_raw_material function
        result = check_raw_material(rm_code_id, warehouse_from_id, status_id)
        # Display the result in the GUI
        if result:

            # Validate if the entry value exceeds the stock
            validatation_result = PrepValidation.validate_soh_value(
                rm_code_id,
                warehouse_from_id,
                qty,
                status_id
            )

            if validatation_result:
                    # Send a POST request to the API
                try:
                    response = requests.post(f"{server_ip}/api/transfer_forms/temp/create/", json=data)
                    if response.status_code == 200:  # Successfully created
                        clear_fields()

                        note_table.refresh_table()
                        # refresh_table()  # Refresh the table
                except requests.exceptions.RequestException as e:
                    Messagebox.show_info(e, "Data Entry Error")

            else:
                Messagebox.show_error(
                    "The entered quantity in 'Quantity' exceeds the available stock in the database.",
                    "Data Entry Error")
                return

        else:
            Messagebox.show_error(f"The raw material record is not existing in the database.", "Failed Transfer.", alert=True)
            return


    # Create a frame for the form inputs
    form_frame = ttk.Frame(note_form_tab)
    form_frame.pack(fill=X, pady=10, padx=20)


    # Warehouse JSON-format choices (coming from the API)
    warehouses = get_warehouse_api()
    warehouse_to_id = {item["wh_name"]: item["id"] for item in warehouses}
    warehouse_names = list(warehouse_to_id.keys())

    # Combobox for Warehouse FROM Drop Down
    warehouse_from_label = ttk.Label(form_frame, text="Warehouse (FROM):", font=("Helvetica", 10, "bold"))
    warehouse_from_label.grid(row=0, column=0, padx=5, pady=5, sticky=W)
    warehouse_from_combobox = ttk.Combobox(
        form_frame,
        values=warehouse_names,
        state="readonly",
        width=30,
    )
    warehouse_from_combobox.grid(row=1, column=0, pady=10, padx=10, sticky=W)
    ToolTip(warehouse_from_combobox, text="Choose a warehouse where the raw material is coming from")


    # Combobox for Warehouse TO Drop Down
    warehouse_to_label = ttk.Label(form_frame, text="Warehouse (TO):", font=("Helvetica", 10, "bold"))
    warehouse_to_label.grid(row=0, column=1, padx=5, pady=5, sticky=W)
    warehouse_to_combobox = ttk.Combobox(
        form_frame,
        values=warehouse_names,
        state="readonly",
        width=30,
    )
    warehouse_to_combobox.grid(row=1, column=1, pady=5, padx=5, sticky=W)
    ToolTip(warehouse_to_combobox, text="Choose a warehouse where the raw material is transferred to")



    # Checkbox for Warehouse lock
    checkbox_warehouse_var = ttk.IntVar()  # Integer variable to store checkbox state (0 or 1)
    lock_warehouse = ttk.Checkbutton(
        form_frame,
        text="Lock Warehouse",
        variable=checkbox_warehouse_var,
        bootstyle="round-toggle"
    )
    lock_warehouse.grid(row=1, column=2, pady=5, padx=5, sticky=W)  # Position the checkbox next to the combobox
    ToolTip(lock_warehouse, text="Lock the warehouse by clicking this")

    # REF Number Entry Field
    ref_number_label = ttk.Label(form_frame, text="Reference Number:", font=("Helvetica", 10, "bold"))
    ref_number_label.grid(row=2, column=0, padx=5, pady=5, sticky=W)
    ref_number_entry = ttk.Entry(form_frame, width=30)
    ref_number_entry.grid(row=3, column=0, padx=5, pady=5, sticky=W)
    ToolTip(ref_number_entry, text="Enter the Reference Number")

    checkbox_reference_var = ttk.IntVar()  # Integer variable to store checkbox state (0 or 1)
    # Checkbox beside the combobox
    lock_reference = ttk.Checkbutton(
        form_frame,
        text="Lock Reference Number",
        variable=checkbox_reference_var,
        bootstyle="round-toggle"
    )
    lock_reference.grid(row=3, column=1, pady=5, padx=5, sticky=W)  # Position the checkbox next to the combobox
    ToolTip(lock_reference, text="Lock the reference number by clicking this")

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
        state="readonly",
        width=30,
    )

    rm_codes_combobox.grid(row=5, column=0, pady=5, padx=5, sticky=W)
    ToolTip(rm_codes_combobox, text="Choose a raw material")



    # Status JSON-format choices (coming from the API)
    status = get_status_api()
    status_to_id = {item["name"]: item["id"] for item in status}
    status_names = list(status_to_id.keys())

    # Combobox for Status Drop Down
    status_label = ttk.Label(form_frame, text="Status", font=("Helvetica", 10, "bold"))
    status_label.grid(row=4, column=1, padx=5, pady=5, sticky=W)
    status_combobox = ttk.Combobox(
        form_frame,
        values=status_names,
        state="normal",
        width=30,
    )
    status_combobox.grid(row=5, column=1, pady=10, padx=10, sticky=W)
    ToolTip(status_combobox, text="Choose the current status")




    # Register the validation command
    validate_numeric_command = form_frame.register(TranferValidation.validate_numeric_input)

    # Quantity Entry Field
    qty_label = ttk.Label(form_frame, text="Quantity:", font=("Helvetica", 10, "bold"))
    qty_label.grid(row=4, column=2, pady=5, padx=5, sticky=W)
    qty_entry = ttk.Entry(form_frame,
                          width=30,
                          validate="key",  # Trigger validation on keystrokes
                          validatecommand=(validate_numeric_command, "%P")  # Pass the current widget content ("%P")
)
    qty_entry.grid(row=5, column=2, pady=5, padx=5, sticky=W)
    ToolTip(qty_entry, text="Enter the Quantity(kg)")


    # Date Entry field
    date_label = ttk.Label(form_frame, text="Outgoing Date:", font=("Helvetica", 10, "bold"))
    date_label.grid(row=4, column=3, padx=5, pady=5, sticky=W)

    # Calculate yesterday's date
    yesterday_date = datetime.now() - timedelta(days=1)

    # Create the DateEntry widget with yesterday's date as the default value
    transfer_date_entry = ttk.DateEntry(
        form_frame,
        bootstyle=PRIMARY,
        dateformat="%m/%d/%Y",
        startdate=yesterday_date,  # Set yesterday's date
        width=20
    )
    transfer_date_entry.grid(row=5, column=3, padx=5, pady=5, sticky=W)

    ToolTip(transfer_date_entry, text="This is the transfer date.")

    # Add button to submit data
    btn_submit = ttk.Button(
        form_frame,
        text="+ Add",
        command=submit_data,
        width=10
    )
    btn_submit.grid(row=5, column=6, pady=10)

    # Calling the table
    note_table = NoteTable(note_form_tab)


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


def get_status_api():
    url = server_ip + "/api/droplist/list/"
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse JSON response
        data = response.json()
        print("Data fetched successfully!")
        return data
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")








