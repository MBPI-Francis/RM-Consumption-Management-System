from backend.api_outgoing_report.main.exceptions import OutgoingReportCreateException, OutgoingReportNotFoundException
from backend.api_outgoing_report.main.main import AppCRUD, AppService
from backend.api_outgoing_report.main.models import OutgoingReport
from backend.api_outgoing_report.main.schemas import OutgoingReportCreate
from uuid import UUID


# These are the code for the app to communicate to the database
class OutgoingReportCRUD(AppCRUD):
    def create_outgoing_report(self, outgoing_report: OutgoingReportCreate):
        outgoing_report_item = OutgoingReport(rm_code_id=outgoing_report.rm_code_id,
                                                warehouse_id=outgoing_report.warehouse_id,
                                                rm_soh_id=outgoing_report.rm_soh_id,
                                                computed_detail_id=outgoing_report.computed_detail_id,
                                                ref_number=outgoing_report.ref_number,
                                                outgoing_date=outgoing_report.outgoing_date,
                                                qty_kg=outgoing_report.qty_kg
                                                )
        self.db.add(outgoing_report_item)
        self.db.commit()
        self.db.refresh(outgoing_report_item)
        return outgoing_report_item

    def get_outgoing_report(self):
        outgoing_report_item = self.db.query(OutgoingReport).all()
        if outgoing_report_item:
            return outgoing_report_item
        return []



# These are the code for the business logic like calculation etc.
class OutgoingReportService(AppService):
    def create_outgoing_report(self, item: OutgoingReportCreate):
        try:
            outgoing_report_item = OutgoingReportCRUD(self.db).create_outgoing_report(item)

        except Exception as e:
            raise OutgoingReportCreateException(detail=f"Error: {str(e)}")


        return outgoing_report_item

    def get_outgoing_report(self):
        try:
            outgoing_report_item = OutgoingReportCRUD(self.db).get_outgoing_report()

        except Exception as e:
            raise OutgoingReportNotFoundException(detail=f"Error: {str(e)}")
        return outgoing_report_item


