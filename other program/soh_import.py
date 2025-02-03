import requests
import pandas as pd
import psycopg2

# API Base URL (Replace with your actual API endpoint)
API_BASE_URL = "http://127.0.0.1:8000/api/rm_stock_on_hand/temp/create/"


# Function to get raw material ID from the database
def get_raw_material_id(rm_code):
    query = f"SELECT id FROM public.tbl_raw_materials WHERE rm_code LIKE '{rm_code}%'"
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


# Function to get status ID from the database
def get_status_id(status_name):
    query = f"SELECT id FROM tbl_droplist WHERE name = '{status_name}'"
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


# Function to create record via API
def create_record(rm_code_id, warehouse_id, status_id, rm_soh):
    payload = {
        "rm_code_id": rm_code_id,
        "warehouse_id": warehouse_id,
        "status_id": status_id,
        "rm_soh": rm_soh
    }
    response = requests.post(API_BASE_URL, json=payload)
    if response.status_code == 200:
        print(f"Record for RM Code ID {rm_code_id} saved successfully.")
        print(f"Record for RM Code ID {status_id} saved successfully.")
        print(f" ")
    else:
        print(f"Failed to save record for RM Code ID {rm_code_id}. Status Code: {response.status_code}")


# Read the Excel file (assuming it's named 'data.xlsx')
excel_file = r'C:\Users\Administrator\Desktop\MBPI-Projects\RM-Consumption-Management-System\TEST DATA\Sir Elton\Sample_2\wh1_soh_data.xlsx'
df = pd.read_excel(excel_file)

# Loop through each row in the Excel file
for index, row in df.iterrows():
    # Extract data from each column
    rm_code = row['Codes']  # Column A
    rm_soh = row['Total']  # Column B
    status_name = row['Status']  # Column C
    warehouse_id = row['Warehouse']  # Column D

    # Get raw material ID and status ID
    raw_material_id = get_raw_material_id(str(rm_code))
    status_id = get_status_id(status_name)
    # If both IDs are found, create the record via API
    if raw_material_id and status_id:
        create_record(raw_material_id, warehouse_id, status_id, rm_soh)
    else:
        print(f"Could not find raw material or status for RM Code: {rm_code}, Status: {status_name}")
