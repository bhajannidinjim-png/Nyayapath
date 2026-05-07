from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.session import Base


class ActionItem(Base):
    __tablename__ = "action_items"

    id = Column(Integer, primary_key=True, index=True)
    judgment_id = Column(Integer, ForeignKey("judgments.id"), nullable=False)
    action_type = Column(String(100), nullable=False)
    action_summary = Column(Text, nullable=False)
    department = Column(String(120), nullable=False)
    deadline = Column(String(120), default="Not specified")
    priority = Column(String(20), default="Medium")
    compliance_requirement = Column(Text, default="")
    appeal_consideration = Column(Text, default="")
    confidence = Column(Float, default=0.0)
    source_text = Column(Text, nullable=False)
    extraction_reason = Column(Text, default="")
    page_reference = Column(Integer, nullable=True)
    verification_status = Column(String(20), default="pending", index=True)
    reviewer_notes = Column(Text, default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    judgment = relationship("Judgment", back_populates="actions")

