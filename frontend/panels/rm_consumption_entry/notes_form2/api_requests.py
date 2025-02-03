import requests
from backend.settings.database import server_ip
from ttkbootstrap.dialogs.dialogs import Messagebox
from datetime import datetime


class ApiRequest:
    def create_note(self, data):
        # Send a POST request to the API
        try:
            response = requests.post(f"{server_ip}/api/notes/temp/create/", json=data)
            if response.status_code == 200:  # Successfully created
                # Messagebox.show_info("Success", "Data added successfully!")
                return True

                # refresh_table()  # Refresh the table
        except requests.exceptions.RequestException as e:
            Messagebox.show_info("Success", "Data added successfully!")



    def get_product_kinds_api(self):
        url = server_ip+"/api/product_kinds/temp/list/"
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse JSON response
            data = response.json()
            print("Data fetched successfully!")
            return data
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")

    def get_notes_data_api(self):
        # API endpoint
        url = server_ip + "/api/notes/temp/list/"

        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for HTTP status codes 4xx/5xx

            # Parse the JSON response
            data = response.json()
            print(data)
            # Transform the JSON data into a format suitable for rowdata
            # Assuming the JSON response looks like this:
            # [{"product_code": "A123", "lot_no": "IzzyCo", "product_kind": "asd", "consumption_date": "2025-01-16", "entry_date": "2025-01-15"}, ...]
            rowdata = [
                (
                    item["product_code"],
                    item["lot_number"],
                    item["product_kind_id"],
                    datetime.fromisoformat(item["stock_change_date"]).strftime("%m/%d/%Y"),
                    datetime.fromisoformat(item["created_at"]).strftime("%m/%d/%Y %I:%M %p")
                )
                for item in data
            ]
            return rowdata
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from API: {e}")
            return []  # Return an empty list if there's an error