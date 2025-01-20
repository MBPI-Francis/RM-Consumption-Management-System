
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from .table import NoteTable
from .entry_fields import entry_fields


# def notes_form_tab(notebook):
#     note_form_tab = ttk.Frame(notebook)
#     notebook.add(note_form_tab, text="Notes Form")
#     # Populate the Raw Materials Tab
#     note_form_label = ttk.Label(
#         note_form_tab,
#         text="Note Form Entry",
#         font=("Helvetica", 14),
#         bootstyle=INFO,
#     )
#     note_form_label.pack(pady=20, padx=20)
#
#     # Call the entry fields function to show the table
#     entry_fields(note_form_tab)

def receiving_report_tab(notebook):
    receiving_report_tab = ttk.Frame(notebook)
    notebook.add(receiving_report_tab, text="Receiving Report Entry")
    # Populate the Raw Materials Tab
    receiving_report_label = ttk.Label(
        receiving_report_tab,
        text="Receiving Report Entry",
        font=("Helvetica", 14),
        bootstyle=INFO,
    )
    receiving_report_label.pack(pady=20, padx=20)

    # Call the entry fields function to show the table
    entry_fields(receiving_report_tab)
