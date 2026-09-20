from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
import uuid
from app.database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    # pending → processing → done / failed
    status = Column(String(20), default="pending")
    result = Column(Text, nullable=True)
    # lambda để SQLAlchemy gọi lại mỗi lần tạo row — tránh timestamp bị đóng băng lúc import
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))