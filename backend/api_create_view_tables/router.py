from fastapi import HTTPException, status
from fastapi import APIRouter, Depends
from backend.settings.database import get_db
from datetime import datetime
from sqlalchemy import text
from datetime import date
from sqlalchemy import update
from backend.api_preparation_form.temp.models import TempPreparationForm
from backend.api_notes.temp.models import TempNotes
from backend.api_transfer_form.temp.models import TempTransferForm
from backend.api_outgoing_report.temp.models import TempOutgoingReport
from backend.api_receiving_report.temp.models import TempReceivingReport
from backend.api_stock_on_hand.v1.service import AppService
from backend.api_held_form.temp.models import TempHeldForm
from backend.settings.database import server_ip
import requests


router = APIRouter(prefix="/api")




@router.get("/get/new_soh/")
async def get_new_soh(db: get_db = Depends()):
    try:
        query = text("SELECT * FROM view_sample_new_soh")
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

@router.post("/create_stock_view/")
async def create_stock_view(params_date ,db: get_db = Depends()):
    try:
        # Get params_date's date in YYYYMMDD format for the view name

        # Convert the params_date_entry_value into this format '2025_01_14'
        date_object = datetime.strptime(params_date, "%Y-%m-%d")
        view_date = date_object.strftime("%Y_%m_%d")
        today = date.today()

        view_name = f"view_wh_soh_{view_date}"

        # SQL query for creating the view
        sql_query = f"""
            CREATE OR REPLACE VIEW {view_name} AS
            WITH 
            -- Step 1: Initial Beginning Balance
            initialbalance AS (
                WITH rankedrecords AS (
                    SELECT 
                        SOH.warehouse_id AS warehouseid,
                        WH.wh_name AS WarehouseName,
                        WH.wh_number AS WarehouseNumber,
                        SOH.rm_code_id AS rawmaterialid,
                        RM.rm_code AS RMCode,
                        SOH.rm_soh AS beginningbalance,
                        SOH.stock_change_date AS stockchangedate,
                        STATUS.name AS StatusName,
                        SOH.status_id AS StatusID,
                        row_number() OVER (PARTITION BY SOH.warehouse_id, SOH.rm_code_id, SOH.status_id ORDER BY SOH.stock_change_date DESC) AS row_num
                    FROM tbl_stock_on_hand AS SOH
                    INNER JOIN tbl_raw_materials AS RM 
                        ON SOH.rm_code_id = RM.id
                    INNER JOIN tbl_warehouses AS WH
                        ON SOH.warehouse_id = WH.id
            
                    LEFT JOIN tbl_droplist AS STATUS
                        ON SOH.status_id = STATUS.id
                )
                SELECT 
                    rankedrecords.warehouseid,
                    rankedrecords.warehousename,
                    rankedrecords.warehousenumber,
                    rankedrecords.rawmaterialid,
                    rankedrecords.rmcode,
                    rankedrecords.beginningbalance,
                    rankedrecords.stockchangedate,
                    rankedrecords.statusname,
                    rankedrecords.statusid
                FROM rankedrecords
                WHERE rankedrecords.row_num = 1
            ), 
            
            -- Step 2: Outgoing Report Adjustments
            OGR_Adjustments AS (
                SELECT
                    ogr.warehouse_id AS WarehouseID,
                    ogr.rm_code_id AS RawMaterialID,
                    SUM(ogr.qty_kg) AS Total_OGR_Quantity,
                    ogr.date_computed AS DateComputed
                FROM 
                    tbl_outgoing_reports AS ogr
                INNER JOIN tbl_warehouses AS wh
                    ON ogr.warehouse_id = wh.id
                WHERE 
                    ogr.date_computed = '{today}'
                GROUP BY 
                    ogr.warehouse_id, ogr.rm_code_id, ogr.date_computed
            ),
            
            -- Step 3: Preparation Form Adjustments
            PF_Adjustments AS (
                SELECT 
                    pf.warehouse_id AS WarehouseID,
                    pf.rm_code_id AS RawMaterialID,
                    SUM(pf.qty_prepared) AS Total_Prepared,
                    SUM(pf.qty_return) AS Total_Returned,
                    pf.date_computed AS DateComputed
                FROM 
                    tbl_preparation_forms as pf
                INNER JOIN tbl_warehouses AS wh
                    ON pf.warehouse_id = wh.id
                    
                WHERE 
                    pf.date_computed = '{today}'
                GROUP BY 
                    pf.warehouse_id, pf.rm_code_id, pf.date_computed
            ),
            
            -- Step 4: Transfer Form Adjustments
            TF_Adjustments AS (
                SELECT 
                    tf.from_warehouse_id AS WarehouseID,
                    tf.rm_code_id AS RawMaterialID,
                    -SUM(tf.qty_kg) AS Total_Transferred_Quantity,
                    tf.date_computed AS DateComputed
                FROM 
                    tbl_transfer_forms AS tf
                INNER JOIN tbl_warehouses AS wh_from
                    ON tf.from_warehouse_id = wh_from.id
                WHERE 
                    tf.date_computed = '{today}' AND tf.status_id ISNULL 
                GROUP BY 
                    tf.from_warehouse_id, tf.rm_code_id, tf.date_computed
                UNION ALL
                SELECT 
                    tf.to_warehouse_id AS WarehouseID,
                    tf.rm_code_id AS RawMaterialID,
                    SUM(tf.qty_kg) AS Total_Transferred_Quantity,
                    tf.date_computed AS DateComputed
                FROM 
                    tbl_transfer_forms AS tf
            
                INNER JOIN tbl_warehouses AS wh_to
                    ON tf.to_warehouse_id = wh_to.id
                    
                WHERE 
                    tf.date_computed = '{today}' AND tf.status_id ISNULL
                GROUP BY 
                    tf.to_warehouse_id, tf.rm_code_id, tf.date_computed
            ),
            
            -- Step 5: Receiving Report Adjustments
            RR_Adjustments AS (
                SELECT 
                    rr.warehouse_id AS WarehouseID, 
                    rr.rm_code_id AS RawMaterialID,
                    SUM(rr.qty_kg) AS Total_Received,
                    rr.date_computed AS DateComputed
                FROM 
                    tbl_receiving_reports  AS rr
            
                INNER JOIN tbl_warehouses AS wh
                    ON rr.warehouse_id = wh.id
                    
                WHERE 
                    rr.date_computed = '{today}'
                GROUP BY 
                    rr.warehouse_id, rr.rm_code_id, rr.date_computed
            ),
            
            
            -- Step 6: Change of Status Form Adjustments
            Status_Adjustments AS (
                SELECT 
                        hf.warehouse_id AS WarehouseID, 
                        hf.rm_code_id AS RawMaterialID,
                    SUM(
                        CASE 
                            WHEN new_status.name LIKE 'held%'
                                THEN qty_kg
                            ELSE 0 
                        END
                        ) 
                        AS Total_Held,
                    SUM(CASE WHEN new_status.name LIKE 'good%' THEN qty_kg ELSE 0 END) AS Total_Released,
                    hf.date_computed AS DateComputed
                FROM 
                    tbl_held_forms as hf
            
                INNER JOIN tbl_warehouses AS wh
                    ON hf.warehouse_id = wh.id
            
                INNER JOIN tbl_droplist AS current_status
                    ON hf.current_status_id = current_status.id
            
                INNER JOIN tbl_droplist AS new_status
                    ON hf.new_status_id = new_status.id
            
                LEFT JOIN InitialBalance AS ib
                    ON hf.new_status_id = ib.statusid
                    
                WHERE 
                    hf.date_computed = '{today}'
                GROUP BY 
                    hf.warehouse_id, hf.rm_code_id, hf.date_computed
            ),
            
            -- Step 7: Held Status Details Adjustments
            Held_Status_Details AS (
                SELECT 
                    hf.rm_code_id AS RawMaterialID,
                    wh.wh_name AS WarehouseName,
                    wh.id AS WarehouseID,
                    wh.wh_number AS WarehouseNumber,
                    rm.rm_code AS RMCode,
                    SUM(qty_kg) AS HeldQuantity,
                    new_status.name AS Status,
                    hf.date_computed,
                    hf.new_status_id AS StatusID
                FROM 
                    tbl_held_forms AS hf
                INNER JOIN tbl_raw_materials AS rm
                    ON hf.rm_code_id = rm.id
                INNER JOIN tbl_warehouses AS wh
                    ON hf.warehouse_id = wh.id
                INNER JOIN tbl_droplist AS new_status
                    ON hf.new_status_id = new_status.id
                
                WHERE 
                    new_status.name LIKE 'held%' AND hf.date_computed = '{today}'
                GROUP BY 
                    hf.rm_code_id, wh.wh_name, wh.wh_number, rm.rm_code, new_status.name, hf.date_computed, wh.id, hf.new_status_id
            )
            
            
            -- Final Query
            SELECT
                ib.rawmaterialid,
                ib.rmcode,
                ib.warehouseid,
                ib.warehousename,
                ib.warehousenumber,
                ib.BeginningBalance
                + COALESCE(rr.Total_Received, 0)
                + COALESCE(pf.Total_Returned, 0)
                - COALESCE(ogr.Total_OGR_Quantity, 0)
                - COALESCE(pf.Total_Prepared, 0)
                + COALESCE(tf.Total_Transferred_Quantity, 0)
                - COALESCE(cs.Total_Held, 0)
                + COALESCE(cs.Total_Released, 0) AS New_Beginning_Balance,
                '' AS Status,
                NULL AS StatusID
            FROM 
                initialbalance ib
            LEFT JOIN 
                OGR_Adjustments ogr 
                ON ib.WarehouseID = ogr.WarehouseID AND ib.RawMaterialID = ogr.RawMaterialID
            LEFT JOIN 
                PF_Adjustments pf 
                ON ib.WarehouseID = pf.WarehouseID AND ib.RawMaterialID = pf.RawMaterialID
            LEFT JOIN 
                TF_Adjustments tf 
                ON ib.WarehouseID = tf.WarehouseID AND ib.RawMaterialID = tf.RawMaterialID
            LEFT JOIN 
                RR_Adjustments rr 
                ON ib.WarehouseID = rr.WarehouseID AND ib.RawMaterialID = rr.RawMaterialID
            LEFT JOIN 
                Status_Adjustments cs 
                ON ib.WarehouseID = cs.WarehouseID AND ib.RawMaterialID = cs.RawMaterialID
            
            WHERE ib.statusid ISNULL
            
            UNION ALL
            
            SELECT
                hs.rawmaterialid,
                hs.RMCode,
                hs.warehouseid,
                hs.WarehouseName,
                hs.WarehouseNumber,
                hs.HeldQuantity AS New_Beginning_Balance,
                hs.Status,
                hs.StatusID
            FROM 
                Held_Status_Details hs
            
            ORDER BY 
                RMCode, WarehouseName, WarehouseNumber, Status NULLS FIRST;


        """

        # Execute the query
        db.execute(text(sql_query))

        # Commit the transaction
        db.commit()

        return {"message": "Views created successfully"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))



# API endpoint to get records from the dynamic view
@router.get("/get_soh/", response_model=list[dict])
def get_soh(params_date: str, db: get_db = Depends()):
    date_object = datetime.strptime(params_date, "%Y-%m-%d")
    view_date = date_object.strftime("%Y_%m_%d")
    records = get_data_from_dynamic_view(db, view_date)

    if not records:
        raise HTTPException(status_code=404, detail="No records found")
    return records


# Helper function to query the view dynamically
def get_data_from_dynamic_view(db, param_date: str) -> list[dict]:
    # Format the view name dynamically
    view_name = f"view_wh_soh_{param_date}"

    # Prepare the SQL query to select all records from the dynamic view
    query = text(f"SELECT * FROM {view_name}")

    try:
        # Execute the query and fetch all rows
        result = db.execute(query).fetchall()

        # Convert the result into a list of dictionaries
        records = [
            {
                "rmcode": row[0],
                "warehousename": row[1],
                "warehousenumber": row[2],
                "new_beginning_balance": row[3],
                "status": row[4]
            }
            for row in result
        ]

        return records

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")


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
async def update_stock_on_hand(db=Depends(get_db)):
    """
    Endpoint to update the stock-on-hand records from an external API.

    Args:
        db: Database session dependency injected by FastAPI.

    Returns:
        A JSON response indicating the success of the operation.
    """
    url = f"{server_ip}/api/get/new_soh/"

    try:
        # Step 1: Fetch data from the external API
        response = requests.get(url)
        if response.status_code != 200:
            # Raise an HTTPException if the API request fails
            raise HTTPException(status_code=500, detail="Failed to fetch data from API")

        # Parse the API response as a list of dictionaries
        raw_data = response.json()

        # Step 2: Transform and insert the data into the database
        for record in raw_data:
            # Prepare the data for database insertion
            transformed_data = {
                "rm_code_id": record["rawmaterialid"],  # Raw material ID
                "warehouse_id": record["warehouseid"],  # Warehouse ID
                "rm_soh": record["new_beginning_balance"],  # New beginning stock balance
                "status_id": record["statusid"],  # Stock status ID
            }

            # Call the service method to create a StockOnHand record
            result = AppService(db).create_stock_on_hand(transformed_data)
            if not result.success:
                # Raise an exception if the insertion fails
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to insert record: {result.message}",
                )

        # Return a success message upon successful insertion
        return {"message": "StockOnHand records updated successfully."}

    except Exception as e:
        # Handle any unexpected exceptions and return a 500 error with details
        raise HTTPException(status_code=500, detail=str(e))

