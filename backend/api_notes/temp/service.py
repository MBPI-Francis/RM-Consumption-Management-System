from backend.api_notes.temp.exceptions import NotesCreateException, NotesNotFoundException, \
    NotesUpdateException, NotesSoftDeleteException, NotesRestoreException
from backend.api_notes.temp.main import AppCRUD, AppService
from backend.api_notes.temp.models import TempNotes
from backend.api_notes.temp.schemas import NotesCreate, NotesUpdate
from uuid import UUID
from sqlalchemy import or_

# These are the code for the app to communicate to the database
class TempNotesCRUD(AppCRUD):
    def create_notes(self, notes: NotesCreate):
        notes_item = TempNotes(product_code=notes.product_code,
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
        # Query TempNotes with filters applied to is_cleared and is_deleted columns
        notes_item = self.db.query(TempNotes).filter(
            or_(
                TempNotes.is_cleared.is_(None),  # NULL check for is_cleared
                TempNotes.is_cleared == False # False check for is_cleared

            ),
            or_(
                TempNotes.is_deleted.is_(None),  # NULL check for is_deleted
                TempNotes.is_deleted == False  # False check for is_deleted
            )

        ).all()

        # Return the filtered records, or an empty list if no records are found
        if notes_item:
            return notes_item
        return []


    def update_notes(self, notes_id: UUID, notes_update: NotesUpdate):
        try:
            notes = self.db.query(TempNotes).filter(TempNotes.id == notes_id).first()
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
            notes = self.db.query(TempNotes).filter(TempNotes.id == notes_id).first()
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
            notes = self.db.query(TempNotes).filter(TempNotes.id == notes_id).first()
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
            notes_item = TempNotesCRUD(self.db).create_notes(item)

        except Exception as e:
            raise NotesCreateException(detail=f"Error: {str(e)}")

        return notes_item

    def get_notes(self):
        try:
            notes_item = TempNotesCRUD(self.db).get_notes()

        except Exception as e:
            raise NotesNotFoundException(detail=f"Error: {str(e)}")
        return notes_item

    # This is the service/business logic in updating the notes.
    def update_notes(self, notes_id: UUID, notes_update: NotesUpdate):
        notes = TempNotesCRUD(self.db).update_notes(notes_id, notes_update)
        return notes

    # This is the service/business logic in soft deleting the notes.
    def soft_delete_notes(self, notes_id: UUID):
        notes = TempNotesCRUD(self.db).soft_delete_notes(notes_id)
        return notes


    # This is the service/business logic in soft restoring the notes.
    def restore_notes(self, notes_id: UUID):
        notes = TempNotesCRUD(self.db).restore_notes(notes_id)
        return notes





