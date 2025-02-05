import psycopg2
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import requests
from backend.settings.database import server_ip
from tkinter import Toplevel, messagebox, StringVar
from ttkbootstrap.dialogs import Querybox, Messagebox
from ttkbootstrap.widgets import DateEntry
from uuid import UUID
from datetime import datetime
from ttkbootstrap.tooltip import ToolTip
from .validation import EntryValidation


class NoteTable:
    def __init__(self, root):
        self.root = root

        # Frame for search
        search_frame = ttk.Frame(self.root)
        search_frame.pack(fill=X, padx=10, pady=5)
        ttk.Label(search_frame, text="Search:").pack(side=LEFT, padx=5)
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side=LEFT, fill=X, expand=YES)
        self.search_entry.bind("<Return>", self.search_data)

        self.tree = ttk.Treeview(root,
                                 columns=("Raw Material", "Warehouse", "Reference No.",
                                          "Quantity (Prepared)", "Quantity (Return)",
                                          "Preparation Date",
                                          "Entry Date"),
                                 show='headings')

        # Define columns
        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        self.tree.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        self.tree.bind("<Button-3>", self.show_context_menu)
        self.refresh_table()

        # Define column headers
        col_names = [   "Raw Material",
                        "Warehouse",
                        "Reference No.",
                        "Quantity (Prepared)",
                        "Quantity (Return)",
                        "Preparation Date",
                        "Entry Date"]
        for col in col_names:
            self.tree.heading(col, text=col, command=lambda _col=col: self.sort_treeview(_col, False))
            self.tree.column(col, anchor=W)

    def fetch_data(self):
        """Fetch data from API."""
        url = server_ip + "/api/preparation_forms/temp/list/"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return []

    def refresh_table(self):
        """Refresh Treeview with data."""
        self.tree.delete(*self.tree.get_children())
        for item in self.fetch_data():
            self.tree.insert("", END, values=(
                item["raw_material"],
                item["wh_name"],
                item["ref_number"],
                item["qty_prepared"],
                item["qty_return"],
                item["preparation_date"],
                datetime.fromisoformat(item["created_at"]).strftime("%m/%d/%Y %I:%M %p"),
            ), iid=item["id"])

    def sort_treeview(self, col, reverse):
        """Sort treeview column data."""
        items = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]
        items.sort(reverse=reverse)
        for index, (val, k) in enumerate(items):
            self.tree.move(k, "", index)
        self.tree.heading(col, command=lambda: self.sort_treeview(col, not reverse))


    def show_context_menu(self, event):
        """Show right-click menu."""
        item = self.tree.identify_row(event.y)
        if item:
            menu = ttk.Menu(self.root, tearoff=0)
            menu.add_command(label="Edit", command=lambda: self.edit_record(item))
            menu.add_command(label="Delete", command=lambda: self.confirm_delete(item))
            menu.post(event.x_root, event.y_root)

    def edit_record(self, item):
        """Open edit form."""
        record = self.tree.item(item, 'values')
        if not record:
            return

        edit_window = Toplevel(self.root)
        edit_window.title("Edit Record")

        fields = [ "Raw Material",
                    "Warehouse",
                    "Reference No.",
                    "Quantity (Prepared)",
                    "Quantity (Return)",
                    "Preparation Date"]
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

            elif field == "Preparation Date":
                entry = DateEntry(edit_window, dateformat="%m/%d/%Y", width=30)
                entry.entry.delete(0, "end")
                formatted_date = datetime.strptime(record[idx], "%Y-%m-%d").strftime("%m/%d/%Y")
                entry.entry.insert(0, formatted_date)


            elif field == "Quantity (Prepared)":
                validate_numeric_command = edit_window.register(EntryValidation.validate_numeric_input)
                entry = ttk.Entry(edit_window,
                                      width=30,
                                      validate="key",  # Trigger validation on keystrokes
                                      validatecommand=(validate_numeric_command, "%P")
                                      # Pass the current widget content ("%P")
                                      )
                entry.insert(0, record[idx])
                ToolTip(entry, text="Enter the Quantity (Prepared)")


            elif field == "Quantity (Return)":

                validate_numeric_command = edit_window.register(EntryValidation.validate_numeric_input)
                entry = ttk.Entry(edit_window,
                                      width=30,
                                      validate="key",  # Trigger validation on keystrokes
                                      validatecommand=(validate_numeric_command, "%P")
                                      # Pass the current widget content ("%P")
                                      )
                entry.insert(0, record[idx])
                ToolTip(entry, text="Enter the Quantity (Return)")


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

        def update_record():
            qty_return = entries["Quantity (Return)"].get()
            status_id = self.get_status_id()

            if qty_return == None or qty_return == '':
                qty_return = float(0.00)

            # Convert date to YYYY-MM-DD
            try:
                preparation_date = datetime.strptime(entries["Preparation Date"].entry.get(), "%m/%d/%Y").strftime("%Y-%m-%d")
            except ValueError:
                Messagebox.show_error("Error", "Invalid date format. Please use MM/DD/YYYY.")
                return
            data = {
                "rm_code_id": get_selected_rm_code_id(),
                "warehouse_id": get_selected_warehouse_id(),
                "ref_number": entries["Reference No."].get(),
                "preparation_date":  preparation_date,
                "qty_prepared": entries["Quantity (Prepared)"].get(),
                "qty_return": qty_return,
            }

            # Validate the data entries in front-end side
            if EntryValidation.entry_validation(data):
                error_text = EntryValidation.entry_validation(data)
                Messagebox.show_error(f"There is no data in these fields {error_text}.", "Data Entry Error", alert=True)
                return

            validatation_result = EntryValidation.validate_soh_value(
                get_selected_rm_code_id(),
                get_selected_warehouse_id(),
                entries["Quantity (Prepared)"].get(),
                status_id
            )

            if validatation_result:
                try:
                    url = server_ip + f"/api/preparation_forms/temp/update/{item}/"
                    response = requests.put(url, json=data)
                    if response.status_code == 200:
                        messagebox.showinfo("Success", "Record updated successfully")
                        self.refresh_table()
                        edit_window.destroy()
                    else:
                        messagebox.showerror("Error", "Failed to update record - ",response.status_code)
                except requests.exceptions.RequestException as e:
                    messagebox.showerror("Error", f"Failed to update: {e}")

            else:
                Messagebox.show_error(
                    "The entered quantity in 'Quantity (Prepared)' exceeds the available stock in the database.",
                    "Data Entry Error")
                return

        ttk.Button(edit_window, text="Save", command=update_record, width=30).grid(row=len(fields), column=0, columnspan=2,
                                                                         pady=10)
    def confirm_delete(self, item_id):
        """Show confirmation before deleting record."""
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this record?"):
            self.delete_record(item_id)

    def delete_record(self, item_id):
        """Send DELETE request to API."""
        url = server_ip + f"/api/preparation_forms/temp/delete/{item_id}/"
        response = requests.delete(url)
        if response.status_code == 200:
            messagebox.showinfo("Success", "Record deleted successfully")
            self.refresh_table()
        else:
            messagebox.showerror("Error", "Failed to delete record")

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

    def get_status_id(self):
        query = f"SELECT id FROM tbl_droplist WHERE name = 'good'"
        # Assuming you have a PostgreSQL connection (replace with your connection details)
        connection = psycopg2.connect(
            dbname="RMManagementSystemDB", user="postgres", password="mbpi", host="192.168.1.13", port="5432"
        )

        # connection = psycopg2.connect(
        #     dbname="RMManagementSystemDB", user="postgres", password="331212", host="localhost", port="5432"
        # )
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        connection.close()

        return result[0] if result else None

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