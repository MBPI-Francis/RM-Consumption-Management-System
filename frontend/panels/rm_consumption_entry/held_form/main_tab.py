
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from .entry_fields import entry_fields


def held_form_tab(notebook):
    held_form_tab = ttk.Frame(notebook)
    notebook.add(held_form_tab, text="Held Form")
    # Populate the Raw Materials Tab
    held_form_label = ttk.Label(
        held_form_tab,
        text="RM Change of Status",
        font=("Helvetica", 14),
        bootstyle=INFO,
    )
    held_form_label.pack(pady=20, padx=20)

    entry_fields(held_form_tab)



