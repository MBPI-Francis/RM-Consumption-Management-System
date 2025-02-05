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
from ttkbootstrap.dialogs import Messagebox
from ..preparation_form.validation import EntryValidation as PrepValidation
from .validation import EntryValidation as TranferValidation


class NoteTable:
    def __init__(self, root):
        self.root = root

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


        self.tree = ttk.Treeview(self.root, columns=(
            "Raw Material", "Reference No.", "Quantity(kg)",
            "Warehouse (FROM)", "Warehouse (TO)", "Status",
            "Transfer Date", "Entry Date"
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
        url = server_ip + "/api/transfer_forms/temp/list/"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            self.tree.delete(*self.tree.get_children())  # Clear existing data
            for item in data:
                self.tree.insert("", "end", values=(
                    item["raw_material"],
                    item["ref_number"],
                    item["qty_kg"],
                    item["from_warehouse"],
                    item["to_warehouse"],
                    item["status"],
                    item["transfer_date"],
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
        if not record:
            return

        edit_window = Toplevel(self.root)
        edit_window.title("Edit Record")

        fields = ["Raw Material", "Reference No.", "Quantity(kg)",
            "Warehouse (FROM)", "Warehouse (TO)", "Status",
            "Transfer Date"]
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


            elif field == "Warehouse (FROM)":
                # Warehouse JSON-format choices (coming from the API)
                warehouses = self.get_warehouse_api()
                warehouse_to_id = {item["wh_name"]: item["id"] for item in warehouses}
                warehouse_names = list(warehouse_to_id.keys())

                entry = ttk.Combobox(edit_window, values=warehouse_names, state="readonly", width=30)
                entry.set(record[idx])  # Set current value in the combobox
                ToolTip(entry, text="Select a warehouse")  # Tooltip


            elif field == "Warehouse (TO)":
                # Warehouse JSON-format choices (coming from the API)
                warehouses = self.get_warehouse_api()
                warehouse_to_id = {item["wh_name"]: item["id"] for item in warehouses}
                warehouse_names = list(warehouse_to_id.keys())

                entry = ttk.Combobox(edit_window, values=warehouse_names, state="readonly", width=30)
                entry.set(record[idx])  # Set current value in the combobox
                ToolTip(entry, text="Select a warehouse")  # Tooltip


            elif field == "Status":
                # Warehouse JSON-format choices (coming from the API)
                status = self.get_status_api()
                status_to_id = {item["name"]: item["id"] for item in status}
                status_names = list(status_to_id.keys())

                entry = ttk.Combobox(edit_window, values=status_names, state="readonly", width=30,)
                entry.set(record[idx])  # Set current value in the combobox
                ToolTip(entry, text="Choose the current status")  # Tooltip


            elif field == "Transfer Date":
                entry = DateEntry(edit_window, dateformat="%m/%d/%Y", width=30)
                entry.entry.delete(0, "end")
                formatted_date = datetime.strptime(record[idx], "%Y-%m-%d").strftime("%m/%d/%Y")
                entry.entry.insert(0, formatted_date)


            elif field == "Quantity(kg)":

                validate_numeric_command = edit_window.register(TranferValidation.validate_numeric_input)
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

        def get_selected_warehouse_from_id():
            selected_name = entries["Warehouse (FROM)"].get()
            selected_id = warehouse_to_id.get(selected_name)  # Get the corresponding ID
            if selected_id:
                return selected_id
            else:
                return None

        def get_selected_warehouse_to_id():
            selected_name = entries["Warehouse (TO)"].get()
            selected_id = warehouse_to_id.get(selected_name)  # Get the corresponding ID
            if selected_id:
                return selected_id
            else:
                return None

        def get_selected_status_id():
            selected_name = entries["Status"].get()
            selected_id = status_to_id.get(selected_name)  # Get the corresponding ID
            if selected_id:
                return selected_id
            else:
                return None

        def update_record():
            # Convert date to YYYY-MM-DD
            try:
                transfer_date = datetime.strptime(entries["Transfer Date"].entry.get(), "%m/%d/%Y").strftime("%Y-%m-%d")
            except ValueError:
                Messagebox.show_error("Error", "Invalid date format. Please use MM/DD/YYYY.")
                return

            # Create a dictionary with the data
            data = {
                "rm_code_id": get_selected_rm_code_id(),
                "from_warehouse_id": get_selected_warehouse_from_id(),
                "to_warehouse_id": get_selected_warehouse_to_id(),
                "ref_number": entries["Reference No."].get(),
                "status_id": get_selected_status_id(),
                "transfer_date": transfer_date,
                "qty_kg": entries["Quantity(kg)"].get(),
            }

            # Validate the data entries in front-end side
            if TranferValidation.entry_validation(data):
                error_text = TranferValidation.entry_validation(data)
                Messagebox.show_error(f"There is no data in these fields {error_text}.", "Data Entry Error", alert=True)
                return

                # Check if the record is existing in the inventory
                # Call the check_raw_material function
            result = self.check_raw_material(get_selected_rm_code_id(),
                                             get_selected_warehouse_from_id(),
                                             get_selected_status_id())
            # Display the result in the GUI
            if result:

                # Validate if the entry value exceeds the stock
                validatation_result = PrepValidation.validate_soh_value(
                    get_selected_rm_code_id(),
                    get_selected_warehouse_from_id(),
                    entries["Quantity(kg)"].get(),
                    get_selected_status_id()

                )

                if validatation_result:

                    try:
                        url = server_ip + f"/api/transfer_forms/temp/update/{item}/"
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




        save_button = ttk.Button(edit_window,
                                 text="Save",
                                 command=update_record,
                                 width=20)
        save_button.grid(row=len(fields), column=0, columnspan=2,pady=10)

    def delete_entry(self, entry_id):
        """Delete selected entry via API."""
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this entry?"):
            url = server_ip + f"/api/transfer_forms/temp/delete/{entry_id}/"
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

    def check_raw_material(self, rm_id: UUID, warehouse_id: UUID, status_id: UUID = None):
        url = f"{server_ip}/api/check/raw_material/"  # Replace with the actual URL of your FastAPI server

        # Construct the query parameters
        params = {
            "rm_id": str(rm_id),  # Convert UUID to string for query parameter
            "warehouse_id": str(warehouse_id),
        }

        # Include status_id only if it's not None
        if status_id:
            params["status_id"] = status_id
        # Handle response

        try:
            # Send the GET request
            response = requests.get(url, params=params)

            # Check if the response was successful
            if response.status_code == 200:
                # Parse the response data (True or False)
                return response.json()  # This will return either True or False
            else:
                # Handle errors
                print(f"Error: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return False