from backend.api_notes.main.exceptions import NotesCreateException, NotesNotFoundException
from backend.api_notes.main.main import AppCRUD, AppService
from backend.api_notes.main.models import Notes
from backend.api_notes.main.schemas import NotesCreate
from uuid import UUID


# These are the code for the app to communicate to the database
class NotesCRUD(AppCRUD):
    def create_notes(self, notes: NotesCreate):
        notes_item = Notes(product_code=notes.product_code,
                                  lot_number=notes.lot_number,
                                    product_kind_id=notes.product_kind_id,
                                    computed_detail_id=notes.computed_detail_id,
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
        return []

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

