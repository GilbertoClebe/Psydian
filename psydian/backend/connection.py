from typing import Optional, Dict, Any
from database import Base
from sqlalchemy import ForeignKey, String, JSON
from sqlalchemy.orm import Mapped, mapped_column
class Connection(Base) :
    __tablename__ = "connections"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    source_id: Mapped[int] = mapped_column(ForeignKey("files.id"), nullable=False)
    target_id: Mapped[int] = mapped_column(ForeignKey("files.id"), nullable=False)
    label: Mapped[Optional[str]] = mapped_column(String(255))
    metadata: Mapped[Dict[str, any]] = mapped_column("metadata", JSON, default=dict)