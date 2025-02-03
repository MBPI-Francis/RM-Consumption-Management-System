import requests
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import requests
from backend.settings.database import server_ip
from ttkbootstrap.dialogs.dialogs import Messagebox
from datetime import datetime as d_datetime
from validation import EntryValidation


class CRUD:
    def submit_data(self):
        from form_elements import EntryFields

        # Collect the form data
        product_code = EntryFields.entry_fields().product_code_entry.get()
        lot_number = EntryFields.entry_fields().lot_number_entry.get()
        product_kind_id = EntryFields.entry_fields().get_selected_product_kind_id()
        consumption_date = EntryFields.entry_fields().date_entry.get()

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


        # Validate the data entries in front-end side
        if EntryValidation.entry_validation(data):
            error_text = EntryValidation.entry_validation(data)
            Messagebox.show_error(f"There is no data in these fields {error_text}.", "Data Entry Error", alert=True)
            return


   # Function to get the selected item's ID
    def get_selected_product_kind_id(self):
        selected_name = product_kind_combobox.get()
        selected_id = name_to_id.get(selected_name)  # Get the corresponding ID
        if selected_id:
            return selected_id
        else:
            return None

    # Function to clear all entry fields
    def clear_fields(self):
        product_code_entry.delete(0, ttk.END)
        lot_number_entry.delete(0, ttk.END)
        product_kind_combobox.set("")
        yesterday_date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%m/%d/%Y")
        date_entry.config(state="normal")
        date_entry.delete(0, ttk.END)
        date_entry.insert(0, yesterday_date)
        date_entry.config(state="readonly")

