import ttkbootstrap as ttk
from ttkbootstrap import DateEntry
from ttkbootstrap.constants import *
import requests
from tkinter import Menu, Toplevel, Label, Entry, Button, messagebox

from ttkbootstrap.dialogs import Messagebox
from .validation import EntryValidation
from backend.settings.database import server_ip
from datetime import datetime


class NoteTable:
    def __init__(self, root):
        self.note_form_tab = root

        # Frame for search
        self.search_var = ttk.StringVar()
        search_frame = ttk.Frame(self.note_form_tab)
        search_frame.pack(fill=X, padx=10, pady=5)
        ttk.Label(search_frame, text="Search:").pack(side=LEFT, padx=5)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=LEFT, fill=X, expand=YES)
        search_entry.bind("<KeyRelease>", self.filter_data)

        # Treeview setup
        self.tree = ttk.Treeview(
            master=self.note_form_tab,
            columns=("Product Code", "Lot No.", "Product Kind", "Consumption Date", "Entry Date"),
            show='headings'
        )
        self.tree.pack(fill=BOTH, expand=YES, padx=10, pady=10)

        # Define column headers
        col_names = ["Product Code", "Lot No.", "Product Kind", "Consumption Date", "Entry Date"]
        for col in col_names:
            self.tree.heading(col, text=col, command=lambda _col=col: self.sort_treeview(_col, False))
            self.tree.column(col, anchor=W)

        # Load Data
        self.load_data()

        # Bind right-click
        self.tree.bind("<Button-3>", self.show_context_menu)

    def load_data(self):
        """Fetch data from API and populate treeview."""
        url = server_ip + "/api/notes/temp/list/"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            self.tree.delete(*self.tree.get_children())  # Clear existing data
            for item in data:
                self.tree.insert("", END, iid=item["id"], values=(
                    item["product_code"],
                    item["lot_number"],
                    item["product_kind_id"],
                    datetime.fromisoformat(item["stock_change_date"]).strftime("%m/%d/%Y"),
                    datetime.fromisoformat(item["created_at"]).strftime("%m/%d/%Y %I:%M %p"),
                ))
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from API: {e}")

    def filter_data(self, event=None):
        """Filter treeview data based on search entry."""
        search_term = self.search_var.get().lower()
        for item in self.tree.get_children():
            values = self.tree.item(item, "values")
            if any(search_term in str(value).lower() for value in values):
                self.tree.reattach(item, "", END)
            else:
                self.tree.detach(item)

    def sort_treeview(self, col, reverse):
        """Sort treeview column data."""
        items = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]
        items.sort(reverse=reverse)
        for index, (val, k) in enumerate(items):
            self.tree.move(k, "", index)
        self.tree.heading(col, command=lambda: self.sort_treeview(col, not reverse))

    def show_context_menu(self, event):
        """Show right-click context menu."""
        item = self.tree.identify_row(event.y)
        if item:
            menu = Menu(self.tree, tearoff=0)
            menu.add_command(label="Edit", command=lambda: self.edit_record(item))
            menu.add_command(label="Delete", command=lambda: self.confirm_delete(item))
            menu.post(event.x_root, event.y_root)

    def edit_record(self, item):
        record = self.tree.item(item, "values")
        if not record:
            return

        edit_window = Toplevel(self.note_form_tab)
        edit_window.title("Edit Record")
        edit_window.geometry("300x225")

        # Fetch product kinds from API
        product_kinds = self.get_product_kinds_api()
        name_to_id = {item["name"]: item["id"] for item in product_kinds}
        product_kind_names = list(name_to_id.keys())

        fields = ["Product Code", "Lot No.", "Product Kind", "Consumption Date"]
        entries = {}

        for i, label_text in enumerate(fields):
            Label(edit_window, text=label_text).grid(row=i, column=0, padx=10, pady=5, sticky='w')
            if label_text == "Product Kind":
                # Mapping MB -> 'Masterbatch Color' and DC -> 'Dry Color'
                kind_mapping = {
                    "MB": product_kind_names[1],  # 'Masterbatch Color'
                    "DC": product_kind_names[0]  # 'Dry Color'
                }

                entry = ttk.Combobox(edit_window, values=product_kind_names, state="readonly", width=20)
                print(product_kind_names)  # Debugging output

                # Get the mapped value or use record[i] if it's not MB/DC
                entry_value = kind_mapping.get(record[i], record[i])
                entry.set(entry_value)


            elif label_text == "Consumption Date":
                entry = DateEntry(edit_window, dateformat="%m/%d/%Y", width=20)
                entry.entry.delete(0, "end")
                entry.entry.insert(0, datetime.strptime(record[i], "%m/%d/%Y").strftime("%m/%d/%Y"))

            else:
                entry = ttk.Entry(edit_window, width=22)
                entry.insert(0, record[i])

            entry.grid(row=i, column=1, padx=5, pady=5, sticky=W)
            entries[label_text] = entry
        def update_data():

            def get_selected_product_kind_id():
                selected_name = entries["Product Kind"].get()
                print(selected_name)
                selected_id = name_to_id.get(selected_name)  # Get the corresponding ID
                if selected_id:
                    return selected_id
                else:
                    return None

            def get_product_kinds_api():
                url = server_ip + "/api/product_kinds/temp/list/"
                response = requests.get(url)

                # Check if the request was successful
                if response.status_code == 200:
                    # Parse JSON response
                    data = response.json()
                    print("Data fetched successfully!")
                    return data
                else:
                    print(f"Failed to fetch data. Status code: {response.status_code}")


            # Product Kind JSON-format choices (coming from the API)
            product_kinds = get_product_kinds_api()
            name_to_id = {kind_item["name"]: kind_item["id"] for kind_item in product_kinds}
            product_kind_names = list(name_to_id.keys())

            # Convert date to YYYY-MM-DD
            try:
                consumption_date = datetime.strptime(entries["Consumption Date"].entry.get(), "%m/%d/%Y").strftime("%Y-%m-%d")
            except ValueError:
                Messagebox.show_error("Error", "Invalid date format. Please use MM/DD/YYYY.")
                return

            data = {
                "product_code": entries["Product Code"].get(),
                "lot_number": entries["Lot No."].get(),
                "product_kind_id": get_selected_product_kind_id(),
                "stock_change_date": consumption_date,
            }

            # Validate the data entries in front-end side
            if EntryValidation.entry_validation(data):
                error_text = EntryValidation.entry_validation(data)
                Messagebox.show_error(f"There is no data in these fields {error_text}.", "Data Entry Error", alert=True)
                return

            note_id = item
            url = f"{server_ip}/api/notes/temp/update/{note_id}/"
            response = requests.put(url, json=data)
            if response.status_code == 200:
                messagebox.showinfo("Success", "Record updated successfully")
                self.load_data()
                edit_window.destroy()
            else:
                messagebox.showerror("Error", "Failed to update record")

        ttk.Button(edit_window, text="Update", command=update_data, width=30).grid(row=len(fields), columnspan=2, pady=10)

    def confirm_delete(self, note_id):
        """Show confirmation before deleting record."""
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this record?"):
            self.delete_record(note_id)

    def delete_record(self, note_id):
        """Send DELETE request to API."""
        url = f"{server_ip}/api/notes/temp/delete/{note_id}/"
        response = requests.delete(url)
        if response.status_code == 200:
            messagebox.showinfo("Success", "Record deleted successfully")
            self.load_data()
        else:
            messagebox.showerror("Error", "Failed to delete record")

    def get_product_kinds_api(self):
        url = server_ip + "/api/product_kinds/temp/list/"
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse JSON response
            data = response.json()
            print("Data fetched successfully!")
            return data
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")

