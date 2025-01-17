from backend.api_computed_details.v1.exceptions import ComputedDetailCreateException, ComputedDetailNotFoundException
from backend.api_computed_details.v1.main import AppCRUD, AppService
from backend.api_computed_details.v1.models import ComputedDetail
from backend.api_computed_details.v1.schemas import ComputedDetailCreate
from uuid import UUID
from datetime import datetime


# These are the code for the app to communicate to the database
class ComputedDetailCRUD(AppCRUD):
    def create_computed_detail(self, computed_detail: ComputedDetailCreate):
        computed_detail_item = ComputedDetail(computed_by_id=computed_detail.computed_by_id)
        self.db.add(computed_detail_item)
        self.db.commit()
        self.db.refresh(computed_detail_item)
        return computed_detail_item

    def list_computed_detail(self):
        computed_detail_item = self.db.query(ComputedDetail).all()
        if computed_detail_item:
            return computed_detail_item
        return None

    def get_computed_detail(self, computed_date, computed_by_id):
        computed_detail_item = (
            self.db.query(ComputedDetail).filter(
                ComputedDetail.date_computed == computed_date, ComputedDetail.computed_by_id == computed_by_id
            ).first()
        )
        if not computed_detail_item:
            raise ComputedDetailNotFoundException(detail="Computed Details not found.")
        return None



# These are the code for the business logic like calculation etc.
class ComputedDetailService(AppService):
    def create_computed_detail(self, item: ComputedDetailCreate):
        try:
            computed_detail_item = ComputedDetailCRUD(self.db).create_computed_detail(item)

        except Exception as e:
            raise ComputedDetailCreateException(detail=f"Error: {str(e)}")

        return computed_detail_item

    def list_computed_detail(self):
        try:
            computed_detail_item = ComputedDetailCRUD(self.db).list_computed_detail()

        except Exception as e:
            raise ComputedDetailNotFoundException(detail=f"Error: {str(e)}")
        return computed_detail_item


    def get_computed_detail(self, computed_date: datetime, computed_by_id: UUID):
        try:
            computed_detail_item = ComputedDetailCRUD(self.db).get_computed_detail(computed_date, computed_by_id)
        except Exception as e:
            raise ComputedDetailNotFoundException(detail=f"Error: {str(e)}")
        return computed_detail_item


