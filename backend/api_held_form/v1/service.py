from backend.api_held_form.v1.exceptions import HeldFormCreateException, HeldFormNotFoundException, \
    HeldFormUpdateException, HeldFormSoftDeleteException, HeldFormRestoreException
from backend.api_held_form.v1.main import AppCRUD, AppService
from backend.api_held_form.v1.models import HeldForm
from backend.api_held_form.v1.schemas import HeldFormCreate, HeldFormUpdate
from uuid import UUID


# These are the code for the app to communicate to the database
class HeldFormCRUD(AppCRUD):
    def create_held_form(self, held_form: HeldFormCreate):
        held_form_item = HeldForm(rm_code_id=held_form.rm_code_id,
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
        held_form_item = self.db.query(HeldForm).all()
        if held_form_item:
            return held_form_item
        return None


    def update_held_form(self, held_form_id: UUID, held_form_update: HeldFormUpdate):
        try:
            held_form = self.db.query(HeldForm).filter(HeldForm.id == held_form_id).first()
            if not held_form or held_form.is_deleted:
                raise HeldFormNotFoundException(detail="Held Form not found or already deleted.")

            for key, value in held_form_update.dict(exclude_unset=True).items():
                setattr(held_form, key, value)
            self.db.commit()
            self.db.refresh(held_form)
            return held_form

        except Exception as e:
            raise HeldFormUpdateException(detail=f"Error: {str(e)}")

    def soft_delete_held_form(self, held_form_id: UUID):
        try:
            held_form = self.db.query(HeldForm).filter(HeldForm.id == held_form_id).first()
            if not held_form or held_form.is_deleted:
                raise HeldFormNotFoundException(detail="Held Form not found or already deleted.")

            held_form.is_deleted = True
            self.db.commit()
            self.db.refresh(held_form)
            return held_form

        except Exception as e:
            raise HeldFormSoftDeleteException(detail=f"Error: {str(e)}")


    def restore_held_form(self, held_form_id: UUID):
        try:
            held_form = self.db.query(HeldForm).filter(HeldForm.id == held_form_id).first()
            if not held_form or not held_form.is_deleted:
                raise HeldFormNotFoundException(detail="Held Form not found or already restored.")

            held_form.is_deleted = False
            self.db.commit()
            self.db.refresh(held_form)
            return held_form

        except Exception as e:
            raise HeldFormRestoreException(detail=f"Error: {str(e)}")


# These are the code for the business logic like calculation etc.
class HeldFormService(AppService):
    def create_held_form(self, item: HeldFormCreate):
        try:
            held_form_item = HeldFormCRUD(self.db).create_held_form(item)

        except Exception as e:
            raise HeldFormCreateException(detail=f"Error: {str(e)}")


        return held_form_item

    def get_held_form(self):
        try:
            held_form_item = HeldFormCRUD(self.db).get_held_form()

        except Exception as e:
            raise HeldFormNotFoundException(detail=f"Error: {str(e)}")
        return held_form_item

    # This is the service/business logic in updating the held_form.
    def update_held_form(self, held_form_id: UUID, held_form_update: HeldFormUpdate):
        held_form = HeldFormCRUD(self.db).update_held_form(held_form_id, held_form_update)
        return held_form

    # This is the service/business logic in soft deleting the held_form.
    def soft_delete_held_form(self, held_form_id: UUID):
        held_form = HeldFormCRUD(self.db).soft_delete_held_form(held_form_id)
        return held_form


    # This is the service/business logic in soft restoring the held_form.
    def restore_held_form(self, held_form_id: UUID):
        held_form = HeldFormCRUD(self.db).restore_held_form(held_form_id)
        return held_form





