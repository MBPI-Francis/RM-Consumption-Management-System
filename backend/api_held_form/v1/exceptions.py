from fastapi import HTTPException


class HeldFormCreateException(HTTPException):
    def __init__(self, detail="Held Form creation failed"):
        super().__init__(status_code=500, detail=detail)

class HeldFormNotFoundException(HTTPException):
    def __init__(self, detail="Held Form not found"):
        super().__init__(status_code=404, detail=detail)

class HeldFormUpdateException(HTTPException):
    def __init__(self, detail: str = "Held Form update failed"):
        super().__init__(status_code=400, detail=detail)


class HeldFormSoftDeleteException(HTTPException):
    def __init__(self, detail: str = "Held Form soft delete failed"):
        super().__init__(status_code=400, detail=detail)


class HeldFormRestoreException(HTTPException):
    def __init__(self, detail: str = "Held Form restore failed"):
        super().__init__(status_code=400, detail=detail)