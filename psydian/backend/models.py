from database import Base
from sqlalchemy import func, String, Text, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Optional, Dict
class FileModel(Base) :
    __tablename__ = "files"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255))
    path: Mapped[str] = mapped_column(String(500), unique=True)
    tags: Mapped[Optional[str]] = mapped_column(default="", nullable=True)
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(server_default=func.now(), onupdate=func.now(), nullable=True)
    
class Connection(Base) :
    __tablename__ = "connections"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    source_id: Mapped[int] = mapped_column(ForeignKey("files.id"), nullable=False)
    target_id: Mapped[int] = mapped_column(ForeignKey("files.id"), nullable=False)
    label: Mapped[Optional[str]] = mapped_column(String(255))
    metadata_: Mapped[Dict[str, any]] = mapped_column("metadata", JSON, default=dict)
    
    @property
    def __repr__(self) :
        return f"<Connection {self.id}: {self.source_id} -> {self.target_id}>"