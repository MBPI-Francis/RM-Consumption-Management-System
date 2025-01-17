import uuid
from sqlalchemy import Column, String, ForeignKey, DateTime, Boolean, SmallInteger
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from backend.settings.database import Base  # Assuming Base is imported from your database setup
from backend.api_users.v1.models import User


# Parent Model: Department
class ComputedDetail(Base):
    __tablename__ = "tbl_computed_details"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    date_computed = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    computed_by_id = Column(UUID(as_uuid=True), ForeignKey("tbl_users.id"), nullable=True)


    # Relationships for computed_by
    computed_by = relationship("User", foreign_keys=[computed_by_id], backref="computed_by_details")




