from backend.api_receiving_report.temp.exceptions import TempReceivingReportCreateException, TempReceivingReportNotFoundException, \
    TempReceivingReportUpdateException, TempReceivingReportSoftDeleteException, TempReceivingReportRestoreException
from backend.api_receiving_report.temp.main import AppCRUD, AppService
from backend.api_receiving_report.temp.models import TempReceivingReport
from backend.api_receiving_report.temp.schemas import TempReceivingReportCreate, TempReceivingReportUpdate
from uuid import UUID


# These are the code for the app to communicate to the database
class TempReceivingReportCRUD(AppCRUD):
    def create_receiving_report(self, receiving_report: TempReceivingReportCreate):
        receiving_report_item = TempReceivingReport(rm_code_id=receiving_report.rm_code_id,
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
        receiving_report_item = self.db.query(TempReceivingReport).all()
        if receiving_report_item:
            return receiving_report_item
        return None


    def update_receiving_report(self, receiving_report_id: UUID, receiving_report_update: TempReceivingReportUpdate):
        try:
            receiving_report = self.db.query(TempReceivingReport).filter(TempReceivingReport.id == receiving_report_id).first()
            if not receiving_report or receiving_report.is_deleted:
                raise TempReceivingReportNotFoundException(detail="Receiving Report not found or already deleted.")

            for key, value in receiving_report_update.dict(exclude_unset=True).items():
                setattr(receiving_report, key, value)
            self.db.commit()
            self.db.refresh(receiving_report)
            return receiving_report

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
            return receiving_report

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





