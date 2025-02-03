import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import requests
from backend.settings.database import server_ip
from ttkbootstrap.tooltip import ToolTip
from crud import CRUD
from api_requests import ApiRequest
from ttkbootstrap.dialogs.dialogs import Messagebox
from datetime import datetime as d_datetime
import datetime
from .table import table


class EntryFields:
    def __init__(self, note_form_tab):
        self.note_from_tab = note_form_tab

    def entry_fields(self):

        # Function to send POST request

        # Create a frame for the form inputs
        form_frame = ttk.Frame(self.note_form_tab)
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
        product_kinds = ApiRequest.get_product_kinds_api()
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
            command=CRUD.submit_data,
        )
        btn_submit.grid(row=1, column=6, columnspan=2, pady=10)

        entry_fields_list = {
            "product_code_entry": product_code_entry,
            "lot_number": lot_number_entry,
            "product_kind_id": product_kind_combobox,
            "consumption_date": date_entry
        }

        return entry_fields_list






