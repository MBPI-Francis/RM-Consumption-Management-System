
import ttkbootstrap as ttk
from ttkbootstrap.constants import *


def preparation_form_tab(notebook):
    preparation_form_tab = ttk.Frame(notebook)
    notebook.add(preparation_form_tab, text="Preparation Form")
    # Populate the Raw Materials Tab
    preparation_form_label = ttk.Label(
        preparation_form_tab,
        text="Preparation Form Content Here",
        font=("Helvetica", 14),
        bootstyle=INFO,
    )
    preparation_form_label.pack(pady=20, padx=20)