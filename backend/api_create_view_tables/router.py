from fastapi import HTTPException
from fastapi import APIRouter, Depends
from backend.settings.database import get_db
from datetime import datetime
from sqlalchemy import text
import pandas as pd
import os
from ttkbootstrap import Style
from tkinter.filedialog import asksaveasfilename
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from openpyxl.worksheet.datavalidation import DataValidation
import psycopg2  # PostgreSQL library
from backend.settings.database import engine
from datetime import date

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
                    ogr.date_computed = '{params_date}'
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
                    pf.date_computed = '{params_date}'
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
                    tf.date_computed = '{params_date}' AND tf.status_id ISNULL 
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
                    tf.date_computed = '{params_date}' AND tf.status_id ISNULL
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
                    rr.date_computed = '{params_date}'
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
                    hf.date_computed = '{params_date}'
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
                    hf.date_computed
                FROM 
                    tbl_held_forms AS hf
                INNER JOIN tbl_raw_materials AS rm
                    ON hf.rm_code_id = rm.id
                INNER JOIN tbl_warehouses AS wh
                    ON hf.warehouse_id = wh.id
                INNER JOIN tbl_droplist AS new_status
                    ON hf.new_status_id = new_status.id
                
                WHERE 
                    new_status.name LIKE 'held%' AND hf.date_computed = '{params_date}'
                GROUP BY 
                    hf.rm_code_id, wh.wh_name, wh.wh_number, rm.rm_code, new_status.name, hf.date_computed, wh.id
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
                '' AS Status
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
                hs.Status
            FROM 
                Held_Status_Details hs
            
            ORDER BY 
                RMCode, WarehouseName, WarehouseNumber, Status NULLS FIRST;


        """

        # Execute the query
        db.execute(text(sql_query))

        # Commit the transaction
        db.commit()

        def create_soh_whse_excel():
            # Create a new workbook
            wb = Workbook()

            # Sheet 1: NOTES
            notes_sheet = wb.active
            notes_sheet.title = "NOTES"

            # Populate the NOTES sheet
            notes_sheet["A1"] = "Daily Ending Inventory Report from:"
            notes_sheet["B1"] = "September 18, 2023"  # Sample date
            notes_sheet["A2"] = "List of Batches Included in Report"
            notes_sheet["A3"] = "MASTERBATCH"
            notes_sheet.append(["PRODUCT CODE", "LOT#", "Product Kind"])
            notes_sheet.append(["SAMPLE-CODE-1", "SAMPLE-5106AJ-5109AJ", "SAMPLE-MB"])
            notes_sheet.append(["SAMPLE-CODE-2", "SAMPLE-5110AJ", "SAMPLE-DC"])

            # Apply formatting
            for col in ["A", "B", "C"]:
                for cell in notes_sheet[col]:
                    cell.alignment = Alignment(horizontal="center", vertical="center")
            notes_sheet["A4"].font = Font(bold=True)

            # Function to create a WHSE sheet
            def create_whse_sheet(sheet_name):
                sheet = wb.create_sheet(sheet_name)

                # Populate the header
                header = [
                    "Date", "No of bags", "qty per packing",
                    f"{sheet_name} - Excess", "Total", "Status", "drop list"
                ]
                sheet.append(header)
                sheet["A1"] = "09/18/2025"  # Example date
                sheet["A1"].font = Font(bold=True)

                # Example data for rows
                data = [
                    ["A7", "", "", 18.1, 18.1, "", "held : under evaluation"],
                    ["A8", "", "", 5.52, 5.52, "", "held : reject"],
                    ["AO1", 5, 25.00, 7.19, 132.19, "", "held : contaminated"],
                    ["AO8", "", "", 27.97, 27.97, "", ""],
                    ["AO9", "", "", 7.92, 7.92, "", ""],
                ]

                for row in data:
                    sheet.append(row)

                # Create a dropdown list for the "drop list" column
                dv = DataValidation(
                    type="list",
                    formula1='"held : under evaluation,held : reject,held : contaminated"',
                    allow_blank=True,
                    showDropDown=True
                )
                # Apply the data validation to the G column for rows 2 to 100
                for row in range(2, 101):
                    cell = f"G{row}"  # Example: G2, G3, ..., G100
                    dv.add(sheet[cell])
                sheet.add_data_validation(dv)

            # Sheet 2: WHSE1
            create_whse_sheet("WHSE1")

            # Sheet 3: WHSE2
            create_whse_sheet("WHSE2")

            # Sheet 4: WHSE4
            create_whse_sheet("WHSE4")

            # Initialize ttkbootstrap Style and create the dialog
            style = Style("cosmo")
            root = style.master
            root.withdraw()  # Hide the root window

            # Use tkinter's asksaveasfilename for file dialog
            file_path = asksaveasfilename(
                title="Save Excel File",
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx")]
            )

            # Save the workbook
            if file_path:
                try:
                    wb.save(file_path)
                    print(f"Excel file saved successfully at {file_path}")
                except Exception as e:
                    print(f"Error saving file: {e}")
            else:
                print("File save canceled by the user.")

            return print("File is created")

        return {"message": "Views created successfully"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))



# API endpoint to get records from the dynamic view
@router.get("/get_soh/{date}", response_model=list[dict])
def get_soh(date: str, db: get_db = Depends()):
    records = get_data_from_dynamic_view(db, date)
    if not records:
        raise HTTPException(status_code=404, detail="No records found")
    return records


# Helper function to query the view dynamically
def get_data_from_dynamic_view(db, date: str) -> list[dict]:
    # Format the view name dynamically
    view_name = f"view_wh_soh_{date}"

    # Prepare the SQL query to select all records from the dynamic view
    query = text(f"SELECT rmcode, warehousename, warehousenumber, new_beginning_balance, status FROM {view_name}")

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



