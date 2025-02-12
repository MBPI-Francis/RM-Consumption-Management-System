from backend.api_held_form.temp.exceptions import TempHeldFormCreateException, TempHeldFormNotFoundException, \
    TempHeldFormUpdateException, TempHeldFormSoftDeleteException, TempHeldFormRestoreException
from backend.api_held_form.temp.main import AppCRUD, AppService
from backend.api_held_form.temp.models import TempHeldForm
from backend.api_held_form.temp.schemas import TempHeldFormCreate, TempHeldFormUpdate
from uuid import UUID
from backend.api_raw_materials.v1.models import RawMaterial
from backend.api_warehouses.v1.models import Warehouse
from backend.api_stock_on_hand.v1.models import StockOnHand
from backend.api_droplist.v1.models import DropList
from sqlalchemy import desc, or_
from sqlalchemy.orm import aliased
from sqlalchemy import text

# These are the code for the app to communicate to the database
class TempHeldFormCRUD(AppCRUD):

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




    def create_held_form(self, held_form: TempHeldFormCreate):
        
        
        # Check if the status id is null
        query = text("""SELECT * FROM view_beginning_soh
                        WHERE warehouseid = :warehouse_id
                              AND rawmaterialid = :rm_code_id
                              AND statusid = :status_id""")



        record = self.db.execute(query, {
            "warehouse_id": held_form.warehouse_id,
            "rm_code_id": held_form.rm_code_id,
            "status_id": held_form.new_status_id
        }).fetchone()  # or .fetchall() if expecting multiple rows
        result = record

        # This feature is required for the calculation
        if not result:
            # Create a new StockOnHand record
            new_stock = StockOnHand(
                rm_code_id=held_form.rm_code_id,
                warehouse_id=held_form.warehouse_id,
                rm_soh=0.00,
                status_id=held_form.new_status_id
            )
            self.db.add(new_stock)
            self.db.commit()
            self.db.refresh(new_stock)
        
        # Get the latest StockOnHand record ID
        latest_soh_record = self.get_latest_soh_record(
            warehouse_id=held_form.warehouse_id,
            rm_code_id=held_form.rm_code_id,
        )

        if latest_soh_record:
            latest_soh_record_id = latest_soh_record.id

            held_form_item = TempHeldForm(rm_code_id=held_form.rm_code_id,
                                                warehouse_id=held_form.warehouse_id,
                                                ref_number=held_form.ref_number,
                                                rm_soh_id=latest_soh_record_id,
                                                change_status_date=held_form.change_status_date,
                                                qty_kg=held_form.qty_kg,
                                                current_status_id=held_form.current_status_id,
                                                new_status_id=held_form.new_status_id
                                                    )

        else:
            held_form_item = TempHeldForm(rm_code_id=held_form.rm_code_id,
                                                warehouse_id=held_form.warehouse_id,
                                                ref_number=held_form.ref_number,
                                                change_status_date=held_form.change_status_date,
                                                qty_kg=held_form.qty_kg,
                                                current_status_id=held_form.current_status_id,
                                                new_status_id=held_form.new_status_id
                                                    )
        self.db.add(held_form_item)
        self.db.commit()
        self.db.refresh(held_form_item)
        return held_form_item

    def get_held_form(self):

        """
             Join StockOnHand, TempHeldForm, Warehouse, and RawMaterial tables.
             """

        # Create aliases for the Warehouse model
        CurrentStatus = aliased(DropList, name="current_status")
        NewStatus = aliased(DropList, name="new_status")


        # Join tables
        stmt = (
            self.db.query(
                TempHeldForm.id,
                RawMaterial.rm_code.label("raw_material"),
                TempHeldForm.qty_kg,
                TempHeldForm.ref_number,
                Warehouse.wh_name,
                CurrentStatus.name.label("current_status"),
                NewStatus.name.label("new_status"),
                TempHeldForm.change_status_date,
                TempHeldForm.created_at,
                TempHeldForm.updated_at

            )
            .outerjoin(StockOnHand,
                       StockOnHand.id == TempHeldForm.rm_soh_id)  # Left join StockOnHand with ReceivingReport
            .join(RawMaterial, TempHeldForm.rm_code_id == RawMaterial.id)  # Join TempHeldForm with RawMaterial
            .join(Warehouse, TempHeldForm.warehouse_id == Warehouse.id)  # Join TempHeldForm with Warehouse
            .join(CurrentStatus, TempHeldForm.current_status_id == CurrentStatus.id)  # Join TempHeldForm with CurrentStatus
            .join(NewStatus, TempHeldForm.new_status_id == NewStatus.id)  # Join TempHeldForm with NewStatus
            .filter(
                # Filter for records where is_cleared or is_deleted is NULL or False
                or_(
                    TempHeldForm.is_cleared.is_(None),  # NULL check for is_cleared
                    TempHeldForm.is_cleared == False  # False check for is_cleared
                ),
                or_(
                    TempHeldForm.is_deleted.is_(None),  # NULL check for is_deleted
                    TempHeldForm.is_deleted == False  # False check for is_deleted
                )
            )

        )

        if stmt.all():
            # Return All the result
            return stmt.all()

        else:
            return []







        # held_form_item = self.db.query(TempHeldForm).all()
        # if held_form_item:
        #     return held_form_item
        # return []


    def update_held_form(self, held_form_id: UUID, held_form_update: TempHeldFormUpdate):
        try:
            held_form = self.db.query(TempHeldForm).filter(TempHeldForm.id == held_form_id).first()
            if not held_form or held_form.is_deleted:
                raise TempHeldFormNotFoundException(detail="Held Form not found or already deleted.")

            for key, value in held_form_update.dict(exclude_unset=True).items():
                setattr(held_form, key, value)
            self.db.commit()
            self.db.refresh(held_form)
            return self.get_held_form()

        except Exception as e:
            raise TempHeldFormUpdateException(detail=f"Error: {str(e)}")

    def soft_delete_held_form(self, held_form_id: UUID):
        try:
            held_form = self.db.query(TempHeldForm).filter(TempHeldForm.id == held_form_id).first()
            if not held_form or held_form.is_deleted:
                raise TempHeldFormNotFoundException(detail="Held Form not found or already deleted.")

            held_form.is_deleted = True
            self.db.commit()
            self.db.refresh(held_form)
            return self.get_held_form()

        except Exception as e:
            raise TempHeldFormSoftDeleteException(detail=f"Error: {str(e)}")


    def restore_held_form(self, held_form_id: UUID):
        try:
            held_form = self.db.query(TempHeldForm).filter(TempHeldForm.id == held_form_id).first()
            if not held_form or not held_form.is_deleted:
                raise TempHeldFormNotFoundException(detail="Held Form not found or already restored.")

            held_form.is_deleted = False
            self.db.commit()
            self.db.refresh(held_form)
            return held_form

        except Exception as e:
            raise TempHeldFormRestoreException(detail=f"Error: {str(e)}")


# These are the code for the business logic like calculation etc.
class TempHeldFormService(AppService):
    def create_held_form(self, item: TempHeldFormCreate):
        try:
            held_form_item = TempHeldFormCRUD(self.db).create_held_form(item)

        except Exception as e:
            raise TempHeldFormCreateException(detail=f"Error: {str(e)}")


        return held_form_item

    def get_held_form(self):
        try:
            held_form_item = TempHeldFormCRUD(self.db).get_held_form()

        except Exception as e:
            raise TempHeldFormNotFoundException(detail=f"Error: {str(e)}")
        return held_form_item

    # This is the service/business logic in updating the held_form.
    def update_held_form(self, held_form_id: UUID, held_form_update: TempHeldFormUpdate):
        held_form = TempHeldFormCRUD(self.db).update_held_form(held_form_id, held_form_update)
        return held_form

    # This is the service/business logic in soft deleting the held_form.
    def soft_delete_held_form(self, held_form_id: UUID):
        held_form = TempHeldFormCRUD(self.db).soft_delete_held_form(held_form_id)
        return held_form


    # This is the service/business logic in soft restoring the held_form.
    def restore_held_form(self, held_form_id: UUID):
        held_form = TempHeldFormCRUD(self.db).restore_held_form(held_form_id)
        return held_form





