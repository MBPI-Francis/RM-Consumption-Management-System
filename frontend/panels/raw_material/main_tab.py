
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from .entry_fields import entry_fields



def rm_code_tab(notebook):
    raw_material_tab = ttk.Frame(notebook)
    notebook.add(raw_material_tab, text="Raw Materials")
    # Populate the Raw Materials Tab
    raw_material_label = ttk.Label(
        raw_material_tab,
        text="Raw Materials Content Here",
        font=("Helvetica", 14),
        bootstyle=INFO,
    )
    raw_material_label.pack(pady=20, padx=20)
    entry_fields(raw_material_tab)

