from backend.api_transfer_form.temp.exceptions import TempTransferFormCreateException, TempTransferFormNotFoundException, \
    TempTransferFormUpdateException, TempTransferFormSoftDeleteException, TempTransferFormRestoreException
from backend.api_transfer_form.temp.main import AppCRUD, AppService
from backend.api_transfer_form.temp.models import TempTransferForm
from backend.api_transfer_form.temp.schemas import TempTransferFormCreate, TempTransferFormUpdate
from uuid import UUID


# These are the code for the app to communicate to the database
class TempTransferFormCRUD(AppCRUD):
    def create_transfer_form(self, transfer_form: TempTransferFormCreate):
        transfer_form_item = TempTransferForm(rm_code_id=transfer_form.rm_code_id,
                                                from_warehouse_id=transfer_form.from_warehouse_id,
                                                to_warehouse_id=transfer_form.to_warehouse_id,
                                                rm_soh_id=transfer_form.rm_soh_id,
                                                ref_number=transfer_form.ref_number,
                                                transfer_date=transfer_form.transfer_date,
                                                qty_kg=transfer_form.qty_kg
                                                )
        self.db.add(transfer_form_item)
        self.db.commit()
        self.db.refresh(transfer_form_item)
        return transfer_form_item

    def get_transfer_form(self):
        transfer_form_item = self.db.query(TempTransferForm).all()
        if transfer_form_item:
            return transfer_form_item
        return None


    def update_transfer_form(self, transfer_form_id: UUID, transfer_form_update: TempTransferFormUpdate):
        try:
            transfer_form = self.db.query(TempTransferForm).filter(TempTransferForm.id == transfer_form_id).first()
            if not transfer_form or transfer_form.is_deleted:
                raise TempTransferFormNotFoundException(detail="Transfer Form not found or already deleted.")

            for key, value in transfer_form_update.dict(exclude_unset=True).items():
                setattr(transfer_form, key, value)
            self.db.commit()
            self.db.refresh(transfer_form)
            return transfer_form

        except Exception as e:
            raise TempTransferFormUpdateException(detail=f"Error: {str(e)}")

    def soft_delete_transfer_form(self, transfer_form_id: UUID):
        try:
            transfer_form = self.db.query(TempTransferForm).filter(TempTransferForm.id == transfer_form_id).first()
            if not transfer_form or transfer_form.is_deleted:
                raise TempTransferFormNotFoundException(detail="Transfer Form not found or already deleted.")

            transfer_form.is_deleted = True
            self.db.commit()
            self.db.refresh(transfer_form)
            return transfer_form

        except Exception as e:
            raise TempTransferFormSoftDeleteException(detail=f"Error: {str(e)}")


    def restore_transfer_form(self, transfer_form_id: UUID):
        try:
            transfer_form = self.db.query(TempTransferForm).filter(TempTransferForm.id == transfer_form_id).first()
            if not transfer_form or not transfer_form.is_deleted:
                raise TempTransferFormNotFoundException(detail="Transfer Form not found or already restored.")

            transfer_form.is_deleted = False
            self.db.commit()
            self.db.refresh(transfer_form)
            return transfer_form

        except Exception as e:
            raise TempTransferFormRestoreException(detail=f"Error: {str(e)}")


# These are the code for the business logic like calculation etc.
class TempTransferFormService(AppService):
    def create_transfer_form(self, item: TempTransferFormCreate):
        try:
            transfer_form_item = TempTransferFormCRUD(self.db).create_transfer_form(item)

        except Exception as e:
            raise TempTransferFormCreateException(detail=f"Error: {str(e)}")


        return transfer_form_item

    def get_transfer_form(self):
        try:
            transfer_form_item = TempTransferFormCRUD(self.db).get_transfer_form()

        except Exception as e:
            raise TempTransferFormNotFoundException(detail=f"Error: {str(e)}")
        return transfer_form_item

    # This is the service/business logic in updating the transfer_form.
    def update_transfer_form(self, transfer_form_id: UUID, transfer_form_update: TempTransferFormUpdate):
        transfer_form = TempTransferFormCRUD(self.db).update_transfer_form(transfer_form_id, transfer_form_update)
        return transfer_form

    # This is the service/business logic in soft deleting the transfer_form.
    def soft_delete_transfer_form(self, transfer_form_id: UUID):
        transfer_form = TempTransferFormCRUD(self.db).soft_delete_transfer_form(transfer_form_id)
        return transfer_form


    # This is the service/business logic in soft restoring the transfer_form.
    def restore_transfer_form(self, transfer_form_id: UUID):
        transfer_form = TempTransferFormCRUD(self.db).restore_transfer_form(transfer_form_id)
        return transfer_form





