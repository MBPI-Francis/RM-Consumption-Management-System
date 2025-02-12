from backend.api_receiving_report.temp.exceptions import TempReceivingReportCreateException, TempReceivingReportNotFoundException, \
    TempReceivingReportUpdateException, TempReceivingReportSoftDeleteException, TempReceivingReportRestoreException
from backend.api_receiving_report.temp.main import AppCRUD, AppService
from backend.api_receiving_report.temp.models import TempReceivingReport
from backend.api_receiving_report.temp.schemas import TempReceivingReportCreate, TempReceivingReportUpdate
from backend.api_raw_materials.v1.models import RawMaterial
from backend.api_warehouses.v1.models import Warehouse
from uuid import UUID
from backend.api_stock_on_hand.v1.models import StockOnHand
from sqlalchemy import desc, or_
from sqlalchemy.sql import func, cast, case
from sqlalchemy.types import String
from sqlalchemy import text


# These are the code for the app to communicate to the database
class TempReceivingReportCRUD(AppCRUD):


    def get_latest_soh_record(self, warehouse_id, rm_code_id):
        """
        Get the latest stock-on-hand record based on warehouse_id, rm_code_id, and latest date.
        """

        return (
            self.db.query(StockOnHand)
            .filter(
                StockOnHand.warehouse_id == warehouse_id,
                StockOnHand.rm_code_id == rm_code_id,
            )
            .order_by(desc(StockOnHand.stock_change_date))  # Assuming 'date' is the column for the latest date
            .first()
        )


    def create_receiving_report(self, receiving_report: TempReceivingReportCreate):


        status_query = text(""" SELECT id FROM tbl_droplist WHERE name = 'good' """)

        status_record = self.db.execute(status_query).fetchone()  # or .fetchall() if expecting multiple rows
        status_result = status_record

        if status_result:
            status_id = status_result[0]

        else:
            print("There is an error with getting the status ID")
            return

        # Check if the status id is null
        query = text("""SELECT * FROM view_beginning_soh
                        WHERE warehouseid = :warehouse_id
                              AND rawmaterialid = :rm_code_id
                              AND statusid = :status_id""")



        record = self.db.execute(query, {
            "warehouse_id": receiving_report.warehouse_id,
            "rm_code_id": receiving_report.rm_code_id,
            "status_id": status_id
        }).fetchone()  # or .fetchall() if expecting multiple rows
        result = record

        # This feature is required for the calculation
        if not result:
            # Create a new StockOnHand record
            new_stock = StockOnHand(
                rm_code_id=receiving_report.rm_code_id,
                warehouse_id=receiving_report.warehouse_id,
                rm_soh=0.00,
                status_id=status_id
            )
            self.db.add(new_stock)
            self.db.commit()
            self.db.refresh(new_stock)


        # Get the latest StockOnHand record ID
        latest_soh_record = self.get_latest_soh_record(
            warehouse_id=receiving_report.warehouse_id,
            rm_code_id=receiving_report.rm_code_id,
        )

        # Check if the raw material code in warahouse # haves stocks
        if latest_soh_record:
            # If it had stocks, then put the ID of that stock record
            latest_soh_record_id = latest_soh_record.id
            receiving_report_item = TempReceivingReport(rm_code_id=receiving_report.rm_code_id,
                                                       warehouse_id=receiving_report.warehouse_id,
                                                       rm_soh_id=latest_soh_record_id,
                                                       ref_number=receiving_report.ref_number,
                                                       receiving_date=receiving_report.receiving_date,
                                                       qty_kg=receiving_report.qty_kg
                                                       )

        else:
            # If there is no stock record, then make the rm_soh_id NULL in the database
            receiving_report_item = TempReceivingReport(rm_code_id=receiving_report.rm_code_id,
                                                       warehouse_id=receiving_report.warehouse_id,
                                                       ref_number=receiving_report.ref_number,
                                                       receiving_date=receiving_report.receiving_date,
                                                       qty_kg=receiving_report.qty_kg
                                                       )


        self.db.add(receiving_report_item)
        self.db.commit()
        self.db.refresh(receiving_report_item)
        return receiving_report_item

    def get_receiving_report(self):
        """
        Join StockOnHand, ReceivingReport, Warehouse, and RawMaterial tables.
        """
        # Join tables
        stmt = (
            self.db.query(
                TempReceivingReport.id,
                RawMaterial.rm_code.label("raw_material"),
                TempReceivingReport.qty_kg,
                TempReceivingReport.ref_number,
                Warehouse.wh_name,
                TempReceivingReport.receiving_date,
                TempReceivingReport.created_at,
                case(
                    (StockOnHand.id == None, "No Beginning Balance"),  # If no StockOnHand record, show "No Balance"
                    else_=func.concat(
                        cast(StockOnHand.rm_soh, String),
                        "(kg) - ",
                        func.to_char(StockOnHand.stock_change_date, "MM/DD/YYYY")
                    )
                ).label("soh_and_date"),
                TempReceivingReport.created_at,
                TempReceivingReport.updated_at

            )
            .outerjoin(StockOnHand, StockOnHand.id == TempReceivingReport.rm_soh_id)  # Left join StockOnHand with ReceivingReport
            .join(RawMaterial, TempReceivingReport.rm_code_id == RawMaterial.id)       # Join StockOnHand with RawMaterial
            .join(Warehouse, TempReceivingReport.warehouse_id == Warehouse.id) # Join Receiving Report with Warehouse
            .filter(
                # Filter for records where is_cleared or is_deleted is NULL or False
                or_(
                    TempReceivingReport.is_cleared.is_(None),  # NULL check for is_cleared
                    TempReceivingReport.is_cleared == False  # False check for is_cleared
                ),
                or_(
                    TempReceivingReport.is_deleted.is_(None),  # NULL check for is_deleted
                    TempReceivingReport.is_deleted == False  # False check for is_deleted
                )
            )
        )

        # Return All the result
        return stmt.all()


        # receiving_report_item = self.db.query(TempReceivingReport).all()
        # if receiving_report_item:
        #     return receiving_report_item
        # return []


    def update_receiving_report(self, receiving_report_id: UUID, receiving_report_update: TempReceivingReportUpdate):

        # Get the ID of the good status
        status_query = text(""" SELECT id FROM tbl_droplist WHERE name = 'good' """)
        status_record = self.db.execute(status_query).fetchone()  # or .fetchall() if expecting multiple rows
        status_result = status_record
        if status_result:
            status_id = status_result[0]

        else:
            print("There is an error with getting the status ID")
            return


        # Check if the record is existing in the SOH
        query = text("""SELECT * FROM view_beginning_soh
                        WHERE warehouseid = :warehouse_id
                              AND rawmaterialid = :rm_code_id
                              AND statusid = :status_id""")



        record = self.db.execute(query, {
            "warehouse_id": receiving_report_update.warehouse_id,
            "rm_code_id": receiving_report_update.rm_code_id,
            "status_id": status_id
        }).fetchone()  # or .fetchall() if expecting multiple rows
        result = record

        # This feature is required for the calculation.
        # Create a SOH record if there is no RM existing
        if not result:
            # Create a new StockOnHand record
            new_stock = StockOnHand(
                rm_code_id=receiving_report_update.rm_code_id,
                warehouse_id=receiving_report_update.warehouse_id,
                rm_soh=0.00,
                status_id=status_id
            )
            self.db.add(new_stock)
            self.db.commit()
            self.db.refresh(new_stock)


        try:
            receiving_report = self.db.query(TempReceivingReport).filter(TempReceivingReport.id == receiving_report_id).first()
            if not receiving_report or receiving_report.is_deleted:
                raise TempReceivingReportNotFoundException(detail="Receiving Report not found or already deleted.")

            for key, value in receiving_report_update.dict(exclude_unset=True).items():
                setattr(receiving_report, key, value)
            self.db.commit()
            self.db.refresh(receiving_report)
            return self.get_receiving_report()

        except Exception as e:
            raise TempReceivingReportUpdateException(detail=f"Error: {str(e)}")

    def soft_delete_receiving_report(self, receiving_report_id: UUID):
        try:
            receiving_report = self.db.query(TempReceivingReport).filter(TempReceivingReport.id == receiving_report_id).first()
            if not receiving_report or receiving_report.is_deleted:
                raise TempReceivingReportNotFoundException(detail="Receiving Report not found or already deleted.")

            receiving_report.is_deleted = True
            self.db.commit()
            self.db.refresh(receiving_report)
            rr_list = self.get_receiving_report()
            return rr_list

        except Exception as e:
            raise TempReceivingReportSoftDeleteException(detail=f"Error: {str(e)}")


    def restore_receiving_report(self, receiving_report_id: UUID):
        try:
            receiving_report = self.db.query(TempReceivingReport).filter(TempReceivingReport.id == receiving_report_id).first()
            if not receiving_report or not receiving_report.is_deleted:
                raise TempReceivingReportNotFoundException(detail="Receiving Report not found or already restored.")

            receiving_report.is_deleted = False
            self.db.commit()
            self.db.refresh(receiving_report)
            return receiving_report

        except Exception as e:
            raise TempReceivingReportRestoreException(detail=f"Error: {str(e)}")


# These are the code for the business logic like calculation etc.
class TempReceivingReportService(AppService):
    def create_receiving_report(self, item: TempReceivingReportCreate):
        try:
            receiving_report_item = TempReceivingReportCRUD(self.db).create_receiving_report(item)

        except Exception as e:
            raise TempReceivingReportCreateException(detail=f"Error: {str(e)}")


        return receiving_report_item

    def get_receiving_report(self):
        try:
            receiving_report_item = TempReceivingReportCRUD(self.db).get_receiving_report()

        except Exception as e:
            raise TempReceivingReportNotFoundException(detail=f"Error: {str(e)}")
        return receiving_report_item

    # This is the service/business logic in updating the receiving_report.
    def update_receiving_report(self, receiving_report_id: UUID, receiving_report_update: TempReceivingReportUpdate):
        receiving_report = TempReceivingReportCRUD(self.db).update_receiving_report(receiving_report_id, receiving_report_update)
        return receiving_report

    # This is the service/business logic in soft deleting the receiving_report.
    def soft_delete_receiving_report(self, receiving_report_id: UUID):
        receiving_report = TempReceivingReportCRUD(self.db).soft_delete_receiving_report(receiving_report_id)
        return receiving_report


    # This is the service/business logic in soft restoring the receiving_report.
    def restore_receiving_report(self, receiving_report_id: UUID):
        receiving_report = TempReceivingReportCRUD(self.db).restore_receiving_report(receiving_report_id)
        return receiving_report





