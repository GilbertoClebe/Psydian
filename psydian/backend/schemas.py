from pydantic import BaseModel, Field, field_validator
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
    
    @field_validator("tags", mode="before")
    @classmethod
    def parse_tags(cls, v) :
        if isinstance(v, str) :
            return [t for t in v.split(",") if t] 
        return v or []
    
class ConnectionCreate(BaseModel) :
    source_id: int
    target_id: int
    label: Optional[str] = None
    metadata_: Optional[Dict[str, Any]] = Field(default_factory=dict)
class ConnectionOut(BaseModel) :
    id: int
    source_id: int
    target_id: int
    label: Optional[str] = None
    class ConfigDict:
        from_attributes = True