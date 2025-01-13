from backend.api_users.v1.exceptions import UserNotFoundException, UserCreateException, \
    UserUpdateException, UserRestoreException, UserDeactivateException
from backend.api_departments.v1.main import AppCRUD, AppService
from backend.api_users.v1.models import User
from backend.api_users.v1.schemas import UserCreate, UserUpdate
from uuid import UUID

class UserCRUD(AppCRUD):
    def create_user(self, user: UserCreate):
        user_item = User(user_name=user.user_name,
                               first_name=user.first_name,
                               last_name=user.last_name,
                               password=user.password,
                               department_id=user.department_id,
                               created_by_id = user.created_by_id,
                               updated_by_id = user.updated_by_id
                                 )
        self.db.add(user_item)
        self.db.commit()
        self.db.refresh(user_item)
        return user_item

    def get_user(self):
        user_item = self.db.query(User).all()
        if user_item:
            return user_item
        return None


    def update_department(self, user_id: UUID, user_update: UserUpdate):
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user or not user.is_active:
                raise UserNotFoundException(detail="User not found or deactivated.")

            for key, value in user_update.dict(exclude_unset=True).items():
                setattr(user, key, value)
            self.db.commit()
            self.db.refresh(user)
            return user

        except Exception as e:
            raise UserUpdateException(detail=f"Error: {str(e)}")

    def deactivate_user(self, user_id: UUID):
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user or not user.is_active:
                raise UserNotFoundException(detail="User not found or deactivated.")

            user.is_active = False
            self.db.commit()
            self.db.refresh(user)
            return user

        except Exception as e:
            raise UserDeactivateException(detail=f"Error: {str(e)}")


    def restore_user(self, user_id: UUID):
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user or not user.is_active:
                raise UserNotFoundException(detail="User not found or deactivated.")

            user.is_active = True
            self.db.commit()
            self.db.refresh(user)
            return user

        except Exception as e:
            raise UserRestoreException(detail=f"Error: {str(e)}")


# These are the code for the business logic like calculation etc.
class UserService(AppService):
    def create_user(self, item: UserCreate):
        try:
            user_item = UserCRUD(self.db).create_user(item)

        except Exception as e:
            raise UserCreateException(detail=f"Error: {str(e)}")


        return user_item

    def get_user(self):
        try:
            user_item = UserCRUD(self.db).get_user()

        except Exception as e:
            raise UserNotFoundException(detail=f"Error: {str(e)}")
        return user_item

    # This is the service/business logic in updating the department.
    def update_user(self, user_id: UUID, user_update: UserUpdate):
        user = UserCRUD(self.db).update_user(user_id, user_update)
        return user

    # This is the service/business logic in soft deleting the department.
    def deactivate_user(self, user_id: UUID):
        user = UserCRUD(self.db).deactivate_user(user_id)
        return user


    # This is the service/business logic in soft restoring the department.
    def restore_user(self, user_id: UUID):
        user = UserCRUD(self.db).restore_usert(user_id)
        return user