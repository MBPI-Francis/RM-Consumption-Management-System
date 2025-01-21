from backend.api_outgoing_report.temp.exceptions import TempOutgoingReportCreateException, TempOutgoingReportNotFoundException, \
    TempOutgoingReportUpdateException, TempOutgoingReportSoftDeleteException, TempOutgoingReportRestoreException
from backend.api_outgoing_report.temp.main import AppCRUD, AppService
from backend.api_outgoing_report.temp.models import TempOutgoingReport
from backend.api_outgoing_report.temp.schemas import TempOutgoingReportCreate, TempOutgoingReportUpdate
from uuid import UUID
from backend.api_raw_materials.v1.models import RawMaterial
from backend.api_warehouses.v1.models import Warehouse
from backend.api_stock_on_hand.v1.models import StockOnHand
from sqlalchemy import desc
from sqlalchemy.sql import func, cast, case
from sqlalchemy.types import String

# These are the code for the app to communicate to the database
class TempOutgoingReportCRUD(AppCRUD):

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
    
    
    def create_outgoing_report(self, outgoing_report: TempOutgoingReportCreate):

        # Get the latest StockOnHand record ID
        latest_soh_record = self.get_latest_soh_record(
            warehouse_id=outgoing_report.warehouse_id,
            rm_code_id=outgoing_report.rm_code_id,
        )
        
        if latest_soh_record:
            latest_soh_record_id = latest_soh_record.id

            outgoing_report_item = TempOutgoingReport(rm_code_id=outgoing_report.rm_code_id,
                                                warehouse_id=outgoing_report.warehouse_id,
                                                rm_soh_id=latest_soh_record_id,
                                                ref_number=outgoing_report.ref_number,
                                                outgoing_date=outgoing_report.outgoing_date,
                                                qty_kg=outgoing_report.qty_kg
                                                )

        else:
            outgoing_report_item = TempOutgoingReport(rm_code_id=outgoing_report.rm_code_id,
                                                warehouse_id=outgoing_report.warehouse_id,
                                                ref_number=outgoing_report.ref_number,
                                                outgoing_date=outgoing_report.outgoing_date,
                                                qty_kg=outgoing_report.qty_kg
                                                )


        self.db.add(outgoing_report_item)
        self.db.commit()
        self.db.refresh(outgoing_report_item)
        # return self.get_outgoing_report()
        return outgoing_report_item

    def get_outgoing_report(self):
        """
             Join StockOnHand, OutgoingReport, Warehouse, and RawMaterial tables.
             """
        # Join tables
        stmt = (
            self.db.query(
                RawMaterial.rm_code.label("raw_material"),
                TempOutgoingReport.qty_kg,
                TempOutgoingReport.ref_number,
                Warehouse.wh_name,
                TempOutgoingReport.outgoing_date,
                TempOutgoingReport.created_at,
                case(
                    (StockOnHand.id == None, "No Beginning Balance"),  # If no StockOnHand record, show "No Balance"
                    else_=func.concat(
                        cast(StockOnHand.rm_soh, String),
                        "(kg) - ",
                        func.to_char(StockOnHand.stock_change_date, "MM/DD/YYYY")
                    )
                ).label("soh_and_date"),
                TempOutgoingReport.created_at,
                TempOutgoingReport.updated_at

            )
            .outerjoin(StockOnHand,
                       StockOnHand.id == TempOutgoingReport.rm_soh_id)  # Left join StockOnHand with ReceivingReport
            .join(RawMaterial, TempOutgoingReport.rm_code_id == RawMaterial.id)  # Join TempOutgoingReport with RawMaterial
            .join(Warehouse, TempOutgoingReport.warehouse_id == Warehouse.id)  # Join TempOutgoingReport with Warehouse
        )

        # Return All the result
        return stmt.all()

    def update_outgoing_report(self, outgoing_report_id: UUID, outgoing_report_update: TempOutgoingReportUpdate):
        try:
            outgoing_report = self.db.query(TempOutgoingReport).filter(TempOutgoingReport.id == outgoing_report_id).first()
            if not outgoing_report or outgoing_report.is_deleted:
                raise TempOutgoingReportNotFoundException(detail="Outgoing Report not found or already deleted.")

            for key, value in outgoing_report_update.dict(exclude_unset=True).items():
                setattr(outgoing_report, key, value)
            self.db.commit()
            self.db.refresh(outgoing_report)
            return outgoing_report

        except Exception as e:
            raise TempOutgoingReportUpdateException(detail=f"Error: {str(e)}")

    def soft_delete_outgoing_report(self, outgoing_report_id: UUID):
        try:
            outgoing_report = self.db.query(TempOutgoingReport).filter(TempOutgoingReport.id == outgoing_report_id).first()
            if not outgoing_report or outgoing_report.is_deleted:
                raise TempOutgoingReportNotFoundException(detail="Outgoing Report not found or already deleted.")

            outgoing_report.is_deleted = True
            self.db.commit()
            self.db.refresh(outgoing_report)
            return outgoing_report

        except Exception as e:
            raise TempOutgoingReportSoftDeleteException(detail=f"Error: {str(e)}")


    def restore_outgoing_report(self, outgoing_report_id: UUID):
        try:
            outgoing_report = self.db.query(TempOutgoingReport).filter(TempOutgoingReport.id == outgoing_report_id).first()
            if not outgoing_report or not outgoing_report.is_deleted:
                raise TempOutgoingReportNotFoundException(detail="Outgoing Report not found or already restored.")

            outgoing_report.is_deleted = False
            self.db.commit()
            self.db.refresh(outgoing_report)
            return outgoing_report

        except Exception as e:
            raise TempOutgoingReportRestoreException(detail=f"Error: {str(e)}")


# These are the code for the business logic like calculation etc.
class TempOutgoingReportService(AppService):
    def create_outgoing_report(self, item: TempOutgoingReportCreate):
        try:
            outgoing_report_item = TempOutgoingReportCRUD(self.db).create_outgoing_report(item)

        except Exception as e:
            raise TempOutgoingReportCreateException(detail=f"Error: {str(e)}")


        return outgoing_report_item

    def get_outgoing_report(self):
        try:
            outgoing_report_item = TempOutgoingReportCRUD(self.db).get_outgoing_report()

        except Exception as e:
            raise TempOutgoingReportNotFoundException(detail=f"Error: {str(e)}")
        return outgoing_report_item

    # This is the service/business logic in updating the outgoing_report.
    def update_outgoing_report(self, outgoing_report_id: UUID, outgoing_report_update: TempOutgoingReportUpdate):
        outgoing_report = TempOutgoingReportCRUD(self.db).update_outgoing_report(outgoing_report_id, outgoing_report_update)
        return outgoing_report

    # This is the service/business logic in soft deleting the outgoing_report.
    def soft_delete_outgoing_report(self, outgoing_report_id: UUID):
        outgoing_report = TempOutgoingReportCRUD(self.db).soft_delete_outgoing_report(outgoing_report_id)
        return outgoing_report


    # This is the service/business logic in soft restoring the outgoing_report.
    def restore_outgoing_report(self, outgoing_report_id: UUID):
        outgoing_report = TempOutgoingReportCRUD(self.db).restore_outgoing_report(outgoing_report_id)
        return outgoing_report





