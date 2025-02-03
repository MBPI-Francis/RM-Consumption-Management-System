from fastapi import HTTPException


class OutgoingReportCreateException(HTTPException):
    def __init__(self, detail="Outgoing Report creation failed"):
        super().__init__(status_code=500, detail=detail)

class OutgoingReportNotFoundException(HTTPException):
    def __init__(self, detail="Outgoing Report not found"):
        super().__init__(status_code=404, detail=detail)
