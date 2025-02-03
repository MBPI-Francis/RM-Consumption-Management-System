import ttkbootstrap as ttk
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.constants import *


class WarehouseView:
    def __init__(self, parent):
        self.parent = parent

    def show(self):
        """Display the Warehouse content."""
        # Use grid layout for the frame inside the content area
        warehouse_frame = ttk.Frame(self.parent)
        warehouse_frame.grid(row=0, column=0, sticky=N + S + E + W)

        # Add widgets inside the warehouse_frame
        label = ttk.Label(warehouse_frame, text="Warehouse Content")
        label.grid(row=0, column=0, sticky="nsew")

        # Ensure the content frame can expand
        warehouse_frame.grid_rowconfigure(0, weight=1)
        warehouse_frame.grid_columnconfigure(0, weight=1)
