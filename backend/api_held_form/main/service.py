from backend.api_held_form.main.exceptions import HeldFormCreateException, HeldFormNotFoundException
from backend.api_held_form.main.main import AppCRUD, AppService
from backend.api_held_form.main.models import HeldForm
from backend.api_held_form.main.schemas import HeldFormCreate


# These are the code for the app to communicate to the database
class HeldFormCRUD(AppCRUD):
    def create_held_form(self, held_form: HeldFormCreate):
        held_form_item = HeldForm(rm_code_id=held_form.rm_code_id,
                                    warehouse_id=held_form.warehouse_id,
                                    rm_soh_id=held_form.rm_soh_id,
                                    held_date=held_form.held_date,
                                    qty_kg=held_form.qty_kg,
                                    status_id=held_form.status_id,
                                    computed_detail_id=held_form.computed_detail_id
                                )
        self.db.add(held_form_item)
        self.db.commit()
        self.db.refresh(held_form_item)
        return held_form_item

    def get_held_form(self):
        held_form_item = self.db.query(HeldForm).all()
        if held_form_item:
            return held_form_item
        return []


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

