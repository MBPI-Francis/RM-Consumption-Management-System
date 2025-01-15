import ttkbootstrap as ttk
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.constants import *


class WarehouseView:
    def __init__(self, parent):
        self.parent = parent

    def show(self):
        """Display the Warehouse content."""
        label = ttk.Label(
            self.parent,
            text="Warehouse Content",
            font=("Helvetica", 18),
            bootstyle=PRIMARY,
        )
        label.pack(pady=20)

        # Example ScrolledFrame content for Warehouse
        scroll_frame = ScrolledFrame(self.parent)
        scroll_frame.pack(fill=BOTH, expand=YES, pady=10)

        for i in range(20):  # Add example items
            ttk.Label(
                scroll_frame,
                text=f"Warehouse Item {i + 1}",
                bootstyle=SECONDARY,
            ).pack(pady=5)
