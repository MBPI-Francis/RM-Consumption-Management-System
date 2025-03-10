
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from .table import ChangeStatusFormTable


def held_form_tab(notebook):
    held_form_tab = ttk.Frame(notebook)
    notebook.add(held_form_tab, text="Change Status Form")
    # Populate the Raw Materials Tab
    held_form_label = ttk.Label(
        held_form_tab,
        text="Change Status Form",
        font=("Helvetica", 14, "bold"),
        bootstyle=PRIMARY,
    )
    held_form_label.pack(pady=20, padx=20)

    table = ChangeStatusFormTable(held_form_tab)



