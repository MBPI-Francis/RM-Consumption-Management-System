from backend.api_outgoing_report.v1.exceptions import ReceivingReportCreateException, ReceivingReportNotFoundException, \
    ReceivingReportUpdateException, ReceivingReportSoftDeleteException, ReceivingReportRestoreException
from backend.api_outgoing_report.v1.main import AppCRUD, AppService
from backend.api_outgoing_report.v1.models import ReceivingReport
from backend.api_outgoing_report.v1.schemas import ReceivingReportCreate, ReceivingReportUpdate
from uuid import UUID


# These are the code for the app to communicate to the database
class ReceivingReportCRUD(AppCRUD):
    def create_receiving_report(self, receiving_report: ReceivingReportCreate):
        receiving_report_item = ReceivingReport(rm_code_id=receiving_report.rm_code_id,
                                                warehouse_id=receiving_report.warehouse_id,
                                                rm_soh_id=receiving_report.rm_soh_id,
                                                ref_number=receiving_report.ref_number,
                                                receiving_date=receiving_report.receiving_date,
                                                qty_kg=receiving_report.qty_kg
                                                )
        self.db.add(receiving_report_item)
        self.db.commit()
        self.db.refresh(receiving_report_item)
        return receiving_report_item

    def get_receiving_report(self):
        receiving_report_item = self.db.query(ReceivingReport).all()
        if receiving_report_item:
            return receiving_report_item
        return None


    def update_receiving_report(self, receiving_report_id: UUID, receiving_report_update: ReceivingReportUpdate):
        try:
            receiving_report = self.db.query(ReceivingReport).filter(ReceivingReport.id == receiving_report_id).first()
            if not receiving_report or receiving_report.is_deleted:
                raise ReceivingReportNotFoundException(detail="Receiving Report not found or already deleted.")

            for key, value in receiving_report_update.dict(exclude_unset=True).items():
                setattr(receiving_report, key, value)
            self.db.commit()
            self.db.refresh(receiving_report)
            return receiving_report

        except Exception as e:
            raise ReceivingReportUpdateException(detail=f"Error: {str(e)}")

    def soft_delete_receiving_report(self, receiving_report_id: UUID):
        try:
            receiving_report = self.db.query(ReceivingReport).filter(ReceivingReport.id == receiving_report_id).first()
            if not receiving_report or receiving_report.is_deleted:
                raise ReceivingReportNotFoundException(detail="Receiving Report not found or already deleted.")

            receiving_report.is_deleted = True
            self.db.commit()
            self.db.refresh(receiving_report)
            return receiving_report

        except Exception as e:
            raise ReceivingReportSoftDeleteException(detail=f"Error: {str(e)}")


    def restore_receiving_report(self, receiving_report_id: UUID):
        try:
            receiving_report = self.db.query(ReceivingReport).filter(ReceivingReport.id == receiving_report_id).first()
            if not receiving_report or not receiving_report.is_deleted:
                raise ReceivingReportNotFoundException(detail="Receiving Report not found or already restored.")

            receiving_report.is_deleted = False
            self.db.commit()
            self.db.refresh(receiving_report)
            return receiving_report

        except Exception as e:
            raise ReceivingReportRestoreException(detail=f"Error: {str(e)}")


# These are the code for the business logic like calculation etc.
class ReceivingReportService(AppService):
    def create_receiving_report(self, item: ReceivingReportCreate):
        try:
            receiving_report_item = ReceivingReportCRUD(self.db).create_receiving_report(item)

        except Exception as e:
            raise ReceivingReportCreateException(detail=f"Error: {str(e)}")


        return receiving_report_item

    def get_receiving_report(self):
        try:
            receiving_report_item = ReceivingReportCRUD(self.db).get_receiving_report()

        except Exception as e:
            raise ReceivingReportNotFoundException(detail=f"Error: {str(e)}")
        return receiving_report_item

    # This is the service/business logic in updating the receiving_report.
    def update_receiving_report(self, receiving_report_id: UUID, receiving_report_update: ReceivingReportUpdate):
        receiving_report = ReceivingReportCRUD(self.db).update_receiving_report(receiving_report_id, receiving_report_update)
        return receiving_report

    # This is the service/business logic in soft deleting the receiving_report.
    def soft_delete_receiving_report(self, receiving_report_id: UUID):
        receiving_report = ReceivingReportCRUD(self.db).soft_delete_receiving_report(receiving_report_id)
        return receiving_report


    # This is the service/business logic in soft restoring the receiving_report.
    def restore_receiving_report(self, receiving_report_id: UUID):
        receiving_report = ReceivingReportCRUD(self.db).restore_receiving_report(receiving_report_id)
        return receiving_report





