from fastapi import HTTPException

class PreparationFormCreateException(HTTPException):
    def __init__(self, detail="Preparation Form creation failed"):
        super().__init__(status_code=500, detail=detail)

class PreparationFormNotFoundException(HTTPException):
    def __init__(self, detail="Preparation Form not found"):
        super().__init__(status_code=404, detail=detail)
