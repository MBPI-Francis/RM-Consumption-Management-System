import psycopg2
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import requests
from ttkbootstrap.tooltip import ToolTip
from tkinter import Toplevel, messagebox, StringVar
from backend.settings.database import server_ip
from datetime import datetime
from uuid import UUID
from tkinter import simpledialog
from ttkbootstrap.widgets import DateEntry
from .validation import EntryValidation
from ttkbootstrap.dialogs import Messagebox
from ..preparation_form.validation import EntryValidation as PrepValidation


class NoteTable:
    def __init__(self, root):
        self.root = root

        # self.search_entry = ttk.Entry(self.root)
        # self.search_entry.pack(pady=5)
        # self.search_entry.bind("<Return>", self.search_data)

        # Frame for search
        search_frame = ttk.Frame(self.root)
        search_frame.pack(fill=X, padx=10, pady=5)
        ttk.Label(search_frame, text="Search:").pack(side=LEFT, padx=5)
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side=LEFT, fill=X, expand=YES)
        self.search_entry.bind("<Return>", self.search_data)

        # Define a style for the Treeview Header
        style = ttk.Style()
        style.configure("Custom.Treeview.Heading", font=("Arial", 10, "bold"), foreground="white",
                        background="#0078D4")  # Header color
        style.configure("Custom.Treeview", rowheight=25)  # Adjust row height for better visibility

        # Create Treeview with custom style
        self.tree = ttk.Treeview(self.root, columns=(
            "Raw Material", "Warehouse", "Reference No.", "Quantity(kg)",
            "Current Status", "New Status", "Change Status Date", "Entry Date"
        ), show="headings", style="Custom.Treeview")


        # Define column headings
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_column(c, False))
            self.tree.column(col, width=150, anchor="w")

        self.tree.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        self.tree.bind("<Button-3>", self.show_context_menu)  # Right-click menu

        self.refresh_table()

    def refresh_table(self):
        """Fetch data from API and populate Treeview."""
        url = server_ip + "/api/held_forms/temp/list/"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            self.tree.delete(*self.tree.get_children())  # Clear existing data
            for item in data:
                self.tree.insert("", "end", values=(
                    item["raw_material"],
                    item["wh_name"],
                    item["ref_number"],
                    item["qty_kg"],
                    item["current_status"],
                    item["new_status"],
                    item["change_status_date"],
                    datetime.fromisoformat(item["created_at"]).strftime("%m/%d/%Y %I:%M %p"),
                ), iid=item["id"])
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")

    def show_context_menu(self, event):
        """Show right-click menu with Edit/Delete options."""
        item = self.tree.identify_row(event.y)
        if item:
            menu = ttk.Menu(self.root, tearoff=0)
            menu.add_command(label="Edit", command=lambda: self.edit_record(item))
            # menu.add_command(label="Delete", command=lambda: self.confirm_delete(item))
            menu.add_command(label="Delete", command=lambda: self.delete_entry(item))
            menu.post(event.x_root, event.y_root)

    def edit_record(self, item):
        """Open edit form."""
        record = self.tree.item(item, 'values')

        print(record)
        if not record:
            return

        edit_window = Toplevel(self.root)
        edit_window.title("Edit Record")

        fields = ["Raw Material", "Warehouse", "Reference No.", "Quantity(kg)",
            "Current Status", "New Status", "Change Status Date",]
        entries = {}


        for idx, field in enumerate(fields):
            ttk.Label(edit_window, text=field).grid(row=idx, column=0, padx=10, pady=5, sticky=W)

            if field == "Raw Material":
                # Fetch Raw Material Data from API
                rm_codes = self.get_rm_code_api()
                code_to_id = {item["rm_code"]: item["id"] for item in rm_codes}
                rm_names = list(code_to_id.keys())

                entry = ttk.Combobox(edit_window, values=rm_names, state="normal", width=30)
                entry.set(record[idx])  # Set current value in the combobox
                ToolTip(entry, text="Choose a raw material")  # Tooltip


            elif field == "Warehouse":
                # Warehouse JSON-format choices (coming from the API)
                warehouses = self.get_warehouse_api()
                warehouse_to_id = {item["wh_name"]: item["id"] for item in warehouses}
                warehouse_names = list(warehouse_to_id.keys())

                entry = ttk.Combobox(edit_window, values=warehouse_names, state="readonly", width=30)
                entry.set(record[idx])  # Set current value in the combobox
                ToolTip(entry, text="Select a warehouse")  # Tooltip

            elif field == "Change Status Date":
                entry = DateEntry(edit_window, dateformat="%m/%d/%Y", width=30)
                entry.entry.delete(0, "end")
                formatted_date = datetime.strptime(record[idx], "%Y-%m-%d").strftime("%m/%d/%Y")
                entry.entry.insert(0, formatted_date)

            elif field == "Current Status":
                # Warehouse JSON-format choices (coming from the API)
                status = self.get_status_api()
                status_to_id = {item["name"]: item["id"] for item in status}
                status_names = list(status_to_id.keys())

                entry = ttk.Combobox(edit_window, values=status_names, state="readonly", width=30,)
                entry.set(record[idx])  # Set current value in the combobox
                ToolTip(entry, text="Choose the current status")  # Tooltip


            elif field == "New Status":
                # Warehouse JSON-format choices (coming from the API)
                status = self.get_status_api()
                status_to_id = {item["name"]: item["id"] for item in status}
                status_names = list(status_to_id.keys())

                entry = ttk.Combobox(edit_window, values=status_names, state="readonly", width=30,)
                entry.set(record[idx])  # Set current value in the combobox
                ToolTip(entry, text="Choose the new status")  # Tooltip

            elif field == "Quantity(kg)":

                validate_numeric_command = edit_window.register(EntryValidation.validate_numeric_input)
                entry = ttk.Entry(edit_window,
                                      width=30,
                                      validate="key",  # Trigger validation on keystrokes
                                      validatecommand=(validate_numeric_command, "%P")
                                      # Pass the current widget content ("%P")
                                      )
                entry.insert(0, record[idx])
                ToolTip(entry, text="Enter the Quantity(kg)")


            else:
                entry = ttk.Entry(edit_window, width=30)
                entry.insert(0, record[idx])


            entries[field] = entry
            entry.grid(row=idx, column=1, padx=10, pady=5, sticky=W)


        def get_selected_rm_code_id():
            selected_name = entries["Raw Material"].get()
            selected_id = code_to_id.get(selected_name)
            return selected_id if selected_id else None


        def get_selected_warehouse_id():
            selected_name = entries["Warehouse"].get()
            selected_id = warehouse_to_id.get(selected_name)  # Get the corresponding ID
            if selected_id:
                return selected_id
            else:
                return None

        def get_selected_current_status_id():
            selected_name = entries["Current Status"].get()
            selected_id = status_to_id.get(selected_name)  # Get the corresponding ID
            if selected_id:
                return selected_id
            else:
                return None

        def get_selected_new_status_id():
            selected_name = entries["New Status"].get()
            selected_id = status_to_id.get(selected_name)  # Get the corresponding ID
            if selected_id:
                return selected_id
            else:
                return None

        def update_record():
            # Convert date to YYYY-MM-DD
            try:
                change_status_date = datetime.strptime(entries["Change Status Date"].entry.get(), "%m/%d/%Y").strftime("%Y-%m-%d")
            except ValueError:
                Messagebox.show_error("Error", "Invalid date format. Please use MM/DD/YYYY.")
                return
            data = {
                "rm_code_id": get_selected_rm_code_id(),
                "warehouse_id": get_selected_warehouse_id(),
                "current_status_id": get_selected_current_status_id(),
                "new_status_id": get_selected_new_status_id(),
                "ref_number": entries["Reference No."].get(),
                "change_status_date":  change_status_date,
                "qty_kg": entries["Quantity(kg)"].get(),
            }

            # Validate the data entries in front-end side
            if EntryValidation.entry_validation(data):
                error_text = EntryValidation.entry_validation(data)
                Messagebox.show_error(f"There is no data in these fields {error_text}.", "Data Entry Error", alert=True)
                return

            # Validate if the entry value exceeds the stock
            validatation_result = PrepValidation.validate_soh_value(
                get_selected_rm_code_id(),
                get_selected_warehouse_id(),
                entries["Quantity(kg)"].get(),
                get_selected_current_status_id()

            )

            if validatation_result:

                try:
                    url = server_ip + f"/api/held_forms/temp/update/{item}/"
                    response = requests.put(url, json=data)
                    if response.status_code == 200:
                        messagebox.showinfo("Success", "Record updated successfully")
                        self.refresh_table()
                        edit_window.destroy()

                    else:
                        messagebox.showerror("Error", f"Failed to update record - {response.status_code}")
                except requests.exceptions.RequestException as e:
                    messagebox.showerror("Error", f"Failed to update: {e}")

            else:
                Messagebox.show_error(
                    "The entered quantity in 'Quantity' exceeds the available stock in the database.",
                    "Data Entry Error")
                return

        ttk.Button(edit_window, text="Save", command=update_record, width=30).grid(row=len(fields), column=0, columnspan=2,
                                                                         pady=10)

    def delete_entry(self, entry_id):
        """Delete selected entry via API."""
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this entry?"):
            url = server_ip + f"/api/held_forms/temp/delete/{entry_id}/"
            response = requests.delete(url)
            if response.status_code == 200:
                self.tree.delete(entry_id)
                messagebox.showinfo("Success", "Entry deleted successfully.")
            else:
                messagebox.showerror("Error", "Failed to delete entry.")

    def search_data(self, event=None):
        """Search for data when Enter is pressed."""
        search_term = self.search_entry.get().strip().lower()
        for item in self.tree.get_children():
            values = [str(val).lower() for val in self.tree.item(item)["values"]]
            if any(search_term in val for val in values):
                self.tree.selection_set(item)
                self.tree.focus(item)
                self.tree.see(item)
                return
        messagebox.showinfo("Search", "No matching record found.")

    def sort_column(self, col, reverse):
        """Sort Treeview column in ascending/descending order."""
        data = [(self.tree.set(k, col), k) for k in self.tree.get_children("")]
        data.sort(reverse=reverse)
        for index, (_, k) in enumerate(data):
            self.tree.move(k, "", index)
        self.tree.heading(col, command=lambda: self.sort_column(col, not reverse))



    def get_rm_code_api(self):
        url = server_ip + "/api/raw_materials/list/"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            print("Data fetched successfully!")
            return data
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            return []

    def get_warehouse_api(self):
        url = server_ip + "/api/warehouses/list/"
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse JSON response
            data = response.json()
            print("Data fetched successfully!")
            return data
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")

    def get_status_api(self):
        url = server_ip + "/api/droplist/list/"
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse JSON response
            data = response.json()
            print("Data fetched successfully!")
            return data
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")