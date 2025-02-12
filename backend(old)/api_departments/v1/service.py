from backend.api_departments.v1.exceptions import DepartmentCreateException, DepartmentNotFoundException, \
    DepartmentUpdateException, DepartmentSoftDeleteException, DepartmentRestoreException
from backend.api_departments.v1.main import AppCRUD, AppService
from backend.api_departments.v1.models import Department
from backend.api_departments.v1.schemas import DepartmentCreate, DepartmentUpdate
from uuid import UUID


# These are the code for the app to communicate to the database
class DepartmentCRUD(AppCRUD):
    def create_department(self, department: DepartmentCreate):
        department_item = Department(name=department.name,
                                     description=department.description,
                                     is_deleted=department.is_deleted)
        self.db.add(department_item)
        self.db.commit()
        self.db.refresh(department_item)
        return department_item

    def get_department(self):
        department_item = self.db.query(Department).all()
        if department_item:
            return department_item
        return []


    def update_department(self, department_id: UUID, department_update: DepartmentUpdate):
        try:
            department = self.db.query(Department).filter(Department.id == department_id).first()
            if not department or department.is_deleted:
                raise DepartmentNotFoundException(detail="Department not found or already deleted.")

            for key, value in department_update.dict(exclude_unset=True).items():
                setattr(department, key, value)
            self.db.commit()
            self.db.refresh(department)
            return department

        except Exception as e:
            raise DepartmentUpdateException(detail=f"Error: {str(e)}")

    def soft_delete_department(self, department_id: UUID):
        try:
            department = self.db.query(Department).filter(Department.id == department_id).first()
            if not department or department.is_deleted:
                raise DepartmentNotFoundException(detail="Department not found or already deleted.")

            department.is_deleted = True
            self.db.commit()
            self.db.refresh(department)
            return department

        except Exception as e:
            raise DepartmentSoftDeleteException(detail=f"Error: {str(e)}")


    def restore_department(self, department_id: UUID):
        try:
            department = self.db.query(Department).filter(Department.id == department_id).first()
            if not department or not department.is_deleted:
                raise DepartmentNotFoundException(detail="Department not found or already restored.")

            department.is_deleted = False
            self.db.commit()
            self.db.refresh(department)
            return department

        except Exception as e:
            raise DepartmentRestoreException(detail=f"Error: {str(e)}")


# These are the code for the business logic like calculation etc.
class DepartmentService(AppService):
    def create_department(self, item: DepartmentCreate):
        try:
            department_item = DepartmentCRUD(self.db).create_department(item)

        except Exception as e:
            raise DepartmentCreateException(detail=f"Error: {str(e)}")


        return department_item

    def get_department(self):
        try:
            department_item = DepartmentCRUD(self.db).get_department()

        except Exception as e:
            raise DepartmentNotFoundException(detail=f"Error: {str(e)}")
        return department_item

    # This is the service/business logic in updating the department.
    def update_department(self, department_id: UUID, department_update: DepartmentUpdate):
        department = DepartmentCRUD(self.db).update_department(department_id, department_update)
        return department

    # This is the service/business logic in soft deleting the department.
    def soft_delete_department(self, department_id: UUID):
        department = DepartmentCRUD(self.db).soft_delete_department(department_id)
        return department


    # This is the service/business logic in soft restoring the department.
    def restore_department(self, department_id: UUID):
        department = DepartmentCRUD(self.db).restore_department(department_id)
        return department





