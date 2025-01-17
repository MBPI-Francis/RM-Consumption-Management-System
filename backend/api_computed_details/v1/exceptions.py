from fastapi import HTTPException


class ComputedDetailCreateException(HTTPException):
    def __init__(self, detail="Computed Details Record creation failed"):
        super().__init__(status_code=500, detail=detail)

class ComputedDetailNotFoundException(HTTPException):
    def __init__(self, detail="Computed Details Record not found"):
        super().__init__(status_code=404, detail=detail)
