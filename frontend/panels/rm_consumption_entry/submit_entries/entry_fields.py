import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import requests
from backend.settings.database import server_ip
from ttkbootstrap.tooltip import ToolTip
from ttkbootstrap.dialogs.dialogs import Messagebox
from datetime import datetime, timedelta
from .table import NoteTable
import tkinter as tk
import os
from ttkbootstrap import Style
from tkinter.filedialog import asksaveasfilename
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from openpyxl.worksheet.datavalidation import DataValidation
import psycopg2  # PostgreSQL library


def entry_fields(note_form_tab):

    # Function to clear all entry fields
    def clear_fields():
        if not checkbox_date_var.get():  # Clear only if checkbox_date_var is False
            date_entry.entry.delete(0, tk.END)


    def btn_clear():
        """Fetch data from API and format for table rowdata."""
        url = f"{server_ip}/api/clear-table-data"
        try:
            # Send another POST request to clear data
            response = requests.post(url)
            if response.status_code == 200:  # Check if the stock view was successfully created
                print("Successfully Cleared the Data")
                Messagebox.show_info("Data is successfully cleared!", "Data Clearing")

            else:
                print(f"There is an error:  {response.status_code}")
                Messagebox.show_error(f"There must be a mistake, the status code is {response.status_code}", "Data Clearing Error")

        except requests.exceptions.RequestException as e:
            return False


    def submit_data():

        date_entry_value = date_entry.entry.get()

        # Convert date to YYYY-MM-DD
        try:
            date_entry_value = datetime.strptime(date_entry_value, "%m/%d/%Y").strftime("%Y-%m-%d")
        except ValueError:
            Messagebox.show_error("Error", "Invalid date format. Please use MM/DD/YYYY.")
            return

        try:

            # Call the function to get all the data from the view table
            data = get_soh_data()
            print("This is the data: ", data)

            # Generate an Excel file for the stock-on-hand data
            create_soh_whse_excel(date_entry_value, data)


            try:
                # Send another POST request to update the stocks
                response = requests.post(f"{server_ip}/api/update_stock_on_hand/?params_date={date_entry_value}")
                if response.status_code == 200:  # Check if the stock view was successfully created
                    print("Successfully Updated the Stocks.")

            except requests.exceptions.RequestException as e:
                # Show an error message if the second POST request fails
                Messagebox.show_info(e, "Data Entry Error")

            try:
                # Send a POST request to update the computed date in the API
                response = requests.post(f"{server_ip}/api/update-date-computed")
                if response.status_code == 200:  # Check if the request was successful
                    print("Successfully Updated the Computed Date")
            except requests.exceptions.RequestException as e:
                # Show an error message if the second POST request fails
                Messagebox.show_info(e, "Data Entry Error")





            # Clear input fields after successful operation
            clear_fields()

            # Refresh the note table to display updated data
            note_table.refresh_table()
        except requests.exceptions.RequestException as e:
            # Show an error message if the first POST request fails
            Messagebox.show_info(e, "Data Entry Error")

    # Create a frame for the form inputs
    form_frame = ttk.Frame(note_form_tab)
    form_frame.pack(fill=X, pady=10, padx=20)


    # Checkbox for Warehouse lock
    checkbox_date_var = ttk.BooleanVar(value=False)  # Integer variable to store checkbox state (0 or 1)
    lock_warehouse = ttk.Checkbutton(
        form_frame,
        text="Lock Date",
        variable=checkbox_date_var,
        bootstyle="round-toggle"
    )
    lock_warehouse.grid(row=0, column=0, pady=10, padx=10, sticky=W)  # Position the checkbox next to the combobox
    ToolTip(lock_warehouse, text="Lock the date")


    # Calculate yesterday's date
    yesterday_date = datetime.now() - timedelta(days=1)

    # Create the DateEntry widget with yesterday's date as the default value
    date_entry = ttk.DateEntry(
        form_frame,
        bootstyle=PRIMARY,
        dateformat="%m/%d/%Y",
        startdate=yesterday_date,  # Set yesterday's date
        width=30
    )
    date_entry.grid(row=1, column=0, padx=5, pady=5, sticky=W)

    ToolTip(date_entry, text="This is the outgoing date.")


    # Add button to submit data
    btn_submit = ttk.Button(
        form_frame,
        text="Calculate Data",
        command=submit_data,
    )
    btn_submit.grid(row=1, column=2, pady=10)
    ToolTip(btn_submit, text="Click the button to calculate all the entered data.")


    # Add button to clear data
    btn_clear = ttk.Button(
        form_frame,
        text="Clear Data",
        command=btn_clear,
    )
    btn_clear.grid(row=1, column=6, pady=30, padx=10)
    ToolTip(btn_clear, text="Click the button to clear all the data.")

    # Calling the table
    note_table = NoteTable(note_form_tab)


def create_soh_whse_excel(date_entry_value, data):
    # Convert the string into a datetime object
    notes_date_object = datetime.strptime(date_entry_value, "%Y-%m-%d")
    notes_formatted_date = notes_date_object.strftime("%B %d, %Y")
    notes_date = notes_formatted_date

    wh_date_object = datetime.strptime(date_entry_value, "%Y-%m-%d")
    wh_formatted_date = wh_date_object.strftime("%m/%d/%Y")
    wh_date = wh_formatted_date

    # Create a new workbook
    wb = Workbook()

    # Sheet 1: NOTES
    notes_sheet = wb.active
    notes_sheet.title = "NOTES"

    # Populate the NOTES sheet
    notes_sheet["A1"] = "Daily Ending Inventory Report from:"
    notes_sheet["B1"] = f"{notes_date}"  # Sample date
    notes_sheet["A2"] = "List of Batches Included in Report"
    notes_sheet["A3"] = "MASTERBATCH"
    notes_sheet.append(["PRODUCT CODE", "LOT#", "Product Kind"])

    # Example data for the notes sheet
    notes_sheet.append(["SAMPLE-CODE-1", "SAMPLE-5106AJ-5109AJ", "SAMPLE-MB"])
    notes_sheet.append(["SAMPLE-CODE-2", "SAMPLE-5110AJ", "SAMPLE-DC"])

    # Apply formatting
    for col in ["A", "B", "C"]:
        for cell in notes_sheet[col]:
            cell.alignment = Alignment(horizontal="center", vertical="center")
    notes_sheet["A4"].font = Font(bold=True)

    # Function to create a WHSE sheet
    def create_whse_sheet(sheet_name):
        sheet = wb.create_sheet(sheet_name)

        # Set header based on warehouse number
        if sheet_name == "WHSE1":
            wh_header = "WHSE #1 - Excess"
        elif sheet_name == "WHSE2":
            wh_header = "WHSE #2 - Excess"
        elif sheet_name == "WHSE4":
            wh_header = "WHSE #4 - Excess"

        # Populate the header
        header = [
            "Date", "No of bags", "qty per packing",
            f"{wh_header}", "Total", "Status"
        ]
        sheet.append(header)
        sheet["A1"] = f"{wh_date}"  # Example date
        sheet["A1"].font = Font(bold=True)

        # Insert data into the respective warehouse sheet
        for record in data:
            if record["warehousenumber"] == int(sheet_name[-1]):  # Match warehouse number to sheet
                row = [
                    record["rmcode"],  # rmcode
                    "",  # No of bags (blank)
                    "",  # qty per packing (blank)
                    "",  # Excess column (blank)
                    float(record["new_beginning_balance"]),  # Total
                    record["status"],  # Status
                    ""  # Drop list (blank)
                ]
                sheet.append(row)

        # Create a dropdown list for the "drop list" column
        dv = DataValidation(
            type="list",
            formula1='"held : under evaluation,held : reject,held : contaminated"',
            allow_blank=True,
            showDropDown=True
        )
        # Apply the data validation to the G column for rows 2 to 100
        for row in range(2, 101):
            cell = f"G{row}"  # Example: G2, G3, ..., G100
            dv.add(sheet[cell])
        sheet.add_data_validation(dv)

    # Create sheets for WHSE1, WHSE2, and WHSE4
    create_whse_sheet("WHSE1")
    create_whse_sheet("WHSE2")
    create_whse_sheet("WHSE4")

    # Initialize ttkbootstrap Style and create the dialog
    style = Style("cosmo")
    root = style.master
    root.withdraw()  # Hide the root window

    # Use tkinter's asksaveasfilename for file dialog
    file_path = asksaveasfilename(
        title="Save Excel File",
        defaultextension=".xlsx",
        filetypes=[("Excel files", "*.xlsx")]
    )

    # Save the workbook
    if file_path:
        try:
            wb.save(file_path)
            print(f"Excel file saved successfully at {file_path}")
        except Exception as e:
            print(f"Error saving file: {e}")
    else:
        print("File save canceled by the user.")

def get_soh_data():

    """Fetch data from API and format for table rowdata."""
    url = f"{server_ip}/api/get/new_soh/"
    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return []

    # Return both buttons as a tuple
    return []







