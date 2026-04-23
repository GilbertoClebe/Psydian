from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import get_db
from models import FileRecord
from schemas import FileCreate, FileUpdate, FileResponse
from pathlib import Path
from typing import Optional
import os

router = APIRouter(prefix="/files", tags=["files"])
WORKSPACE_DIR = Path("./files")
WORKSPACE_DIR.mkdir(exist_ok=True)
#Concluida
@router.get("/", response_model=list[FileResponse])
def list_files(db: Session = Depends(get_db)) :
    try :
        files = db.query(FileRecord).all()
        for f in files :
            f.tags = f.tags.split(",") if f.tags else []
        return files
    except :
        db.rollback()
        raise HTTPException.add_note("Falha ao listar os arquivos")
#Concluida
@router.post("/", response_model=FileResponse)
def create_file(data: FileCreate, db: Session = Depends(get_db)) :
    #Renomeia o titulo deixando ele em lower case e colocando o .md
    try:
        filename = f"{data.title.lower().replace(' ', '_')}.md"
        filepath = os.path.join(WORKSPACE_DIR, filename)
        # salva o content do arquivo
        os.makedirs(WORKSPACE_DIR, exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f :
            f.write(data.content)
            
        #cria uma nova variavel para salvar o arquivo
        record = FileRecord(
            title = data.title,
            path=filepath,
            tags=",".join(data.tags)
        )
        #faz o commit no db, atualizando a variavel atual e o db
        db.add(record)
        db.commit()
        db.refresh(record)
        record.tags = data.tags
        return record
    except :
        db.rollback()
        raise HTTPException.add_note("Falha ao criar o arquivo")
#Concluida
@router.get("/", response_model=FileResponse)
def get_file_by_id(id: int, db: Session = Depends(get_db)) :
    try :
        file_by_id = db.get(FileRecord, id)
        return file_by_id
    except :
        db.rollback()
        raise HTTPException.add_note("Falha ao buscar por id")    
#Concluida
@router.get("/", response_model=FileResponse)
def get_by_files_title(title: str, db: Session = Depends(get_db)) :
    try :
        query = select(FileResponse).where(FileResponse.title == title).scalar_one_or_none()
        return db.execute(query)
        
    except :
        db.rollback()
        raise HTTPException.add_note("Falha ao buscar por filtros")

@router.put("/", response_model=FileResponse)
def update_file(id_get: int, title: Optional[str] = None, content: Optional[str] = None, db: Session = Depends(get_db)) :
    try :
        file = db.get(FileResponse, id)
        if file :
            file_updated = file
            file_updated.content = content
            file_updated.title = title
            return file_updated
    except :
        db.rollback()
        raise HTTPException.add_note("Falha ao atualizar")

@router.delete("/")
def delete_file(id: int, db: Session = Depends(get_db)) :
    try :
        file_to_del = db.get(FileResponse, id)
        db.delete(file_to_del)
        db.commit()
        return "File deletada"
    except :
        db.rollback()
        raise HTTPException.add_note("Falha ao ")


