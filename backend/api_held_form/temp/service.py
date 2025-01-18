from backend.api_held_form.temp.exceptions import TempHeldFormCreateException, TempHeldFormNotFoundException, \
    TempHeldFormUpdateException, TempHeldFormSoftDeleteException, TempHeldFormRestoreException
from backend.api_held_form.temp.main import AppCRUD, AppService
from backend.api_held_form.temp.models import TempHeldForm
from backend.api_held_form.temp.schemas import TempHeldFormCreate, TempHeldFormUpdate
from uuid import UUID


# These are the code for the app to communicate to the database
class TempHeldFormCRUD(AppCRUD):
    def create_held_form(self, held_form: TempHeldFormCreate):
        held_form_item = TempHeldForm(rm_code_id=held_form.rm_code_id,
                                                warehouse_id=held_form.warehouse_id,
                                                rm_soh_id=held_form.rm_soh_id,
                                                held_date=held_form.held_date,
                                                qty_kg=held_form.qty_kg,
                                                status_id=held_form.status_id
                                                )
        self.db.add(held_form_item)
        self.db.commit()
        self.db.refresh(held_form_item)
        return held_form_item

    def get_held_form(self):
        held_form_item = self.db.query(TempHeldForm).all()
        if held_form_item:
            return held_form_item
        return []


    def update_held_form(self, held_form_id: UUID, held_form_update: TempHeldFormUpdate):
        try:
            held_form = self.db.query(TempHeldForm).filter(TempHeldForm.id == held_form_id).first()
            if not held_form or held_form.is_deleted:
                raise TempHeldFormNotFoundException(detail="Held Form not found or already deleted.")

            for key, value in held_form_update.dict(exclude_unset=True).items():
                setattr(held_form, key, value)
            self.db.commit()
            self.db.refresh(held_form)
            return held_form

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
            return held_form

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





