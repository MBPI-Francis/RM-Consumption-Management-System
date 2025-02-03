
import ttkbootstrap as ttk
from ttkbootstrap.constants import *


def held_form_tab(notebook):
    held_form_tab = ttk.Frame(notebook)
    notebook.add(held_form_tab, text="Held Form")
    # Populate the Raw Materials Tab
    held_form_label = ttk.Label(
        held_form_tab,
        text="Held Form Content Here",
        font=("Helvetica", 14),
        bootstyle=INFO,
    )
    held_form_label.pack(pady=20, padx=20)