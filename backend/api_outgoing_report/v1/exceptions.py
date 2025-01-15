from fastapi import HTTPException


class OutgoingReportCreateException(HTTPException):
    def __init__(self, detail="Outgoing Report creation failed"):
        super().__init__(status_code=500, detail=detail)

class OutgoingReportNotFoundException(HTTPException):
    def __init__(self, detail="Outgoing Report not found"):
        super().__init__(status_code=404, detail=detail)

class OutgoingReportUpdateException(HTTPException):
    def __init__(self, detail: str = "Outgoing Report update failed"):
        super().__init__(status_code=400, detail=detail)


class OutgoingReportSoftDeleteException(HTTPException):
    def __init__(self, detail: str = "Outgoing Report soft delete failed"):
        super().__init__(status_code=400, detail=detail)


class OutgoingReportRestoreException(HTTPException):
    def __init__(self, detail: str = "Outgoing Report restore failed"):
        super().__init__(status_code=400, detail=detail)