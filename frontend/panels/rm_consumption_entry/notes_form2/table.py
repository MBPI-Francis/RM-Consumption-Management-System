import ttkbootstrap as ttk
from ttkbootstrap.tableview import *
from ttkbootstrap.constants import *
import requests
from api_requests import ApiRequest
from backend.settings.database import server_ip
from datetime import datetime

def table(note_form_tab):
    # Define column and row data
    coldata = [
        {"text": "Product Code", "stretch": True, "anchor": "w"},
        {"text": "Lot No.", "stretch": True},
        {"text": "Product Kind", "stretch": True},
        {"text": "Consumption Date", "stretch": True},
        {"text": "Entry Date", "stretch": True},
    ]

    rowdata = ApiRequest.get_notes_data_api()

    # Create Tableview
    dt = Tableview(
        master=note_form_tab,
        coldata=coldata,
        rowdata=rowdata,
        paginated=True,
        searchable=True,
        bootstyle=PRIMARY,
        pagesize=20,
        autofit=True,  # Auto-size columns
        autoalign=False,  # Auto-align columns based on data


    )
    return dt



