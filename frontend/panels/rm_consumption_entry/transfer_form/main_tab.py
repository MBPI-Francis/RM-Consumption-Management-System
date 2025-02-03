
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from .entry_fields import entry_fields


def transfer_form_tab(notebook):
    transfer_form_tab = ttk.Frame(notebook)
    notebook.add(transfer_form_tab, text="Transfer Report Form")
    # Populate the Raw Materials Tab
    transfer_form_label = ttk.Label(
        transfer_form_tab,
        text="Transfer Report Form Entry",
        font=("Helvetica", 14),
        bootstyle=INFO,
    )
    transfer_form_label.pack(pady=20, padx=20)

    entry_fields(transfer_form_tab)


