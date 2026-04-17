from __future__ import annotations

from datetime import date
from uuid import UUID, uuid4

from pydantic import BaseModel, Field



class NotaMetadata(BaseModel) :
    id: UUID = Field(default_factory=uuid4)
    titulo: str
    tags: list[str] = Field(default=[])
    conexoes: list[str] = Field(default=[])
    criado_em: date = Field(default_factory = date.today)
    modificado_em: date = Field(default_factory = date.today)
    
    model_config = {"extra": "allow"}