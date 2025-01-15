from fastapi import HTTPException


class ReceivingReportCreateException(HTTPException):
    def __init__(self, detail="Receiving Report creation failed"):
        super().__init__(status_code=500, detail=detail)

class ReceivingReportNotFoundException(HTTPException):
    def __init__(self, detail="Receiving Report not found"):
        super().__init__(status_code=404, detail=detail)

class ReceivingReportUpdateException(HTTPException):
    def __init__(self, detail: str = "Receiving Report update failed"):
        super().__init__(status_code=400, detail=detail)


class ReceivingReportSoftDeleteException(HTTPException):
    def __init__(self, detail: str = "Receiving Report soft delete failed"):
        super().__init__(status_code=400, detail=detail)


class ReceivingReportRestoreException(HTTPException):
    def __init__(self, detail: str = "Receiving Report restore failed"):
        super().__init__(status_code=400, detail=detail)