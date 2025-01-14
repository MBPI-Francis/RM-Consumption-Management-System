from backend.api_droplist.v1.exceptions import DropListCreateException, DropListNotFoundException, \
    DropListUpdateException, DropListSoftDeleteException, DropListRestoreException
from backend.api_droplist.v1.main import AppCRUD, AppService
from backend.api_droplist.v1.models import DropList
from backend.api_droplist.v1.schemas import DropListCreate, DropListUpdate
from uuid import UUID


# These are the code for the app to communicate to the database
class DropListCRUD(AppCRUD):
    def create_droplist(self, droplist: DropListCreate):
        droplist_item = DropList(name=droplist.name,
                                   description=droplist.description,
                                   updated_by_id=droplist.updated_by_id,
                                   created_by_id=droplist.created_by_id)
        self.db.add(droplist_item)
        self.db.commit()
        self.db.refresh(droplist_item)
        return droplist_item

    def get_droplist(self):
        droplist_item = self.db.query(DropList).all()
        if droplist_item:
            return droplist_item
        return None


    def update_droplist(self, droplist_id: UUID, droplist_update: DropListUpdate):
        try:
            droplist = self.db.query(DropList).filter(DropList.id == droplist_id).first()
            if not droplist or droplist.is_deleted:
                raise DropListNotFoundException(detail="Drop List not found or already deleted.")

            for key, value in droplist_update.dict(exclude_unset=True).items():
                setattr(droplist, key, value)
            self.db.commit()
            self.db.refresh(droplist)
            return droplist

        except Exception as e:
            raise DropListUpdateException(detail=f"Error: {str(e)}")

    def soft_delete_droplist(self, droplist_id: UUID):
        try:
            droplist = self.db.query(DropList).filter(DropList.id == droplist_id).first()
            if not droplist or droplist.is_deleted:
                raise DropListNotFoundException(detail="Drop List not found or already deleted.")

            droplist.is_deleted = True
            self.db.commit()
            self.db.refresh(droplist)
            return droplist

        except Exception as e:
            raise DropListSoftDeleteException(detail=f"Error: {str(e)}")


    def restore_droplist(self, droplist_id: UUID):
        try:
            droplist = self.db.query(DropList).filter(DropList.id == droplist_id).first()
            if not droplist or not droplist.is_deleted:
                raise DropListNotFoundException(detail="Drop List not found or already restored.")

            droplist.is_deleted = False
            self.db.commit()
            self.db.refresh(droplist)
            return droplist

        except Exception as e:
            raise DropListRestoreException(detail=f"Error: {str(e)}")


# These are the code for the business logic like calculation etc.
class DropListService(AppService):
    def create_droplist(self, item: DropListCreate):
        try:
            droplist_item = DropListCRUD(self.db).create_droplist(item)

        except Exception as e:
            raise DropListCreateException(detail=f"Error: {str(e)}")


        return droplist_item

    def get_droplist(self):
        try:
            droplist_item = DropListCRUD(self.db).get_droplist()

        except Exception as e:
            raise DropListNotFoundException(detail=f"Error: {str(e)}")
        return droplist_item

    # This is the service/business logic in updating the droplist.
    def update_droplist(self, droplist_id: UUID, droplist_update: DropListUpdate):
        droplist = DropListCRUD(self.db).update_droplist(droplist_id, droplist_update)
        return droplist

    # This is the service/business logic in soft deleting the droplist.
    def soft_delete_droplist(self, droplist_id: UUID):
        droplist = DropListCRUD(self.db).soft_delete_droplist(droplist_id)
        return droplist


    # This is the service/business logic in soft restoring the droplist.
    def restore_droplist(self, droplist_id: UUID):
        droplist = DropListCRUD(self.db).restore_droplist(droplist_id)
        return droplist





