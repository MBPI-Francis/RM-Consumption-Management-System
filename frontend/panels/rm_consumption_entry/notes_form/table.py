import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *


def table(note_form_tab):
    # Define column and row data
    coldata = [
        {"text": "Product Code", "stretch": True},
        {"text": "Lot No.", "stretch": True},
        {"text": "Product Kind", "stretch": True},
        {"text": "Consumption Date", "stretch": True},
        {"text": "Entry Date", "stretch": True},
    ]
    rowdata = [
        ('A123', 'IzzyCo', 'asd'),
        ('A136', 'Kimdee Inc.','asd'),
        ('A158', 'Farmadding Co.', 'asd'),
    ]

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


