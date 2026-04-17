from __future__ import annotations

from datetime import date

from sqlalchemy import String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase) :
    pass

class NotaORM(Base) :
    __tablename__ = "notas"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column(String, nullable=False)
    tags: Mapped[list[str]] = mapped_column(Text, default="")
    conexoes: Mapped[list[str]] = mapped_column(Text, default="")
    criado_em: Mapped[date] = mapped_column(nullable=False)
    modificado_em: Mapped[date] = mapped_column(nullable=False)
    