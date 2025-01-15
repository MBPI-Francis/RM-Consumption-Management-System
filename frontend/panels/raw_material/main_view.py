import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from .rm_code_tab import rm_code_tab
from .rm_soh_tab import rm_soh_tab



class RawMaterialView:
    def __init__(self, parent):
        self.parent = parent

    def show(self):
        """Display the Raw Material content."""

        # Create the Notebook widget
        notebook = ttk.Notebook(self.parent)
        notebook.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Create the frames for each tab
        rm_code_tab(notebook)
        rm_soh_tab(notebook)


        # Add the tabs to the notebook





        # Populate the Stock on Hand Tab

