from fastapi import HTTPException


class DropListCreateException(HTTPException):
    def __init__(self, detail="Drop List creation failed"):
        super().__init__(status_code=500, detail=detail)

class DropListNotFoundException(HTTPException):
    def __init__(self, detail="Drop List not found"):
        super().__init__(status_code=404, detail=detail)


class DropListUpdateException(HTTPException):
    def __init__(self, detail: str = "Drop List update failed"):
        super().__init__(status_code=400, detail=detail)


class DropListSoftDeleteException(HTTPException):
    def __init__(self, detail: str = "Drop List soft delete failed"):
        super().__init__(status_code=400, detail=detail)


class DropListRestoreException(HTTPException):
    def __init__(self, detail: str = "Drop List restore failed"):
        super().__init__(status_code=400, detail=detail)