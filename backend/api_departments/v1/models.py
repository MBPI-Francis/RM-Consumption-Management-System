import uuid
from sqlalchemy import Column, String, ForeignKey, DateTime, Boolean, event
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.settings.database import Base  # Assuming Base is imported from your database setup


# Parent Model: Department
class Department(Base):
    __tablename__ = "tbl_departments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    name = Column(String(150), nullable=False, unique=True)
    description = Column(String(300), nullable=False)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)

    # Relationship with User
    users = relationship("User", back_populates="department")

# Event Listener to Automatically Set deleted_at
@event.listens_for(Department, "before_update")
def set_deleted_at(mapper, connection, target):
    """
    Automatically set the deleted_at column when is_deleted is True.
    """
    if target.is_deleted and not target.deleted_at:
        target.deleted_at = datetime.utcnow()

