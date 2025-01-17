
import ttkbootstrap as ttk
from ttkbootstrap.constants import *


def outgoing_form_tab(notebook):
    outgoing_form_tab = ttk.Frame(notebook)
    notebook.add(outgoing_form_tab, text="Outgoing Form")
    # Populate the Raw Materials Tab
    outgoing_form_label = ttk.Label(
        outgoing_form_tab,
        text="Outgoing Form Content Here",
        font=("Helvetica", 14),
        bootstyle=INFO,
    )
    outgoing_form_label.pack(pady=20, padx=20)