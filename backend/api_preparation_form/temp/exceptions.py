from fastapi import HTTPException


class PreparationFormCreateException(HTTPException):
    def __init__(self, detail="Preparation Form creation failed"):
        super().__init__(status_code=500, detail=detail)

class PreparationFormNotFoundException(HTTPException):
    def __init__(self, detail="Preparation Form not found"):
        super().__init__(status_code=404, detail=detail)

class PreparationFormUpdateException(HTTPException):
    def __init__(self, detail: str = "Preparation Form update failed"):
        super().__init__(status_code=400, detail=detail)


class PreparationFormSoftDeleteException(HTTPException):
    def __init__(self, detail: str = "Preparation Form soft delete failed"):
        super().__init__(status_code=400, detail=detail)


class PreparationFormRestoreException(HTTPException):
    def __init__(self, detail: str = "Preparation Form restore failed"):
        super().__init__(status_code=400, detail=detail)