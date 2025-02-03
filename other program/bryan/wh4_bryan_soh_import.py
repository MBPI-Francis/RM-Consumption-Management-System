import requests
import pandas as pd
import psycopg2

from backend.api_droplist.v1.router import delete_droplist

# API Base URL (Replace with your actual API endpoint)
API_BASE_URL = "http://127.0.0.1:8000/api/rm_stock_on_hand/temp/create/"


# Function to get raw material ID from the database
def get_raw_material_id(rm_code):
    query = f"SELECT mid FROM wh4_material_codes WHERE material_code = '{rm_code}'"
    # Assuming you have a PostgreSQL connection (replace with your connection details)
    connection = psycopg2.connect(
        dbname="Inventory", user="postgres", password="mbpi", host="192.168.1.13", port="5432"
    )
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchone()

    connection.close()
    return result[0] if result else None


# Function to create record via API
def create_record(reference_no, date_received, material_code_id, quantity, area_location, id, deleted, status):

    connection = psycopg2.connect(
        dbname="Inventory", user="postgres", password="mbpi", host="192.168.1.13", port="5432"
    )

    # Create a cursor object to interact with the database
    cursor = connection.cursor()

    # Define the SQL query to insert data into a table
    insert_query = """
        INSERT INTO wh4_receiving_report (reference_no, date_received, material_code, quantity, area_location, id, deleted, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """

    # Values to be inserted (e.g., raw material code and description)
    values_to_insert = (reference_no, date_received, material_code_id, quantity, area_location, id, deleted, status)

    # Execute the query and pass the values
    cursor.execute(insert_query, values_to_insert)

    # Commit the transaction to save the changes
    connection.commit()

    # Print a success message
    print("Data inserted successfully.")

    # Close the cursor and connection
    cursor.close()
    connection.close()


# Read the Excel file (assuming it's named 'data.xlsx')
excel_file = r'C:\Users\Administrator\Desktop\TEST DATA\bryan_wh4_data.xlsx'
df = pd.read_excel(excel_file)

# Loop through each row in the Excel file
for index, row in df.iterrows():
    # Extract data from each column

    reference_no = row['Reference']
    date_received = row['Date']
    material_code = row['Code']
    quantity = row['Quantity']
    area_location = row['Area']
    id = row['ID']
    deleted = row['Deleted']
    status = row['Status']

    # Get raw material ID and status ID
    material_code_id = get_raw_material_id(material_code)

    # If both IDs are found, create the record via API
    create_record(reference_no, date_received, material_code_id, quantity, area_location, id, deleted, status)
