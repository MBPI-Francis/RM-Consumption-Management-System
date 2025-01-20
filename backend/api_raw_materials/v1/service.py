from backend.api_raw_materials.v1.exceptions import RawMaterialCreateException, RawMaterialNotFoundException, \
    RawMaterialUpdateException, RawMaterialSoftDeleteException, RawMaterialRestoreException
from backend.api_raw_materials.v1.main import AppCRUD, AppService
from backend.api_raw_materials.v1.models import RawMaterial
from backend.api_raw_materials.v1.schemas import RawMaterialCreate, RawMaterialUpdate
from uuid import UUID


# These are the code for the app to communicate to the database
class RawMaterialCRUD(AppCRUD):
    def create_raw_material(self, raw_material: RawMaterialCreate):
        raw_material_item = RawMaterial(rm_code=raw_material.rm_code,
                                   description=raw_material.description,
                                   rm_name=raw_material.rm_name,
                                   updated_by_id=raw_material.updated_by_id,
                                   created_by_id=raw_material.created_by_id)
        self.db.add(raw_material_item)
        self.db.commit()
        self.db.refresh(raw_material_item)
        return raw_material_item

    def all_raw_material(self):
        raw_material_item = self.db.query(RawMaterial).all()
        if raw_material_item:
            return raw_material_item
        return []
    
    
    def get_raw_material(self, rm_code):

        computed_detail_item = (
            self.db.query(RawMaterial).filter(
                RawMaterial.rm_code == rm_code
            ).first()
        )
        if computed_detail_item:
            return computed_detail_item
        return None


    def update_raw_material(self, rm_id: UUID, raw_material_update: RawMaterialUpdate):
        try:
            raw_material = self.db.query(RawMaterial).filter(RawMaterial.id == rm_id).first()
            if not raw_material or raw_material.is_deleted:
                raise RawMaterialNotFoundException(detail="Raw Material not found or already deleted.")

            for key, value in raw_material_update.dict(exclude_unset=True).items():
                setattr(raw_material, key, value)
            self.db.commit()
            self.db.refresh(raw_material)
            return raw_material

        except Exception as e:
            raise RawMaterialUpdateException(detail=f"Error: {str(e)}")

    def soft_delete_raw_material(self, rm_id: UUID):
        try:
            raw_material = self.db.query(RawMaterial).filter(RawMaterial.id == rm_id).first()
            if not raw_material or raw_material.is_deleted:
                raise RawMaterialNotFoundException(detail="Raw Material not found or already deleted.")

            raw_material.is_deleted = True
            self.db.commit()
            self.db.refresh(raw_material)
            return raw_material

        except Exception as e:
            raise RawMaterialSoftDeleteException(detail=f"Error: {str(e)}")


    def restore_raw_material(self, rm_id: UUID):
        try:
            raw_material = self.db.query(RawMaterial).filter(RawMaterial.id == rm_id).first()
            if not raw_material or not raw_material.is_deleted:
                raise RawMaterialNotFoundException(detail="Raw Material not found or already restored.")

            raw_material.is_deleted = False
            self.db.commit()
            self.db.refresh(raw_material)
            return raw_material

        except Exception as e:
            raise RawMaterialRestoreException(detail=f"Error: {str(e)}")


# These are the code for the business logic like calculation etc.
class RawMaterialService(AppService):
    def create_raw_material(self, item: RawMaterialCreate):
        try:
            raw_material_item = RawMaterialCRUD(self.db).create_raw_material(item)

        except Exception as e:
            raise RawMaterialCreateException(detail=f"Error: {str(e)}")

        return raw_material_item

    def all_raw_material(self):
        try:
            raw_material_item = RawMaterialCRUD(self.db).all_raw_material()

        except Exception as e:
            raise RawMaterialNotFoundException(detail=f"Error: {str(e)}")
        return raw_material_item



    def get_raw_material(self, rm_code: str):
        try:
            raw_material_item = RawMaterialCRUD(self.db).get_raw_material(rm_code)

        except Exception as e:
            raise RawMaterialNotFoundException(detail=f"Error: {str(e)}")
        return raw_material_item


    # This is the service/business logic in updating the raw_material.
    def update_raw_material(self, rm_id: UUID, raw_material_update: RawMaterialUpdate):
        raw_material = RawMaterialCRUD(self.db).update_raw_material(rm_id, raw_material_update)
        return raw_material

    # This is the service/business logic in soft deleting the raw_material.
    def soft_delete_raw_material(self, rm_id: UUID):
        raw_material = RawMaterialCRUD(self.db).soft_delete_raw_material(rm_id)
        return raw_material


    # This is the service/business logic in soft restoring the raw_material.
    def restore_raw_material(self, rm_id: UUID):
        raw_material = RawMaterialCRUD(self.db).restore_raw_material(rm_id)
        return raw_material





