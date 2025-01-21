import uuid
from sqlalchemy import Column, ForeignKey, DateTime, Boolean, Date, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from backend.settings.database import Base  # Assuming Base is imported from your database setup



# Parent Model: Department
class HeldForm(Base):
    __tablename__ = "tbl_held_forms"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    rm_code_id = Column(UUID(as_uuid=True), ForeignKey("tbl_raw_materials.id"), nullable=False)
    warehouse_id = Column(UUID(as_uuid=True), ForeignKey("tbl_warehouses.id"), nullable=False)
    rm_soh_id = Column(UUID(as_uuid=True), ForeignKey("tbl_stock_on_hand.id"), nullable=False)
    current_status_id = Column(UUID(as_uuid=True), ForeignKey("tbl_droplist.id"), nullable=True)
    new_status_id = Column(UUID(as_uuid=True), ForeignKey("tbl_droplist.id"), nullable=True)
    computed_detail_id = Column(UUID(as_uuid=True), ForeignKey("tbl_computed_details.id"), nullable=False)


    change_status_date = Column(Date,nullable=False)
    ref_number = Column(String(50), nullable=False, unique=False)
    qty_kg = Column(Numeric(10, 2), nullable=False)
    is_deleted = Column(Boolean, default=False)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc), nullable=True)
    created_by_id = Column(UUID(as_uuid=True), ForeignKey("tbl_users.id"), nullable=True)
    updated_by_id = Column(UUID(as_uuid=True), ForeignKey("tbl_users.id"), nullable=True)
    deleted_by_id = Column(UUID(as_uuid=True), ForeignKey("tbl_users.id"), nullable=True)


    # Relationships
    created_by = relationship("User", foreign_keys=[created_by_id], backref="created_held_form")
    updated_by = relationship("User", foreign_keys=[updated_by_id], backref="updated_held_form")
    deleted_by = relationship("User", foreign_keys=[deleted_by_id], backref="deleted_held_form")
    rm_code = relationship("RawMaterial", foreign_keys=[rm_code_id], backref="rm_held_form")
    rm_soh = relationship("StockOnHand", foreign_keys=[rm_soh_id], backref="soh_held_form")
    warehouse = relationship("Warehouse", foreign_keys=[warehouse_id], backref="warehouse_held_form")
    current_status = relationship("DropList", foreign_keys=[current_status_id], backref="current_status_held_form")
    new_status = relationship("DropList", foreign_keys=[new_status_id], backref="new_status_held_form")
    computed_detail = relationship("ComputedDetail", foreign_keys=[computed_detail_id], backref="compdetail_held_form")



