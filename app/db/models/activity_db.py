from sqlalchemy import Column, String, Integer, Float, DateTime
from sqlalchemy.dialects.postgresql import JSONB, UUID
from app.database import Base
import uuid


class ActivityDB(Base):
    __tablename__ = "activities"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Integer, nullable=False)
    source = Column(String, nullable=False)
    type = Column(String, nullable=False)
    file_type = Column(String)
    start_time = Column(DateTime(timezone=True), nullable=False)

    summary = Column(JSONB, nullable=False)
    samples = Column(JSONB)
    device = Column(JSONB)
    comparison = Column(JSONB)
    linked_session = Column(JSONB)

    rpe = Column(Integer)
    tss = Column(Float)
    notes = Column(String)
    perceived_recovery = Column(Integer)
