import uuid
from sqlalchemy import Column, String, ForeignKey, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.settings.database import Base  # Assuming Base is imported from your database setup



# Child Model: User
class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Foreign Key to Department
    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"), nullable=False)

    # Relationship with Department
    # department = relationship("Department", back_populates="users")