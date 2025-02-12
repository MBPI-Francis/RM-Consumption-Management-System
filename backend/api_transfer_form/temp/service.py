from backend.api_transfer_form.temp.exceptions import TempTransferFormCreateException, TempTransferFormNotFoundException, \
    TempTransferFormUpdateException, TempTransferFormSoftDeleteException, TempTransferFormRestoreException
from backend.api_transfer_form.temp.main import AppCRUD, AppService
from backend.api_transfer_form.temp.models import TempTransferForm
from backend.api_transfer_form.temp.schemas import TempTransferFormCreate, TempTransferFormUpdate
from backend.api_raw_materials.v1.models import RawMaterial
from backend.api_warehouses.v1.models import Warehouse
from backend.api_stock_on_hand.v1.models import StockOnHand
from backend.api_droplist.v1.models import DropList
from uuid import UUID
from sqlalchemy import text
from sqlalchemy.future import select

from sqlalchemy import desc, or_
from sqlalchemy.sql import func, cast, case
from sqlalchemy.types import String
from sqlalchemy.orm import aliased

# These are the code for the app to communicate to the database
class TempTransferFormCRUD(AppCRUD):

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


    def create_transfer_form(self, transfer_form: TempTransferFormCreate):

        # Check if the status id is null
        query = text("""SELECT * FROM view_beginning_soh
                        WHERE warehouseid = :warehouse_id
                              AND rawmaterialid = :rm_code_id
                              AND statusid = :status_id""")

        record = self.db.execute(query, {
            "warehouse_id": transfer_form.to_warehouse_id,
            "rm_code_id": transfer_form.rm_code_id,
            "status_id": transfer_form.status_id
        }).fetchone()  # or .fetchall() if expecting multiple rows
        result = record

        # This feature is required for the calculation
        if not result:
            # Create a new StockOnHand record
            new_stock = StockOnHand(
                rm_code_id=transfer_form.rm_code_id,
                warehouse_id=transfer_form.to_warehouse_id,
                rm_soh=0.00,
                status_id=transfer_form.status_id
            )
            self.db.add(new_stock)
            self.db.commit()
            self.db.refresh(new_stock)
            print('NAKAPAG CREATE KA NG RECORD PARE KO ', new_stock)

        # Get the latest StockOnHand record ID
        latest_soh_from = self.get_latest_soh_record(
            warehouse_id=transfer_form.from_warehouse_id,
            rm_code_id=transfer_form.rm_code_id,
        )

        latest_soh_to = self.get_latest_soh_record(
            warehouse_id=transfer_form.to_warehouse_id,
            rm_code_id=transfer_form.rm_code_id,
        )


        if latest_soh_from and latest_soh_to:
            transfer_form_item = TempTransferForm(rm_code_id=transfer_form.rm_code_id,
                                                    from_warehouse_id=transfer_form.from_warehouse_id,
                                                    to_warehouse_id=transfer_form.to_warehouse_id,
                                                    from_rm_soh_id=latest_soh_from.id,
                                                    to_rm_soh_id=latest_soh_to.id,
                                                    ref_number=transfer_form.ref_number,
                                                    transfer_date=transfer_form.transfer_date,
                                                    qty_kg=transfer_form.qty_kg,
                                                    status_id=transfer_form.status_id
                                                  )


        elif not latest_soh_from and latest_soh_to:
            transfer_form_item = TempTransferForm(rm_code_id=transfer_form.rm_code_id,
                                                    from_warehouse_id=transfer_form.from_warehouse_id,
                                                    to_warehouse_id=transfer_form.to_warehouse_id,
                                                    to_rm_soh_id=latest_soh_to.id,
                                                    ref_number=transfer_form.ref_number,
                                                    transfer_date=transfer_form.transfer_date,
                                                    qty_kg=transfer_form.qty_kg,
                                                    status_id = transfer_form.status_id
                                                    )

        elif latest_soh_from and not latest_soh_to:
            transfer_form_item = TempTransferForm(rm_code_id=transfer_form.rm_code_id,
                                                    from_warehouse_id=transfer_form.from_warehouse_id,
                                                    to_warehouse_id=transfer_form.to_warehouse_id,
                                                    from_rm_soh_id=latest_soh_from.id,
                                                    ref_number=transfer_form.ref_number,
                                                    transfer_date=transfer_form.transfer_date,
                                                    qty_kg=transfer_form.qty_kg,
                                                    status_id=transfer_form.status_id
                                                    )


        elif not latest_soh_from and not latest_soh_to:
            transfer_form_item = TempTransferForm(rm_code_id=transfer_form.rm_code_id,
                                                    from_warehouse_id=transfer_form.from_warehouse_id,
                                                    to_warehouse_id=transfer_form.to_warehouse_id,
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

        # Create aliases for the Warehouse model
        FromWarehouse = aliased(Warehouse, name="from_warehouse")
        ToWarehouse = aliased(Warehouse, name="to_warehouse")

        FromStockOnHand = aliased(StockOnHand, name="from_soh")
        ToStockOnHand = aliased(StockOnHand, name="to_soh")
        """
        Join StockOnHand, TransferForm, Warehouse, and RawMaterial tables.
        """
        stmt = (
            self.db.query(
                TempTransferForm.id,
                RawMaterial.rm_code.label("raw_material"),
                TempTransferForm.qty_kg,
                TempTransferForm.ref_number,
                FromWarehouse.wh_name.label("from_warehouse"),
                ToWarehouse.wh_name.label("to_warehouse"),
                TempTransferForm.transfer_date,
                DropList.name.label("status"),
                TempTransferForm.created_at,
                TempTransferForm.updated_at
            )
            .outerjoin(FromStockOnHand,
                       FromStockOnHand.id == TempTransferForm.from_rm_soh_id)  # Left join StockOnHand with TransferForm
            .outerjoin(ToStockOnHand,
                       ToStockOnHand.id == TempTransferForm.to_rm_soh_id)  # Left join StockOnHand with TransferForm
            .outerjoin(DropList, DropList.id == TempTransferForm.status_id)  # Left join DropList with TransferForm
            .join(RawMaterial, TempTransferForm.rm_code_id == RawMaterial.id)  # Join StockOnHand with RawMaterial
            .join(FromWarehouse,
                  TempTransferForm.from_warehouse_id == FromWarehouse.id)  # Join TempTransferForm with Warehouse
            .join(ToWarehouse,
                  TempTransferForm.to_warehouse_id == ToWarehouse.id)  # Join TempTransferForm with Warehouse
            .filter(
                # Filter for records where is_cleared or is_deleted is NULL or False
                or_(
                    TempTransferForm.is_cleared.is_(None),  # NULL check for is_cleared
                    TempTransferForm.is_cleared == False # False check for is_cleared
                ),
                or_(
                    TempTransferForm.is_deleted.is_(None),  # NULL check for is_deleted
                    TempTransferForm.is_deleted == False  # False check for is_deleted
                )
            )
        )

        # Return filtered results
        return stmt.all()


    def update_transfer_form(self, transfer_form_id: UUID, transfer_form_update: TempTransferFormUpdate):
        try:
            transfer_form = self.db.query(TempTransferForm).filter(TempTransferForm.id == transfer_form_id).first()
            if not transfer_form or transfer_form.is_deleted:
                raise TempTransferFormNotFoundException(detail="Transfer Form not found or already deleted.")

            for key, value in transfer_form_update.dict(exclude_unset=True).items():
                setattr(transfer_form, key, value)
            self.db.commit()
            self.db.refresh(transfer_form)
            return self.get_transfer_form()

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
            return self.get_transfer_form()

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





