
import ttkbootstrap as ttk
from ttkbootstrap.constants import *


def submit_entries_tab(notebook):
    submit_entries_tab = ttk.Frame(notebook)
    notebook.add(submit_entries_tab, text="Submit Entries")
    # Populate the Raw Materials Tab
    submit_entries_label = ttk.Label(
        submit_entries_tab,
        text="Click the Button to Submit and Compute your Entries",
        font=("Helvetica", 14),
        bootstyle=INFO,
    )
    submit_entries_label.pack(pady=20, padx=20)