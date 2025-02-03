import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# Create main window
root = ttk.Window(themename="flatly")

# Create a Combobox with sample values
combobox = ttk.Combobox(root, values=["Apple", "Banana", "Cherry", "Date", "Grape"])

# Enable autocompletion by setting the state to 'normal' and let ttk handle it
combobox.set('')  # Optional: Initialize with an empty string
combobox.pack(padx=20, pady=20)

root.mainloop()
