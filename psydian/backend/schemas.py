from pydantic import BaseModel
from datetime import datetime
from typing import Optional
class FileCreate(BaseModel) :
    title: str
    content: str
    tags: list[str] = []
    path: str
class FileUpdate(BaseModel) :
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[list[str]] = None
class FileResponse(BaseModel) :
    id: int
    title: str
    path: str
    tags: list[str]
    content: str
    created_at: datetime
    updated_at: Optional[datetime] 
    model_config = {"from_attributes": True}