from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any
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
    
class ConnectionCreate(BaseModel) :
    source_id: int
    target_id: int
    label: Optional[str]
    metadata_: Optional[Dict[str, Any]] = Field(default_factory=dict)
class ConnectionOut(BaseModel) :
    id: int
    source_id: int
    target_id: int
    label: Optional[str]
    class Config:
        from_attributes = True