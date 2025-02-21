
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from frontend.stock_on_hand.table import BeginningBalanceTable
from frontend.stock_on_hand.import_feature.confirm_messages import ConfirmationMessage
def beginning_balance_tab(notebook):
    soh_tab = ttk.Frame(notebook)
    notebook.add(soh_tab, text="Beginning Balance")
    # Populate the Raw Materials Tab
    raw_material_label = ttk.Label(
        soh_tab,
        text="Beginning Balance",
        font=("Helvetica", 14, "bold"),
        bootstyle=PRIMARY,
    )
    raw_material_label.pack(pady=20, padx=20)

    # Button to trigger the import process
    import_button = ttk.Button(
        soh_tab,
        text="Generate New Beginning Balance",
        bootstyle=WARNING,
        command= lambda: ConfirmationMessage(soh_tab).show_confirmation_message()
    )

    import_button.pack(pady=20, padx=(12,0), anchor="w")  # Use pack() instead of grid()


    # Call out the table to show in the panel
    table = BeginningBalanceTable(soh_tab)





