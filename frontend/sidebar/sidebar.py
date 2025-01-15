import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class Sidebar(ttk.Frame):
    def __init__(self, parent, navigate_callback):
        super().__init__(parent, width=200, padding=10, style="Sidebar.TFrame")

        # Custom Style for Sidebar
        style = ttk.Style()
        style.configure("Sidebar.TFrame", background="#8B4513")  # Brown color

        # Navigation Buttons
        ttk.Button(
            self,
            text="Warehouse",
            command=lambda: navigate_callback("warehouse"),
            bootstyle=PRIMARY,
            width=15,
        ).pack(pady=10)

        ttk.Button(
            self,
            text="Department",
            command=lambda: navigate_callback("department"),
            bootstyle=SUCCESS,
            width=15,
        ).pack(pady=10)

        ttk.Button(
            self,
            text="User",
            command=lambda: navigate_callback("user"),
            bootstyle=INFO,
            width=15,
        ).pack(pady=10)

        ttk.Button(
            self,
            text="Raw Material",
            command=lambda: navigate_callback("raw_material"),
            bootstyle=INFO,
            width=15,
        ).pack(pady=10)

        ttk.Button(
            self,
            text="Consumption Entry",
            command=lambda: navigate_callback("consumption_entry"),
            bootstyle=INFO,
            width=15,
        ).pack(pady=10)
