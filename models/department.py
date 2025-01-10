from sqlalchemy import  Boolean, ForeignKey, Column, Integer, String
from database import Base
from datetime import datetime


class Department(Base):
    __tablename__ = 'tbl_department'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # Default generates a new UUID
    department = Column(String(150), unique=True, index=True)  # VARCHAR Data type
    is_deleted = Column(Boolean, default=False)  # Boolean field (True or False)
    created_at = Column(DateTime, default=datetime.utcnow)  # Timestamp for creation date
    modified_at = Column(DateTime, default=datetime.utcnow)  # Timestamp for modifying date
    deleted_at = Column(DateTime, nullable=True)  # Nullable DateTime field
    created_by = Column(UUID(as_uuid=True), ForeignKey("tbl_user.id"),nullable=True) # Foreign Key referring to User's UUID id
    modified_by = Column(UUID(as_uuid=True), ForeignKey("tbl_user.id"), nullable=True) # Foreign Key referring to User's UUID id
    deleted_by = Column(UUID(as_uuid=True), ForeignKey("tbl_user.id"), nullable=True)  # Foreign Key referring to User's UUID id







