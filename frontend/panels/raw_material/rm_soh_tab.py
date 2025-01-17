
import ttkbootstrap as ttk
from ttkbootstrap.constants import *


def rm_soh_tab(notebook):
    stock_on_hand_tab = ttk.Frame(notebook)
    notebook.add(stock_on_hand_tab, text="Stock on Hand")
    stock_on_hand_label = ttk.Label(
        stock_on_hand_tab,
        text="Stock on Hand Content Here",
        font=("Helvetica", 14),
        bootstyle=INFO,
    )
    stock_on_hand_label.pack(pady=20, padx=20)