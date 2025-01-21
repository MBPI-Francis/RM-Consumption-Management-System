from backend.api_transfer_form.main.exceptions import TransferFormCreateException, TransferFormNotFoundException
from backend.api_transfer_form.main.main import AppCRUD, AppService
from backend.api_transfer_form.main.models import TransferForm
from backend.api_transfer_form.main.schemas import TransferFormCreate
from uuid import UUID


# These are the code for the app to communicate to the database
class TransferFormCRUD(AppCRUD):
    def create_transfer_form(self, transfer_form: TransferFormCreate):
        transfer_form_item = TransferForm(rm_code_id=transfer_form.rm_code_id,
                                                from_warehouse_id=transfer_form.from_warehouse_id,
                                                to_warehouse_id=transfer_form.to_warehouse_id,
                                                rm_soh_id=transfer_form.rm_soh_id,
                                                computed_detail_id=transfer_form.computed_detail_id,
                                                ref_number=transfer_form.ref_number,
                                                transfer_date=transfer_form.transfer_date,
                                                qty_kg=transfer_form.qty_kg,
                                                status_id=transfer_form.status_id
                                                )
        self.db.add(transfer_form_item)
        self.db.commit()
        self.db.refresh(transfer_form_item)
        return transfer_form_item

    def get_transfer_form(self):
        transfer_form_item = self.db.query(TransferForm).all()
        if transfer_form_item:
            return transfer_form_item
        return []


# These are the code for the business logic like calculation etc.
class TransferFormService(AppService):
    def create_transfer_form(self, item: TransferFormCreate):
        try:
            transfer_form_item = TransferFormCRUD(self.db).create_transfer_form(item)

        except Exception as e:
            raise TransferFormCreateException(detail=f"Error: {str(e)}")


        return transfer_form_item

    def get_transfer_form(self):
        try:
            transfer_form_item = TransferFormCRUD(self.db).get_transfer_form()

        except Exception as e:
            raise TransferFormNotFoundException(detail=f"Error: {str(e)}")
        return transfer_form_item

