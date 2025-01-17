
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from .table import table
from .entry_fields import entry_fields


def notes_form_tab(notebook):
    note_form_tab = ttk.Frame(notebook)
    notebook.add(note_form_tab, text="Notes Form")
    # Populate the Raw Materials Tab
    note_form_label = ttk.Label(
        note_form_tab,
        text="Notes Form Content Here",
        font=("Helvetica", 14),
        bootstyle=INFO,
    )
    note_form_label.pack(pady=20, padx=20)




    # Call the entry fields function to show the table
    entry_fields(note_form_tab)


    # Call the table function to show the table
    table(note_form_tab)