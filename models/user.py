from sqlalchemy import  Boolean, ForeignKey, Column, Integer, String
from database import Base
from datetime import datetime


class User(Base):
    __tablename__ = 'tbl_user'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # Default generates a new UUID
    # department_id = Column(UUID(as_uuid=True), ForeignKey("tbl_department.id"))  # Foreign Key referring to User's UUID id
    user_name = Column(String(50), unique=True, index=True)  # VARCHAR Data type
    password = Column(String(50), index=True)  # VARCHAR Data type
    first_name = Column(String(50), unique=True, index=True)  # VARCHAR Data type
    last_name = Column(String(50), unique=True, index=True)  # VARCHAR Data type
    is_superuser = Column(Boolean, default=True)  # Boolean field (True or False)
    is_reguser = Column(Boolean, default=True)  # Boolean field (True or False)
    is_active = Column(Boolean, default=True)  # Boolean field (True or False)
    created_at = Column(DateTime, default=datetime.utcnow)  # Timestamp for creation date
    modified_at = Column(DateTime, nullable=True)  # Nullable DateTime field
    deactivated_at = Column(DateTime, nullable=True)  # Nullable DateTime field





