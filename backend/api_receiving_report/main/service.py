from backend.api_receiving_report.main.exceptions import ReceivingReportCreateException, ReceivingReportNotFoundException
from backend.api_receiving_report.main.main import AppCRUD, AppService
from backend.api_receiving_report.main.models import ReceivingReport
from backend.api_receiving_report.main.schemas import ReceivingReportCreate

# These are the code for the app to communicate to the database
class ReceivingReportCRUD(AppCRUD):
    def create_receiving_report(self, receiving_report: ReceivingReportCreate):
        receiving_report_item = ReceivingReport(rm_code_id=receiving_report.rm_code_id,
                                                warehouse_id=receiving_report.warehouse_id,
                                                rm_soh_id=receiving_report.rm_soh_id,
                                                computed_detail_id=receiving_report.computed_detail_id,
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
        return []



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




