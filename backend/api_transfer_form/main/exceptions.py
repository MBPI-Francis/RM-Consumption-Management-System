from fastapi import HTTPException


class TransferFormCreateException(HTTPException):
    def __init__(self, detail="Transfer Form creation failed"):
        super().__init__(status_code=500, detail=detail)

class TransferFormNotFoundException(HTTPException):
    def __init__(self, detail="Transfer Form not found"):
        super().__init__(status_code=404, detail=detail)
