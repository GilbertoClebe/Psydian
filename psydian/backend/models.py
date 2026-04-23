from database import Base
from sqlalchemy import func, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Optional
class FileRecord(Base) :
    __tablename__ = "files"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255))
    path: Mapped[str] = mapped_column(String(500), unique=True)
    tags: Mapped[Optional[str]] = mapped_column(default="", nullable=True)
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(server_default=func.now(), onupdate=func.now(), nullable=True)
    