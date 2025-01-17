import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from .held_form.held_form_tab import held_form_tab
from .notes_form.notes_form_tab import notes_form_tab
from .transfer_form.transfer_form_tab import transfer_form_tab
from .preparation_form.preparation_form_tab import preparation_form_tab
from .outgoing_report_form.outgoing_form_tab import outgoing_form_tab
from .receiving_report_form.receiving_report_tab import receiving_report_tab

class ConsumptionEntryView:
    def __init__(self, parent):
        self.parent = parent

    def show(self):
        """Display the Raw Material content."""
        # Create the Notebook widget
        notebook = ttk.Notebook(self.parent)
        notebook.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Create the frames for each tab
        notes_form_tab(notebook)
        outgoing_form_tab(notebook)
        preparation_form_tab(notebook)
        receiving_report_tab(notebook)
        # transfer_form_tab(notebook)
        held_form_tab(notebook)
