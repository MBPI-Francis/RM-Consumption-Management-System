import ttkbootstrap as ttk
from click.termui import raw_terminal
from ttkbootstrap.constants import *
import requests
from backend.settings.database import server_ip
from ttkbootstrap.tooltip import ToolTip
from ttkbootstrap.dialogs.dialogs import Messagebox
from datetime import datetime, timedelta
from .table import NoteTable
from .validation import EntryValidation
from tkinter import StringVar


def entry_fields(note_form_tab):

        # Function to clear all entry fields
    def clear_fields():
        rm_code_entry.delete(0, ttk.END)


    def submit_data():
        # Collect the form data
        rm_code = rm_code_entry.get()


        # Create a dictionary with the data
        data = {
            "rm_code": rm_code,
        }

        print("This is the data: ", data)

        # Validate the data entries in front-end side
        if EntryValidation.entry_validation(data):
            error_text = EntryValidation.entry_validation(data)
            Messagebox.show_error(f"There is no data in these fields {error_text}.", "Data Entry Error", alert=True)
            return

            # Send a POST request to the API
        try:
            response = requests.post(f"{server_ip}/api/raw_materials/create/", json=data)
            if response.status_code == 200:  # Successfully created
                clear_fields()

                note_table.refresh_table()
                # refresh_table()  # Refresh the table
        except requests.exceptions.RequestException as e:
            Messagebox.show_info(e, "Data Entry Error")



    # Create a frame for the form inputs
    form_frame = ttk.Frame(note_form_tab)
    form_frame.pack(fill=X, pady=10, padx=20)


    # Raw Material Code Entry Field
    rm_code_label = ttk.Label(form_frame, text="Raw Material Code:", font=("Helvetica", 10, "bold"))
    rm_code_label.grid(row=0, column=0, padx=5, pady=5, sticky=W)
    rm_code_entry = ttk.Entry(form_frame, width=30)
    rm_code_entry.grid(row=1, column=0, padx=5, pady=5)
    ToolTip(rm_code_entry, text="Add New Raw Material Code")


    # Add button to submit data
    btn_submit = ttk.Button(
        form_frame,
        text="+ Add",
        command=submit_data,
    )
    btn_submit.grid(row=1, column=2, columnspan=2, pady=10)

    # Calling the table
    note_table = NoteTable(note_form_tab)








