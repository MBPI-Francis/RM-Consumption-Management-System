import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from sidebar.sidebar import Sidebar
from panels.warehouse.warehouse_view import WarehouseView
from panels.department.department_view import DepartmentView
from panels.user.user_view import UserView
from panels.raw_material.main_view import RawMaterialView
from panels.rm_consumption_entry.main_view import ConsumptionEntryView

class App(ttk.Window):
    def __init__(self):
        super().__init__(themename="cosmo")  # Choose the ttkbootstrap theme
        self.title("Warehouse RM Stock Movement Program")
        self.geometry("1300x700")

        # Configure row/column for responsiveness of the main window
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=0)  # Sidebar should not stretch
        self.columnconfigure(1, weight=0)  # Separator should not stretch
        self.columnconfigure(2, weight=1)  # Content area should stretch

        # Sidebar
        self.sidebar = Sidebar(self, self.navigate_to_view)
        self.sidebar.grid(row=0, column=0, sticky=N + S)

        # Vertical Separator
        self.separator = ttk.Separator(self, orient=VERTICAL)
        self.separator.grid(row=0, column=1, sticky=N + S)

        # Main Content Frame (with padding)
        self.content_frame = ttk.Frame(self, padding=10)
        self.content_frame.grid(row=0, column=2, sticky=N + S + E + W)

        # Configure grid for the content frame to make it responsive
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        # Initialize Views
        self.views = {
            "warehouse": WarehouseView(self.content_frame),
            "department": DepartmentView(self.content_frame),
            "user": UserView(self.content_frame),
            "raw_material": RawMaterialView(self.content_frame),
            "consumption_entry": ConsumptionEntryView(self.content_frame)
        }

        # Default View
        self.navigate_to_view("warehouse")

    def navigate_to_view(self, view_name):
        """Navigate to the selected view."""
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Show the selected view
        if view_name in self.views:
            self.views[view_name].show()

if __name__ == "__main__":
    app = App()
    app.mainloop()

