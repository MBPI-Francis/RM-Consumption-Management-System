from backend.api_preparation_form.main.exceptions import PreparationFormCreateException, PreparationFormNotFoundException
from backend.api_preparation_form.main.main import AppCRUD, AppService
from backend.api_preparation_form.main.models import PreparationForm
from backend.api_preparation_form.main.schemas import PreparationFormCreate


# These are the code for the app to communicate to the database
class PreparationFormCRUD(AppCRUD):
    def create_preparation_form(self, preparation_form: PreparationFormCreate):
        preparation_form_item = PreparationForm(rm_code_id=preparation_form.rm_code_id,
                                                warehouse_id=preparation_form.warehouse_id,
                                                rm_soh_id=preparation_form.rm_soh_id,
                                                computed_detail_id=preparation_form.computed_detail_id,
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
        preparation_form_item = self.db.query(PreparationForm).all()
        if preparation_form_item:
            return preparation_form_item
        return []





# These are the code for the business logic like calculation etc.
class PreparationFormService(AppService):
    def create_preparation_form(self, item: PreparationFormCreate):
        try:
            preparation_form_item = PreparationFormCRUD(self.db).create_preparation_form(item)

        except Exception as e:
            raise PreparationFormCreateException(detail=f"Error: {str(e)}")


        return preparation_form_item

    def get_preparation_form(self):
        try:
            preparation_form_item = PreparationFormCRUD(self.db).get_preparation_form()

        except Exception as e:
            raise PreparationFormNotFoundException(detail=f"Error: {str(e)}")
        return preparation_form_item



