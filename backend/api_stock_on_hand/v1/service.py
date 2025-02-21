from pydantic_core import to_jsonable_python

from backend.api_droplist.v1.models import DropList
from backend.api_raw_materials.v1.models import RawMaterial
from backend.api_stock_on_hand.v1.exceptions import StockOnHandCreateException, StockOnHandNotFoundException, \
    StockOnHandUpdateException, StockOnHandSoftDeleteException, StockOnHandRestoreException
from backend.api_stock_on_hand.v1.main import AppCRUD, AppService
from backend.api_stock_on_hand.v1.models import StockOnHand
from backend.api_stock_on_hand.v1.schemas import StockOnHandCreate, StockOnHandUpdate, StockOnHandCreateBulk
from uuid import UUID
from backend.api_receiving_report.temp.service import TempReceivingReportCRUD
from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError
from fastapi import Depends, HTTPException
import io
import pandas as pd
from backend.api_warehouses.v1.models import Warehouse
from openpyxl import load_workbook

# These are the code for the app to communicate to the database
class StockOnHandCRUD(AppCRUD):

    def create_rm_soh(self, rm_soh: StockOnHandCreate):
        rm_soh_item = StockOnHand(rm_code_id=rm_soh.rm_code_id,
                                  warehouse_id=rm_soh.warehouse_id,
                                  rm_soh=rm_soh.rm_soh,
                                  status_id = rm_soh.status_id,
                                   description=rm_soh.description,
                                   updated_by_id=rm_soh.updated_by_id,
                                   created_by_id=rm_soh.created_by_id)
        self.db.add(rm_soh_item)
        self.db.commit()
        self.db.refresh(rm_soh_item)
        return rm_soh_item

    def all_rm_soh(self):
        rm_soh_item = self.db.query(StockOnHand).all()
        if rm_soh_item:
            return rm_soh_item
        return []

    def import_rm_soh(self, rm_code_id, total, status_id, warehouse_id):
        # Insert data into the StockOnHand table
        new_stock_on_hand = StockOnHand(
            rm_code_id=rm_code_id,
            rm_soh=total,
            status_id=status_id,
            warehouse_id=warehouse_id
        )
        self.db.add(new_stock_on_hand)
        self.db.commit()
        self.db.refresh(new_stock_on_hand)


    def update_rm_soh(self, rm_soh_id: UUID, rm_soh_update: StockOnHandUpdate):
        try:
            rm_soh = self.db.query(StockOnHand).filter(StockOnHand.id == rm_soh_id).first()
            if not rm_soh or rm_soh.is_deleted:
                raise StockOnHandNotFoundException(detail="Raw Material's SOH not found or already deleted.")

            for key, value in rm_soh_update.model_dump(exclude_unset=True).items():
                setattr(rm_soh, key, value)
            self.db.commit()
            self.db.refresh(rm_soh)
            return rm_soh

        except Exception as e:
            raise StockOnHandUpdateException(detail=f"Error: {str(e)}")

    def soft_delete_rm_soh(self, rm_soh_id: UUID):
        try:
            rm_soh = self.db.query(StockOnHand).filter(StockOnHand.id == rm_soh_id).first()
            if not rm_soh or rm_soh.is_deleted:
                raise StockOnHandNotFoundException(detail="Raw Material's SOH not found or already deleted.")

            rm_soh.is_deleted = True
            self.db.commit()
            self.db.refresh(rm_soh)
            return rm_soh

        except Exception as e:
            raise StockOnHandSoftDeleteException(detail=f"Error: {str(e)}")


    def restore_rm_soh(self, rm_soh_id: UUID):
        try:
            rm_soh = self.db.query(StockOnHand).filter(StockOnHand.id == rm_soh_id).first()
            if not rm_soh or not rm_soh.is_deleted:
                raise StockOnHandNotFoundException(detail="Raw Material's SOH not found or already restored.")

            rm_soh.is_deleted = False
            self.db.commit()
            self.db.refresh(rm_soh)
            return rm_soh

        except Exception as e:
            raise StockOnHandRestoreException(detail=f"Error: {str(e)}")


# These are the code for the business logic like calculation etc.
class StockOnHandService(AppService):
    def create_rm_soh(self, item: StockOnHandCreate):
        try:
            rm_soh_item = StockOnHandCRUD(self.db).create_rm_soh(item)

        except Exception as e:
            raise StockOnHandCreateException(detail=f"Error: {str(e)}")

        return rm_soh_item

    def all_rm_soh(self):
        try:
            rm_soh_item = StockOnHandCRUD(self.db).all_rm_soh()

        except Exception as e:
            raise StockOnHandNotFoundException(detail=f"Error: {str(e)}")
        return rm_soh_item

    def get_rm_soh(self, warehouse_id: UUID, rm_code_id: UUID):
        try:
            rm_soh_item = TempReceivingReportCRUD(self.db).get_latest_soh_record(warehouse_id, rm_code_id)

        except Exception as e:
            raise StockOnHandNotFoundException(detail=f"Error: {str(e)}")
        return rm_soh_item

    # This is the service/business logic in updating the rm_soh.
    def update_rm_soh(self, rm_soh_id: UUID, rm_soh_update: StockOnHandUpdate):
        rm_soh = StockOnHandCRUD(self.db).update_rm_soh(rm_soh_id, rm_soh_update)
        return rm_soh

    # This is the service/business logic in soft deleting the rm_soh.
    def soft_delete_rm_soh(self, rm_soh_id: UUID):
        rm_soh = StockOnHandCRUD(self.db).soft_delete_rm_soh(rm_soh_id)
        return rm_soh


    # This is the service/business logic in soft restoring the rm_soh.
    def restore_rm_soh(self, rm_soh_id: UUID):
        rm_soh = StockOnHandCRUD(self.db).restore_rm_soh(rm_soh_id)
        return rm_soh



    def import_rm_soh(self, content):

        # Convert bytes to a BytesIO stream
        excel_data = io.BytesIO(content)

        try:
            # Convert the incoming items to SQLAlchemy model instances

            def get_rm_code_id(rm_code):
                # Remove any leading or trailing whitespace from rm_code
                raw_mat = rm_code.strip().upper()


                rm_code_record = self.db.query(RawMaterial.id).filter(RawMaterial.rm_code == raw_mat).first()
                return rm_code_record.id if rm_code_record else None

            def get_status_id(status_name):
                status_record = self.db.query(DropList.id).filter(DropList.name == status_name).first()
                return status_record.id if status_record else None


            def get_warehouse_id(warehouse_name):
                # Map sheet names to warehouse numbers
                warehouse_mapping = {
                    "whse1": 1,
                    "whse2": 2,
                    "whse4": 4,
                }

                # Get the warehouse number corresponding to the sheet name
                warehouse_number = warehouse_mapping.get(warehouse_name.lower())

                if warehouse_number:
                    # Query the database using the warehouse number
                    warehouse_record = self.db.query(Warehouse.id).filter(
                        Warehouse.wh_number == warehouse_number).first()
                    return warehouse_record.id if warehouse_record else None
                return None

            # Read the Excel file into a pandas DataFrame
            df = pd.read_excel(excel_data, sheet_name=None, engine='openpyxl', header=0)

            # Process each sheet
            for sheet_name, data in df.items():
                if sheet_name in ['WHSE1', 'WHSE2', 'WHSE4']:

                    # Rename columns manually based on observed structure
                    data.columns = ["A", "B", "C", "D", "E", "F", "G"]  # Adjust as needed

                    # Process specific columns (A, E, F) for each warehouse sheet
                    for _, row in data.iterrows():

                        rm_code = row.get('A', None)  # Use .get() to avoid KeyErrors
                        total = row.get('E', 0)  # Default to 0 if missing
                        status = row.get('F', None)  # Default to 'Unknown' if missing


                        # Convert the status into good if they are blank in the excel
                        if pd.isna(status):
                            status = "good"


                        # Get relevant IDs
                        rm_code_id = get_rm_code_id(rm_code)
                        status_id = get_status_id(status)
                        warehouse_id = get_warehouse_id(sheet_name.lower())

                        # Insert the data into the StockOnHand table
                        StockOnHandCRUD(self.db).import_rm_soh(rm_code_id, total, status_id, warehouse_id)

        except Exception as e:
            raise StockOnHandCreateException(detail=f"Error: {str(e)}")






