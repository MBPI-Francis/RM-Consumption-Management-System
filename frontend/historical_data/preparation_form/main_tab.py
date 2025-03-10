
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from .table import PreparationFormTable



def preparation_form_tab(notebook):
    preparation_form_tab = ttk.Frame(notebook)
    notebook.add(preparation_form_tab, text="Preparation Form")
    # Populate the Raw Materials Tab
    preparation_form_label = ttk.Label(
        preparation_form_tab,
        text="Preparation Form",
        font=("Helvetica", 14, "bold"),
        bootstyle=PRIMARY,
    )
    preparation_form_label.pack(pady=(10, 0), padx=20)
    table = PreparationFormTable(preparation_form_tab)



