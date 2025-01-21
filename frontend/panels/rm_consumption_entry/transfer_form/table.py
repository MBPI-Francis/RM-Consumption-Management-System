import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *
import requests
from backend.settings.database import server_ip
from datetime import datetime


class NoteTable:

    def __init__(self, root):
        self.note_form_tab = root

        self.coldata = [
            {"text": "Raw Material", "stretch": True, "anchor": "w"},
            {"text": "Reference No.", "stretch": True},
            {"text": "Quantity(kg)", "stretch": True},
            {"text": "Warehouse (FROM)", "stretch": True},
            {"text": "Warehouse (TO)", "stretch": True},
            {"text": "Beginning Balance", "stretch": True},
            {"text": "Transfer Date", "stretch": True},
            {"text": "Entry Date", "stretch": True},
        ]
        self.rowdata = self.fetch_and_format_data()

        # Create Tableview
        self.table = Tableview(
            master=self.note_form_tab,
            coldata=self.coldata,
            rowdata=self.rowdata,
            paginated=True,
            searchable=True,
            bootstyle=PRIMARY,
            pagesize=20,
            autofit=True,  # Auto-size columns
            autoalign=False,  # Auto-align columns based on data
        )
        self.table.pack(fill=BOTH, expand=YES, padx=10, pady=10)

    def fetch_and_format_data(self):
        """Fetch data from API and format for table rowdata."""
        url = server_ip + "/api/transfer_forms/temp/list/"
        try:
            response = requests.get(url)
            response.raise_for_status()

            data = response.json()
            print(data)

            # Format data for the table
            rowdata = [
                (
                    item["raw_material"],
                    item["ref_number"],
                    item["qty_kg"],
                    item["from_warehouse"],
                    item["to_warehouse"],
                    item["transfer_date"],
                    datetime.fromisoformat(item["created_at"]).strftime("%m/%d/%Y %I:%M %p"),
                )
                for item in data
            ]
            return rowdata
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from API: {e}")
            return []


        # Return both buttons as a tuple
        return [update_button, delete_button]


    def refresh_table(self):
        """Refresh the table with updated data."""
        self.rowdata = self.fetch_and_format_data()
        self.table.build_table_data(
            coldata=self.coldata,
            rowdata=self.rowdata
        )
        self.table.goto_last_page()

