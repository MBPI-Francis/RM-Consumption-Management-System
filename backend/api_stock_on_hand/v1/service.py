from backend.api_stock_on_hand.v1.exceptions import StockOnHandCreateException, StockOnHandNotFoundException, \
    StockOnHandUpdateException, StockOnHandSoftDeleteException, StockOnHandRestoreException
from backend.api_stock_on_hand.v1.main import AppCRUD, AppService
from backend.api_stock_on_hand.v1.models import StockOnHand
from backend.api_stock_on_hand.v1.schemas import StockOnHandCreate, StockOnHandUpdate
from uuid import UUID
from backend.api_receiving_report.temp.service import TempReceivingReportCRUD
from sqlalchemy import desc

# These are the code for the app to communicate to the database
class StockOnHandCRUD(AppCRUD):

    def create_rm_soh(self, rm_soh: StockOnHandCreate):
        rm_soh_item = StockOnHand(rm_code_id=rm_soh.rm_code_id,
                                  warehouse_id=rm_soh.warehouse_id,
                                  rm_soh=rm_soh.rm_soh,
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





