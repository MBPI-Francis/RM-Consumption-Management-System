import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class StockOnHandView:
    def __init__(self, parent):
        self.parent = parent

    def show(self):
        """Display the Stock on Hand content."""
        label = ttk.Label(
            self.parent,
            text="Stock On Hand Content",
            font=("Helvetica", 18),
            bootstyle=SUCCESS,
        )
        label.pack(pady=20)
