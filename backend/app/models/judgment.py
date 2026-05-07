from sqlalchemy import JSON, Column, DateTime, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.session import Base


class Judgment(Base):
    __tablename__ = "judgments"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    status = Column(String(50), default="extracted", nullable=False)
    total_pages = Column(Integer, default=0)
    scanned_pages = Column(JSON, default=list)
    metadata_json = Column(JSON, default=dict)
    pages_json = Column(JSON, default=list)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    actions = relationship("ActionItem", back_populates="judgment", cascade="all, delete-orphan")

