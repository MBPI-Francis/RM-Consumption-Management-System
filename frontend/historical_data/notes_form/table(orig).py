
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
            {"text": "Product Code", "stretch": True, "anchor": "w"},
            {"text": "Lot No.", "stretch": True},
            {"text": "Product Kind", "stretch": True},
            {"text": "Consumption Date", "stretch": True},
            {"text": "Entry Date", "stretch": True},
            {"text": "Actions", "stretch": True},
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
        url = server_ip + "/api/notes/temp/list/"
        try:
            response = requests.get(url)
            response.raise_for_status()

            data = response.json()
            print(data)

            # Format data for the table
            rowdata = [
                (
                    item["product_code"],
                    item["lot_number"],
                    item["product_kind_id"],
                    datetime.fromisoformat(item["stock_change_date"]).strftime("%m/%d/%Y"),
                    datetime.fromisoformat(item["created_at"]).strftime("%m/%d/%Y %I:%M %p"),
                    # self.create_action_buttons(item["id"])  # Add buttons
                )
                for item in data
            ]
            return rowdata
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from API: {e}")
            return []

    # def create_action_buttons(self, note_id):
    #     """Create Update and Delete buttons for a row."""
    #     # Update button
    #     update_button = ttk.Button(
    #         text="Update",
    #         bootstyle="info",
    #         command=lambda: self.update_record(note_id),
    #     )
    #
    #     # Delete button
    #     delete_button = ttk.Button(
    #         text="Delete",
    #         bootstyle="danger",
    #         command=lambda: self.delete_record(note_id),
    #     )
    #
    #     # Return both buttons as a tuple
    #     return [update_button, delete_button]

    def update_record(self, note_id):
        """Update the selected record."""
        print(f"Update clicked for note ID: {note_id}")
        # Implement the logic to handle the update

    def delete_record(self, note_id):
        """Delete the selected record."""
        print(f"Delete clicked for note ID: {note_id}")
        # Implement the logic to handle deletion

    def refresh_table(self):
        """Refresh the table with updated data."""
        self.rowdata = self.fetch_and_format_data()
        self.table.build_table_data(
            coldata=self.coldata,
            rowdata=self.rowdata
        )
        self.table.goto_last_page()


def get_notes_data_api():
    """API request for fetching note data."""
    url = server_ip + "/api/notes/temp/list/"

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return []  # Return an empty list if there's an error

