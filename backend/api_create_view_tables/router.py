from fastapi import HTTPException
from fastapi import APIRouter, Depends
from backend.settings.database import get_db
from datetime import datetime
from sqlalchemy import text
import pandas as pd
import os
import psycopg2  # PostgreSQL library
from backend.settings.database import engine

router = APIRouter(prefix="/api")

@router.post("/create_stock_view/")
async def create_stock_view(db: get_db = Depends()):

    try:
        # Get today's date in YYYYMMDD format for the view name
        today = datetime.now().strftime("%Y-%m-%d")
        view_today = datetime.now().strftime("%Y_%m_%d")

        view_name = f"view_wh_soh_{view_today}"

        # SQL query for creating the view
        sql_query = f"""
            CREATE OR REPLACE VIEW {view_name} AS
            WITH 
                InitialBalance AS (
                    WITH 
                        RankedRecords as (
                            SELECT
                                warehouse_id AS WarehouseID,
                                rm_code_id AS RawMaterialID,
                                rm_soh AS BeginningBalance,
                                stock_change_date AS StockChangeDate,
                                ROW_NUMBER() OVER (
                                    PARTITION BY warehouse_id, rm_code_id 
                                    ORDER BY stock_change_date DESC
                                ) AS row_num
                            FROM tbl_stock_on_hand
                        )
                    SELECT 
                        WarehouseID,
                        RawMaterialID,
                        BeginningBalance,
                        StockChangeDate
                    FROM RankedRecords
                    WHERE row_num = 1
                ),
                OGR_Adjustments AS (
                    SELECT
                        ogr.warehouse_id AS WarehouseID,
                        ogr.rm_code_id AS RawMaterialID,
                        SUM(ogr.qty_kg) AS Total_OGR_Quantity
                    FROM tbl_outgoing_reports AS ogr
                    WHERE  ogr.date_computed = '{today}'
                    GROUP BY ogr.warehouse_id, ogr.rm_code_id
                ),
                PF_Adjustments AS (
                    SELECT 
                        pf.warehouse_id AS WarehouseID,
                        pf.rm_code_id AS RawMaterialID,
                        SUM(pf.qty_prepared) AS Total_Prepared,
                        SUM(pf.qty_return) AS Total_Returned
                    FROM tbl_preparation_forms AS pf
                    WHERE pf.date_computed = '{today}'
                    GROUP BY pf.warehouse_id, pf.rm_code_id
                ),
                TF_Adjustments AS (
                    SELECT 
                        tf.from_warehouse_id AS WarehouseID,
                        tf.rm_code_id AS RawMaterialID,
                        -SUM(tf.qty_kg) AS Total_Transferred_Quantity
                    FROM tbl_transfer_forms AS tf
                    WHERE tf.date_computed = '{today}'
                    GROUP BY tf.from_warehouse_id, tf.rm_code_id
                    UNION ALL
                    SELECT 
                        tf.to_warehouse_id AS WarehouseID,
                        tf.rm_code_id AS RawMaterialID,
                        SUM(tf.qty_kg) AS Total_Transferred_Quantity
                    FROM tbl_transfer_forms AS tf
                    WHERE tf.date_computed = '{today}'
                    GROUP BY tf.to_warehouse_id, tf.rm_code_id
                ),
                RR_Adjustments AS (
                    SELECT 
                        rr.warehouse_id AS WarehouseID, 
                        rr.rm_code_id AS RawMaterialID,
                        SUM(rr.qty_kg) AS Total_Received
                    FROM tbl_receiving_reports AS rr
                    WHERE rr.date_computed = '{today}'
                    GROUP BY rr.warehouse_id, rr.rm_code_id
                ),
                Status_Adjustments AS (
                    SELECT 
                        hf.warehouse_id AS WarehouseID, 
                        hf.rm_code_id AS RawMaterialID,
                        SUM(CASE WHEN status.name LIKE 'held%' THEN qty_kg ELSE 0 END) AS Total_Held,
                        SUM(CASE WHEN status.name LIKE 'good%' THEN qty_kg ELSE 0 END) AS Total_Released
                    FROM tbl_held_forms AS hf
                    INNER JOIN tbl_droplist AS status
                        ON hf.current_status_id = status.id
                    WHERE hf.date_computed = '{today}'
                    GROUP BY hf.warehouse_id, hf.rm_code_id
                )
            SELECT
                ib.WarehouseID AS warehouse_id,
                ib.RawMaterialID AS rm_code_id,
                ib.BeginningBalance
                + COALESCE(rr.Total_Received, 0)
                + COALESCE(pf.Total_Returned, 0)
                - COALESCE(ogr.Total_OGR_Quantity, 0)
                - COALESCE(pf.Total_Prepared, 0)
                + COALESCE(tf.Total_Transferred_Quantity, 0)
                AS New_Beginning_Balance,
                CURRENT_DATE AS stock_change_date
            FROM 
                InitialBalance ib
            LEFT JOIN OGR_Adjustments ogr 
                ON ib.WarehouseID = ogr.WarehouseID AND ib.RawMaterialID = ogr.RawMaterialID
            LEFT JOIN PF_Adjustments pf 
                ON ib.WarehouseID = pf.WarehouseID AND ib.RawMaterialID = pf.RawMaterialID
            LEFT JOIN TF_Adjustments tf 
                ON ib.WarehouseID = tf.WarehouseID AND ib.RawMaterialID = tf.RawMaterialID
            LEFT JOIN RR_Adjustments rr 
                ON ib.WarehouseID = rr.WarehouseID AND ib.RawMaterialID = rr.RawMaterialID
            LEFT JOIN Status_Adjustments cs 
                ON ib.WarehouseID = cs.WarehouseID AND ib.RawMaterialID = cs.RawMaterialID
            ORDER BY ib.StockChangeDate DESC;
        """

        # Execute the query
        db.execute(text(sql_query))

        # Commit the transaction
        db.commit()

        # Export it into excel
        export_into_excel(view_name)

        return {"message": "Views created successfully"}

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def export_into_excel(view_name, folder_path="output_folder"):
    # Ensure the folder exists, create if it doesn't
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Define your query to retrieve the data
    query = f"""
                SELECT * 
                FROM {view_name}
            """

    # Fetch the data into a pandas DataFrame (ensure you have your SQLAlchemy engine set up correctly)
    df = pd.read_sql(query, engine)

    # Define the path for the Excel file in the desired folder
    file_path = os.path.join(folder_path, f"soh_whse.xlsx")

    # Create a Pandas Excel writer object
    with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
        # Write the entire data to the "Notes" sheet
        df.to_excel(writer, sheet_name='Notes', index=False)

        # Separate data by warehouse number and write them into their respective sheets
        for warehouse_id in ['WHSE1', 'WHSE2', 'WHSE4']:
            warehouse_df = df[df['warehouse_id'] == warehouse_id]
            warehouse_df.to_excel(writer, sheet_name=warehouse_id, index=False)

    return file_path  # Optional: return the file path if needed
