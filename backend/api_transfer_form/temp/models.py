import uuid
from sqlalchemy import Column, String, ForeignKey, DateTime, Boolean, SmallInteger, Date, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from backend.settings.database import Base  # Assuming Base is imported from your database setup
from backend.api_users.v1.models import User


# Parent Model: Department
class TransferForm(Base):
    __tablename__ = "tbl_transfer_forms"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    rm_code_id = Column(UUID(as_uuid=True), ForeignKey("tbl_raw_materials.id"), nullable=False)
    from_warehouse_id = Column(UUID(as_uuid=True), ForeignKey("tbl_warehouses.id"), nullable=False)
    to_warehouse_id = Column(UUID(as_uuid=True), ForeignKey("tbl_warehouses.id"), nullable=False)
    rm_soh_id = Column(UUID(as_uuid=True), ForeignKey("tbl_stock_on_hand.id"), nullable=False)

    ref_number = Column(String(50), nullable=False, unique=True)
    transfer_date = Column(Date,nullable=False)
    qty_kg = Column(Numeric(10, 2), nullable=False)
    is_deleted = Column(Boolean, default=False)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc), nullable=True)
    created_by_id = Column(UUID(as_uuid=True), ForeignKey("tbl_users.id"), nullable=True)
    updated_by_id = Column(UUID(as_uuid=True), ForeignKey("tbl_users.id"), nullable=True)
    deleted_by_id = Column(UUID(as_uuid=True), ForeignKey("tbl_users.id"), nullable=True)


    # Relationships for created_by, updated_by, and deleted_by
    created_by = relationship("User", foreign_keys=[created_by_id], backref="created_transfer_form")
    updated_by = relationship("User", foreign_keys=[updated_by_id], backref="updated_transfer_form")
    deleted_by = relationship("User", foreign_keys=[deleted_by_id], backref="deleted_transfer_form")
    rm_code = relationship("RawMaterial", foreign_keys=[rm_code_id], backref="rm_transfer_form")
    rm_soh = relationship("StockOnHand", foreign_keys=[rm_soh_id], backref="soh_transfer_form")
    from_warehouse = relationship("Warehouse", foreign_keys=[from_warehouse_id], backref="from_warehouse_transfer_form")
    to_warehouse = relationship("Warehouse", foreign_keys=[to_warehouse_id], backref="to_warehouse_transfer_form")



