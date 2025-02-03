from fastapi import HTTPException


class ReceivingReportCreateException(HTTPException):
    def __init__(self, detail="Receiving Report creation failed"):
        super().__init__(status_code=500, detail=detail)

class ReceivingReportNotFoundException(HTTPException):
    def __init__(self, detail="Receiving Report not found"):
        super().__init__(status_code=404, detail=detail)
