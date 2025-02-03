from backend.api_outgoing_report.temp.exceptions import TempOutgoingReportCreateException, TempOutgoingReportNotFoundException, \
    TempOutgoingReportUpdateException, TempOutgoingReportSoftDeleteException, TempOutgoingReportRestoreException
from backend.api_outgoing_report.temp.main import AppCRUD, AppService
from backend.api_outgoing_report.temp.models import TempOutgoingReport
from backend.api_outgoing_report.temp.schemas import TempOutgoingReportCreate, TempOutgoingReportUpdate
from uuid import UUID


# These are the code for the app to communicate to the database
class TempOutgoingReportCRUD(AppCRUD):
    def create_outgoing_report(self, outgoing_report: TempOutgoingReportCreate):
        outgoing_report_item = TempOutgoingReport(rm_code_id=outgoing_report.rm_code_id,
                                                warehouse_id=outgoing_report.warehouse_id,
                                                rm_soh_id=outgoing_report.rm_soh_id,
                                                ref_number=outgoing_report.ref_number,
                                                outgoing_date=outgoing_report.outgoing_date,
                                                qty_kg=outgoing_report.qty_kg
                                                )
        self.db.add(outgoing_report_item)
        self.db.commit()
        self.db.refresh(outgoing_report_item)
        return outgoing_report_item

    def get_outgoing_report(self):
        outgoing_report_item = self.db.query(TempOutgoingReport).all()
        if outgoing_report_item:
            return outgoing_report_item
        return None


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





