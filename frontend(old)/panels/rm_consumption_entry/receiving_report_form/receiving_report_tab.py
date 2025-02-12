
import ttkbootstrap as ttk
from ttkbootstrap.constants import *


def receiving_report_tab(notebook):
    receiving_report_tab = ttk.Frame(notebook)
    notebook.add(receiving_report_tab, text="Receiving Report Entry")
    # Populate the Raw Materials Tab
    receiving_report_label = ttk.Label(
        receiving_report_tab,
        text="Receiving Report Entry",
        font=("Helvetica", 14),
        bootstyle=INFO,
    )
    receiving_report_label.pack(pady=20, padx=20)