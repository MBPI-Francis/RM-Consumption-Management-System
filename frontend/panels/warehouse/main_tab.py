
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from .entry_fields import entry_fields


def warehouse_tab(notebook):
    warehouse_tab = ttk.Frame(notebook)
    notebook.add(warehouse_tab, text="Warehouses")
    # Populate the Raw Materials Tab
    raw_material_label = ttk.Label(
        warehouse_tab,
        text="Warehouse Numbers",
        font=("Helvetica", 14),
        bootstyle=PRIMARY,
    )
    raw_material_label.pack(pady=20, padx=20)
    entry_fields(warehouse_tab)

