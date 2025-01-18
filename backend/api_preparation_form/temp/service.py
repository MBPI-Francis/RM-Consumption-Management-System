from backend.api_preparation_form.temp.exceptions import TempPreparationFormCreateException, TempPreparationFormNotFoundException, \
    TempPreparationFormUpdateException, TempPreparationFormSoftDeleteException, TempPreparationFormRestoreException
from backend.api_preparation_form.temp.main import AppCRUD, AppService
from backend.api_preparation_form.temp.models import TempPreparationForm
from backend.api_preparation_form.temp.schemas import TempPreparationFormCreate, TempPreparationFormUpdate
from uuid import UUID


# These are the code for the app to communicate to the database
class TempPreparationFormCRUD(AppCRUD):
    def create_preparation_form(self, preparation_form: TempPreparationFormCreate):
        preparation_form_item = TempPreparationForm(rm_code_id=preparation_form.rm_code_id,
                                                warehouse_id=preparation_form.warehouse_id,
                                                rm_soh_id=preparation_form.rm_soh_id,
                                                ref_number=preparation_form.ref_number,
                                                preparation_date=preparation_form.preparation_date,
                                                qty_prepared=preparation_form.qty_prepared,
                                                qty_return=preparation_form.qty_return
                                                )
        self.db.add(preparation_form_item)
        self.db.commit()
        self.db.refresh(preparation_form_item)
        return preparation_form_item

    def get_preparation_form(self):
        preparation_form_item = self.db.query(TempPreparationForm).all()
        if preparation_form_item:
            return preparation_form_item
        return []


    def update_preparation_form(self, preparation_form_id: UUID, preparation_form_update: TempPreparationFormUpdate):
        try:
            preparation_form = self.db.query(TempPreparationForm).filter(TempPreparationForm.id == preparation_form_id).first()
            if not preparation_form or preparation_form.is_deleted:
                raise TempPreparationFormNotFoundException(detail="Preparation Form not found or already deleted.")

            for key, value in preparation_form_update.dict(exclude_unset=True).items():
                setattr(preparation_form, key, value)
            self.db.commit()
            self.db.refresh(preparation_form)
            return preparation_form

        except Exception as e:
            raise TempPreparationFormUpdateException(detail=f"Error: {str(e)}")

    def soft_delete_preparation_form(self, preparation_form_id: UUID):
        try:
            preparation_form = self.db.query(TempPreparationForm).filter(TempPreparationForm.id == preparation_form_id).first()
            if not preparation_form or preparation_form.is_deleted:
                raise TempPreparationFormNotFoundException(detail="Preparation Form not found or already deleted.")

            preparation_form.is_deleted = True
            self.db.commit()
            self.db.refresh(preparation_form)
            return preparation_form

        except Exception as e:
            raise TempPreparationFormSoftDeleteException(detail=f"Error: {str(e)}")


    def restore_preparation_form(self, preparation_form_id: UUID):
        try:
            preparation_form = self.db.query(TempPreparationForm).filter(TempPreparationForm.id == preparation_form_id).first()
            if not preparation_form or not preparation_form.is_deleted:
                raise TempPreparationFormNotFoundException(detail="Preparation Form not found or already restored.")

            preparation_form.is_deleted = False
            self.db.commit()
            self.db.refresh(preparation_form)
            return preparation_form

        except Exception as e:
            raise TempPreparationFormRestoreException(detail=f"Error: {str(e)}")


# These are the code for the business logic like calculation etc.
class TempPreparationFormService(AppService):
    def create_preparation_form(self, item: TempPreparationFormCreate):
        try:
            preparation_form_item = TempPreparationFormCRUD(self.db).create_preparation_form(item)

        except Exception as e:
            raise TempPreparationFormCreateException(detail=f"Error: {str(e)}")


        return preparation_form_item

    def get_preparation_form(self):
        try:
            preparation_form_item = TempPreparationFormCRUD(self.db).get_preparation_form()

        except Exception as e:
            raise TempPreparationFormNotFoundException(detail=f"Error: {str(e)}")
        return preparation_form_item

    # This is the service/business logic in updating the preparation_form.
    def update_preparation_form(self, preparation_form_id: UUID, preparation_form_update: TempPreparationFormUpdate):
        preparation_form = TempPreparationFormCRUD(self.db).update_preparation_form(preparation_form_id, preparation_form_update)
        return preparation_form

    # This is the service/business logic in soft deleting the preparation_form.
    def soft_delete_preparation_form(self, preparation_form_id: UUID):
        preparation_form = TempPreparationFormCRUD(self.db).soft_delete_preparation_form(preparation_form_id)
        return preparation_form


    # This is the service/business logic in soft restoring the preparation_form.
    def restore_preparation_form(self, preparation_form_id: UUID):
        preparation_form = TempPreparationFormCRUD(self.db).restore_preparation_form(preparation_form_id)
        return preparation_form





