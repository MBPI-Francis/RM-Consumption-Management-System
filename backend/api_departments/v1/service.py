from backend.api_departments.v1.exceptions import AppException
from backend.api_departments.v1.main import AppCRUD, AppService
from backend.api_departments.v1.models import Department
from backend.api_departments.v1.schemas import DepartmentCreate
from backend.api_departments.v1.service_result import ServiceResult


class DepartmentCRUD(AppCRUD):
    def create_department(self, department: DepartmentCreate):
        department_item = Department(name=department.name, description=department.description)
        self.db.add(department_item)
        self.db.commit()
        self.db.refresh(department_item)
        return department_item

    def get_department(self):
        department_item = self.db.query(Department).all()
        if department_item:
            return department_item
        return None


class DepartmentService(AppService):
    def create_department(self, item: DepartmentCreate):
        department_item = DepartmentCRUD(self.db).create_department(item)
        if not department_item:
            return ServiceResult(AppException.DepartmentCreate())
        return ServiceResult(department_item)

    def get_department(self):
        department_item = DepartmentCRUD(self.db).get_department()
        if not department_item:
            return ServiceResult(AppException.DepartmentGet())
        # if not department_item.public:
        #     return ServiceResult(AppException.FooItemRequiresAuth())
        return ServiceResult(department_item)


