import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import requests
from backend.settings.database import server_ip
from ttkbootstrap.tooltip import ToolTip
from ttkbootstrap.dialogs.dialogs import Messagebox
from datetime import datetime, timedelta
from .table import NoteTable
from .validation import EntryValidation
from tkinter import StringVar
import psycopg2


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
    def clear_fields():

        if not checkbox_reference_var.get():
            ref_number_entry.delete(0, ttk.END)

        if not checkbox_warehouse_var.get():
            warehouse_combobox.set("")
        rm_codes_combobox.set("")
        qty_prepared_entry.delete(0, ttk.END)
        qty_return_entry.delete(0, ttk.END)

    def get_status_id():
        query = f"SELECT id FROM tbl_droplist WHERE name = 'good'"
        # Assuming you have a PostgreSQL connection (replace with your connection details)
        connection = psycopg2.connect(
            dbname="RMManagementSystemDB", user="postgres", password="mbpi", host="192.168.1.13", port="5432"
        )

        # connection = psycopg2.connect(
        #     dbname="RMManagementSystemDB", user="postgres", password="331212", host="localhost", port="5432"
        # )
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        connection.close()

        return result[0] if result else None


    def submit_data():

        # Collect the form data
        warehouse_id = get_selected_warehouse_id()
        rm_code_id = get_selected_rm_code_id()
        ref_number = ref_number_entry.get()
        qty_prepared = qty_prepared_entry.get()
        qty_return = qty_return_entry.get()
        preparation_date = preparation_date_entry.entry.get()
        status_id = get_status_id()

        # Set focus to the Entry field
        rm_codes_combobox.focus_set()


        # If the user didn't enter a value in the qty return field, then it will store 0.00 value in the variable
        if qty_return == None or qty_return == '':
            qty_return = float(0.00)


        # Convert date to YYYY-MM-DD
        try:
            preparation_date = datetime.strptime(preparation_date, "%m/%d/%Y").strftime("%Y-%m-%d")
        except ValueError:
            Messagebox.show_error("Error", "Invalid date format. Please use MM/DD/YYYY.")
            return

        # Create a dictionary with the data
        data = {
            "rm_code_id": rm_code_id,
            "warehouse_id": warehouse_id,
            "ref_number": ref_number,
            "preparation_date": preparation_date,
            "qty_prepared": qty_prepared,
            "qty_return": qty_return,
        }



        # Validate the data entries in front-end side
        if EntryValidation.entry_validation(data):
            error_text = EntryValidation.entry_validation(data)
            Messagebox.show_error(f"There is no data in these fields {error_text}.", "Data Entry Error", alert=True)
            return

        validatation_result = EntryValidation.validate_soh_value(
            rm_code_id,
            warehouse_id,
            qty_prepared,
            status_id
        )
        if validatation_result:
            # Send a POST request to the API
            try:
                response = requests.post(f"{server_ip}/api/preparation_forms/temp/create/", json=data)
                if response.status_code == 200:  # Successfully created
                    clear_fields()
                    note_table.refresh_table()
                    # refresh_table()  # Refresh the table
            except requests.exceptions.RequestException as e:
                Messagebox.show_error(e, "Data Entry Error")

        else:
            Messagebox.show_error(
                "The entered quantity in 'Quantity (Prepared)' exceeds the available stock in the database.",
                "Data Entry Error")
            return


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

    # Checkbox for Warehouse lock
    checkbox_warehouse_var = ttk.IntVar()  # Integer variable to store checkbox state (0 or 1)
    lock_warehouse = ttk.Checkbutton(
        form_frame,
        text="Lock Warehouse",
        variable=checkbox_warehouse_var,
        bootstyle="round-toggle"
    )
    lock_warehouse.grid(row=1, column=3, pady=10, padx=10, sticky=W)  # Position the checkbox next to the combobox
    ToolTip(lock_warehouse, text="Lock the warehouse by clicking this")

    # REF Number Entry Field
    ref_number_label = ttk.Label(form_frame, text="Reference Number:", font=("Helvetica", 10, "bold"))
    ref_number_label.grid(row=2, column=0, padx=5, pady=5, sticky=W)
    ref_number_entry = ttk.Entry(form_frame, width=30)
    ref_number_entry.grid(row=3, column=0, padx=5, pady=5)
    ToolTip(ref_number_entry, text="Enter the Reference Number")

    checkbox_reference_var = ttk.IntVar()  # Integer variable to store checkbox state (0 or 1)
    # Checkbox beside the combobox
    lock_reference = ttk.Checkbutton(
        form_frame,
        text="Lock Reference Number",
        variable=checkbox_reference_var,
        bootstyle="round-toggle"
    )
    lock_reference.grid(row=3, column=3, pady=10, padx=10, sticky=W)  # Position the checkbox next to the combobox
    ToolTip(lock_reference, text="Lock the reference number by clicking this")

    #RM CODE JSON-format choices (coming from the API)
    rm_codes = get_rm_code_api()
    code_to_id = {item["rm_code"]: item["id"] for item in rm_codes}
    rm_names = list(code_to_id.keys())


    # Function to convert typed input to uppercase
    def on_combobox_key_release(event):
        # Get the current text in the combobox
        current_text = rm_codes_combobox.get()
        # Convert the text to uppercase and set it back
        rm_codes_combobox.set(current_text.upper())

    # Combobox for RM CODE Drop Down
    rm_codes_label = ttk.Label(form_frame, text="Raw Material:", font=("Helvetica", 10, "bold"))
    rm_codes_label.grid(row=4, column=0, padx=5, pady=5, sticky=W)

    rm_codes_combobox = ttk.Combobox(
        form_frame,
        values=rm_names,
        state="normal",
        width=30,
    )

    # Bind the key release event to the combobox to trigger uppercase conversion
    rm_codes_combobox.bind("<KeyRelease>", on_combobox_key_release)

    rm_codes_combobox.grid(row=5, column=0, columnspan=2, pady=10, padx=10)
    ToolTip(rm_codes_combobox, text="Choose a raw material")


    # Register the validation command

    validate_numeric_command = form_frame.register(EntryValidation.validate_numeric_input)

    # Quantity (Prepared) Entry Field
    qty_prepared_label = ttk.Label(form_frame, text="Quantity (Prepared):", font=("Helvetica", 10, "bold"))
    qty_prepared_label.grid(row=4, column=3, padx=5, pady=5, sticky=W)
    qty_prepared_entry = ttk.Entry(form_frame,
                          width=30,
                          validate="key",  # Trigger validation on keystrokes
                          validatecommand=(validate_numeric_command, "%P")  # Pass the current widget content ("%P")
)
    qty_prepared_entry.grid(row=5, column=3, padx=5, pady=5)
    ToolTip(qty_prepared_entry, text="Enter the Quantity(kg)")


    # Quantity (Return) Entry Field
    qty_return_label = ttk.Label(form_frame, text="Quantity (Return):", font=("Helvetica", 10, "bold"))
    qty_return_label.grid(row=4, column=5, padx=5, pady=5, sticky=W)
    qty_return_entry = ttk.Entry(form_frame,
                          width=30,
                          validate="key",  # Trigger validation on keystrokes
                          validatecommand=(validate_numeric_command, "%P")  # Pass the current widget content ("%P")
                          )
    qty_return_entry.grid(row=5, column=5, padx=5, pady=5)
    ToolTip(qty_return_entry, text="Enter the Quantity(kg)")




    # Date Entry field
    date_label = ttk.Label(form_frame, text="Preparation Date:", font=("Helvetica", 10, "bold"))
    date_label.grid(row=4, column=7, padx=5, pady=5, sticky=W)

    # Calculate yesterday's date
    yesterday_date = datetime.now() - timedelta(days=1)

    # Create the DateEntry widget with yesterday's date as the default value
    preparation_date_entry = ttk.DateEntry(
        form_frame,
        bootstyle=PRIMARY,
        dateformat="%m/%d/%Y",
        startdate=yesterday_date,  # Set yesterday's date
        width=30
    )
    preparation_date_entry.grid(row=5, column=7, padx=5, pady=5, sticky=W)

    ToolTip(preparation_date_entry, text="This is the outgoing date.")

    # Add button to submit data
    btn_submit = ttk.Button(
        form_frame,
        text="+ Add",
        command=submit_data,
    )
    btn_submit.grid(row=5, column=8, columnspan=2, pady=10)

    # Calling the table
    note_table = NoteTable(note_form_tab)


def get_warehouse_api():
    url = server_ip + "/api/warehouses/list/"
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse JSON response
        data = response.json()

        return data
    else:
        return []



def get_rm_code_api():
    url = server_ip + "/api/raw_materials/list/"
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse JSON response
        data = response.json()

        return data
    else:
        return []








