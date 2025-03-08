# This where all the shared variable stored
# All the variables functions we're used by the program.

import requests
from backend.settings.database import server_ip

class SharedFunctions:

    @staticmethod
    def get_warehouse_api():
        url = server_ip + "/api/warehouses/v1/list/"
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse JSON response
            data = response.json()

            return data
        else:
            return []


    @staticmethod
    def get_rm_code_api():
        url = server_ip + "/api/raw_materials/v1/list/"
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse JSON response
            data = response.json()

            return data
        else:
            return []

    @staticmethod
    def get_status_api():
        url = server_ip + "/api/status/v1/list/"
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse JSON response
            data = response.json()
            return data
        else:
            return []