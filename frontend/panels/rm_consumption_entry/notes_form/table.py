import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *
import requests
from backend.settings.database import server_ip
from datetime import datetime


def table(note_form_tab):
    # Define column and row data
    coldata = [
        {"text": "Product Code", "stretch": True},
        {"text": "Lot No.", "stretch": True},
        {"text": "Product Kind", "stretch": True},
        {"text": "Consumption Date", "stretch": True},
        {"text": "Entry Date", "stretch": True},
    ]

    rowdata = get_notes_data_api()

    # Create Tableview
    dt = Tableview(
        master=note_form_tab,
        coldata=coldata,
        rowdata=rowdata,
        paginated=True,
        searchable=True,
        bootstyle=PRIMARY,

    )


    # Pack the Tableview
    dt.pack(fill=BOTH, expand=YES, padx=10, pady=10)


def get_notes_data_api():
    # API endpoint
    url = server_ip + "/api/notes/temp/list/"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP status codes 4xx/5xx

        # Parse the JSON response
        data = response.json()
        print(data)
        # Transform the JSON data into a format suitable for rowdata
        # Assuming the JSON response looks like this:
        # [{"product_code": "A123", "lot_no": "IzzyCo", "product_kind": "asd", "consumption_date": "2025-01-16", "entry_date": "2025-01-15"}, ...]
        rowdata = [
            (
                item["product_code"],
                item["lot_number"],
                item["product_kind_id"],
                datetime.fromisoformat(item["stock_change_date"]).strftime("%m/%d/%Y"),
                datetime.fromisoformat(item["created_at"]).strftime("%m/%d/%Y %I:%M %p")
            )
            for item in data
        ]
        return rowdata
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return []  # Return an empty list if there's an error
