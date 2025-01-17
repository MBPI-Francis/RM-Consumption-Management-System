from fastapi import HTTPException


class NotesCreateException(HTTPException):
    def __init__(self, detail="Notes creation failed"):
        super().__init__(status_code=500, detail=detail)

class NotesNotFoundException(HTTPException):
    def __init__(self, detail="Notes not found"):
        super().__init__(status_code=404, detail=detail)
