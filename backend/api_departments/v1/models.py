import uuid
from sqlalchemy import Column, String, ForeignKey, DateTime, Boolean, event
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from backend.settings.database import Base  # Assuming Base is imported from your database setup


# Parent Model: Department
class Department(Base):
    __tablename__ = "tbl_departments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    name = Column(String(150), nullable=False, unique=True)
    description = Column(String(300), nullable=False)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc), nullable=True)

    # Relationship with User
    users = relationship("User", back_populates="department")


