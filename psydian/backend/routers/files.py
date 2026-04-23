from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from pathlib import Path
from ..models import FileRecord
from ..schemas import FileCreate, FileUpdate, FileResponse
import os

router = APIRouter(prefix="/files", tags=["files"])
WORKSPACE_DIR = Path("./files")
WORKSPACE_DIR.mkdir(exist_ok=True)

