from fastapi import HTTPException


class DepartmentCreateException(HTTPException):
    def __init__(self, detail="Department creation failed"):
        super().__init__(status_code=500, detail=detail)

class DepartmentNotFoundException(HTTPException):
    def __init__(self, detail="Department not found"):
        super().__init__(status_code=404, detail=detail)


class DepartmentUpdateException(HTTPException):
    def __init__(self, detail: str = "Department update failed"):
        super().__init__(status_code=400, detail=detail)


class DepartmentSoftDeleteException(HTTPException):
    def __init__(self, detail: str = "Department soft delete failed"):
        super().__init__(status_code=400, detail=detail)


class DepartmentRestoreException(HTTPException):
    def __init__(self, detail: str = "Department restore failed"):
        super().__init__(status_code=400, detail=detail)