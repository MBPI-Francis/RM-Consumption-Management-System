from fastapi import HTTPException, status
from fastapi import APIRouter, Depends
from backend.settings.database import get_db
from datetime import datetime
from sqlalchemy import text
from datetime import date, timedelta
from sqlalchemy import update
from backend.api_preparation_form.temp.models import TempPreparationForm
from backend.api_notes.temp.models import TempNotes
from backend.api_transfer_form.temp.models import TempTransferForm
from backend.api_outgoing_report.temp.models import TempOutgoingReport
from backend.api_receiving_report.temp.models import TempReceivingReport
from backend.api_stock_on_hand.v1.models import StockOnHand
from backend.api_held_form.temp.models import TempHeldForm
from backend.settings.database import server_ip
import requests


router = APIRouter(prefix="/api")




@router.get("/get/new_soh/")
async def get_new_soh(db: get_db = Depends()):
    try:
        query = text("SELECT * FROM view_ending_stocks_balance")
        result = db.execute(query)
        rows = result.fetchall()
        # Convert rows to a list of dictionaries
        # Use explicit extraction of column values
        data = [
            {column: value for column, value in row._mapping.items()}
            for row in rows
        ]
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.get("/get/beginning_balance/")
async def get_beginning_balance(db: get_db = Depends()):
    try:
        query = text("SELECT * FROM view_beginning_soh")
        result = db.execute(query)
        rows = result.fetchall()
        # Convert rows to a list of dictionaries
        # Use explicit extraction of column values
        data = [
            {column: value for column, value in row._mapping.items()}
            for row in rows
        ]
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# API endpoint to get records from the dynamic view
# @router.get("/get_soh/", response_model=list[dict])
# def get_soh(db: get_db = Depends()):
#
#     records = get_data_from_dynamic_view(db)
#
#     if not records:
#         raise HTTPException(status_code=404, detail="No records found")
#     return records


# # Helper function to query the view dynamically
# def get_data_from_dynamic_view(db) -> list[dict]:
#     # Format the view name dynamically
#
#
#     # Prepare the SQL query to select all records from the dynamic view
#     query = text(f"SELECT * FROM view_ending_stocks_balance")
#
#     try:
#         # Execute the query and fetch all rows
#         result = db.execute(query).fetchall()
#
#         # Convert the result into a list of dictionaries
#         records = [
#             {
#                 "rmcode": row[0],
#                 "warehousename": row[1],
#                 "warehousenumber": row[2],
#                 "new_beginning_balance": row[3],
#                 "status": row[4]
#             }
#             for row in result
#         ]
#
#         return records
#
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")


# Helping function for the api
def update_date_computed_for_table(table, db):
    """
    Updates the `date_computed` column to the current date for records where it is NULL in the given table.
    """
    try:
        # Generate the current date
        current_date = date.today()

        # Create an update query
        stmt = (
            update(table)
            .where(table.date_computed.is_(None))
            .values(date_computed=current_date)
        )

        # Execute the query
        db.execute(stmt)
        db.commit()
        return True

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update table {table.__tablename__}: {e}")

@router.post("/update-date-computed")
async def update_date_computed(db: get_db = Depends()):
    """
    Updates the `date_computed` column to the current date for all specified tables.
    """
    tables = [
        TempNotes,
        TempPreparationForm,
        TempTransferForm,
        TempOutgoingReport,
        TempReceivingReport,
        TempHeldForm,
    ]

    updated_tables = []

    for table in tables:
        success = update_date_computed_for_table(table, db)
        if success:
            updated_tables.append(table.__tablename__)

    return {"message": "Update successful", "updated_tables": updated_tables}


@router.post("/update_stock_on_hand/")
async def update_stock_on_hand(params_date: str, db=Depends(get_db)):
    """
    Endpoint to update the stock-on-hand records from an external API.

    Args:
        db: Database session dependency injected by FastAPI.

    Returns:
        A JSON response indicating the success of the operation.
    """
    # Convert the date_entry_value into this format '2025_01_14'
    date_object = datetime.strptime(params_date, "%Y-%m-%d")
    formatted_date = date_object.strftime("%Y_%m_%d")
    current_date = date.today()

    # Format the view name dynamically
    view_name = f"view_wh_soh_{formatted_date}"

    # Prepare the SQL query to select all records from the dynamic view
    query = text(f"SELECT * FROM {view_name}")

    try:
        # Execute the query and fetch all rows
        result = db.execute(query).fetchall()

        # Convert the result into a list of dictionaries
        records = [
            {
                "rawmaterialid": row[0],
                "warehouseid": row[2],
                "new_beginning_balance": row[5],
                "statusid": row[7]
            }
            for row in result
        ]
        print("The data: ", records)
        # Step 2: Transform and insert the data into the database
        for record in records:
            rm_soh_item = StockOnHand(rm_code_id=record["rawmaterialid"],
                                      warehouse_id=record["warehouseid"],
                                      rm_soh=record["new_beginning_balance"],
                                      status_id= record["statusid"],
                                      date_computed=current_date)
            db.add(rm_soh_item)
            db.commit()
            db.refresh(rm_soh_item)

        # Return a success message upon successful insertion
        return {"message": "StockOnHand records updated successfully."}

    except Exception as e:
        # Handle any unexpected exceptions and return a 500 error with details
        raise HTTPException(status_code=500, detail=str(e))


# Helping function for the api
def clear_table_func(table, db):
    """
    Updates the `date_computed` column to the current date for records where it is NULL in the given table.
    """
    try:

        # Create an update query
        stmt = (
            update(table)
            .where((table.is_cleared.is_(None)) | (table.is_cleared == False))  # Check for NULL or False
            .values(is_cleared=True)  # Set is_clear to True
        )

        # Only uncomment this for unclearing the records
        # stmt = (
        #     update(table)
        #     .where((table.is_cleared == True))  # Check for NULL or False
        #     .values(is_cleared=False)  # Set is_clear to True
        # )

        # Execute the query
        db.execute(stmt)
        db.commit()
        return True

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update table {table.__tablename__}: {e}")

@router.post("/clear-table-data")
async def clear_table_data(db: get_db = Depends()):
    """
    Updates the `is_cleared` column to True for all specified tables.
    """
    tables = [
        TempNotes,
        TempPreparationForm,
        TempTransferForm,
        TempOutgoingReport,
        TempReceivingReport,
        TempHeldForm,
    ]

    updated_tables = []

    for table in tables:
        success = clear_table_func(table, db)
        if success:
            updated_tables.append(table.__tablename__)

    return {"message": "Update successful", "updated_tables": updated_tables}



