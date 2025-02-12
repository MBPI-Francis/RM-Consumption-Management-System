
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from .entry_fields import entry_fields
from ttkbootstrap.tableview import Tableview
import requests
from backend.settings.database import server_ip
from datetime import datetime



def rm_code_tab(notebook):
    raw_material_tab = ttk.Frame(notebook)
    notebook.add(raw_material_tab, text="Raw Materials")
    # Populate the Raw Materials Tab
    raw_material_label = ttk.Label(
        raw_material_tab,
        text="Raw Materials",
        font=("Helvetica", 14),
        bootstyle=PRIMARY,
    )
    raw_material_label.pack(pady=20, padx=20)
    entry_fields(raw_material_tab)



def rm_soh_tab(notebook):
    soh_tab = ttk.Frame(notebook)
    notebook.add(soh_tab, text="Latest Raw Material Stocks")
    # Populate the Raw Materials Tab
    raw_material_label = ttk.Label(
        soh_tab,
        text="Overall Latest Raw Material Stocks",
        font=("Helvetica", 14),
        bootstyle=PRIMARY,
    )
    raw_material_label.pack(pady=20, padx=20)


    class NoteTable:

        def __init__(self, root):
            self.note_form_tab = root

            self.coldata = [
                {"text": "Raw Material Code", "stretch": True, "anchor": "w"},
                {"text": "Warehouse", "stretch": True},
                {"text": "Beginning Balance", "stretch": True},
                {"text": "Status", "stretch": True},
                {"text": "Last Movement", "stretch": True},
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
            url = server_ip + "/api/get/beginning_balance/"
            try:
                response = requests.get(url)
                response.raise_for_status()

                data = response.json()
                print(data)

                # Format data for the table
                rowdata = [
                    (
                        item["rmcode"],
                        item["warehousename"],
                        item["beginningbalance"],
                        item["statusname"],
                        datetime.fromisoformat(item["stockchangedate"]).strftime("%m/%d/%Y %I:%M %p")
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

        # Calling the table
    note_table = NoteTable(soh_tab)



