from backend.api_notes.main.exceptions import NotesCreateException, NotesNotFoundException, \
    NotesUpdateException, NotesSoftDeleteException, NotesRestoreException
from backend.api_notes.main.main import AppCRUD, AppService
from backend.api_notes.main.models import Notes
from backend.api_notes.main.schemas import NotesCreate, NotesUpdate
from uuid import UUID


# These are the code for the app to communicate to the database
class NotesCRUD(AppCRUD):
    def create_notes(self, notes: NotesCreate):
        notes_item = Notes(product_code=notes.product_code,
                                  lot_number=notes.lot_number,
                                    product_kind_id=notes.product_kind_id,
                                    stock_change_date=notes.stock_change_date,
                                   updated_by_id=notes.updated_by_id,
                                   created_by_id=notes.created_by_id)
        self.db.add(notes_item)
        self.db.commit()
        self.db.refresh(notes_item)
        return notes_item

    def get_notes(self):
        notes_item = self.db.query(Notes).all()
        if notes_item:
            return notes_item
        return None


    def update_notes(self, notes_id: UUID, notes_update: NotesUpdate):
        try:
            notes = self.db.query(Notes).filter(Notes.id == notes_id).first()
            if not notes or notes.is_deleted:
                raise NotesNotFoundException(detail="Notes not found or already deleted.")

            for key, value in notes_update.model_dump(exclude_unset=True).items():
                setattr(notes, key, value)
            self.db.commit()
            self.db.refresh(notes)
            return notes

        except Exception as e:
            raise NotesUpdateException(detail=f"Error: {str(e)}")

    def soft_delete_notes(self, notes_id: UUID):
        try:
            notes = self.db.query(Notes).filter(Notes.id == notes_id).first()
            if not notes or notes.is_deleted:
                raise NotesNotFoundException(detail="Notes not found or already deleted.")

            notes.is_deleted = True
            self.db.commit()
            self.db.refresh(notes)
            return notes

        except Exception as e:
            raise NotesSoftDeleteException(detail=f"Error: {str(e)}")


    def restore_notes(self, notes_id: UUID):
        try:
            notes = self.db.query(Notes).filter(Notes.id == notes_id).first()
            if not notes or not notes.is_deleted:
                raise NotesNotFoundException(detail="Notes not found or already restored.")

            notes.is_deleted = False
            self.db.commit()
            self.db.refresh(notes)
            return notes

        except Exception as e:
            raise NotesRestoreException(detail=f"Error: {str(e)}")


# These are the code for the business logic like calculation etc.
class NotesService(AppService):
    def create_notes(self, item: NotesCreate):
        try:
            notes_item = NotesCRUD(self.db).create_notes(item)

        except Exception as e:
            raise NotesCreateException(detail=f"Error: {str(e)}")

        return notes_item

    def get_notes(self):
        try:
            notes_item = NotesCRUD(self.db).get_notes()

        except Exception as e:
            raise NotesNotFoundException(detail=f"Error: {str(e)}")
        return notes_item

    # This is the service/business logic in updating the notes.
    def update_notes(self, notes_id: UUID, notes_update: NotesUpdate):
        notes = NotesCRUD(self.db).update_notes(notes_id, notes_update)
        return notes

    # This is the service/business logic in soft deleting the notes.
    def soft_delete_notes(self, notes_id: UUID):
        notes = NotesCRUD(self.db).soft_delete_notes(notes_id)
        return notes


    # This is the service/business logic in soft restoring the notes.
    def restore_notes(self, notes_id: UUID):
        notes = NotesCRUD(self.db).restore_notes(notes_id)
        return notes





