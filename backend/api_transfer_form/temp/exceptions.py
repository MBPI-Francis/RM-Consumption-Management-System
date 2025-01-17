from fastapi import HTTPException


class TransferFormCreateException(HTTPException):
    def __init__(self, detail="Transfer Form creation failed"):
        super().__init__(status_code=500, detail=detail)

class TransferFormNotFoundException(HTTPException):
    def __init__(self, detail="Transfer Form not found"):
        super().__init__(status_code=404, detail=detail)

class TransferFormUpdateException(HTTPException):
    def __init__(self, detail: str = "Transfer Form update failed"):
        super().__init__(status_code=400, detail=detail)


class TransferFormSoftDeleteException(HTTPException):
    def __init__(self, detail: str = "Transfer Form soft delete failed"):
        super().__init__(status_code=400, detail=detail)


class TransferFormRestoreException(HTTPException):
    def __init__(self, detail: str = "Transfer Form restore failed"):
        super().__init__(status_code=400, detail=detail)