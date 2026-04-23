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
            content=data.content,
            path=filepath,
            tags=",".join(data.tags)
        )
        #faz o commit no db, atualizando a variavel atual e o db
        db.add(record)
        db.commit()
        db.refresh(record)
        record.tags = data.tags
        return record
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))
#Concluida
@router.get("/{id}", response_model=FileResponse)
def get_file_by_id(id: int, db: Session = Depends(get_db)) :
    try :
        file_by_id = db.get(FileRecord, id)
        return file_by_id
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))    
#Concluida
@router.get("/search", response_model=FileResponse)
def get_by_files_title(title: str, db: Session = Depends(get_db)) :
    try :
        query = select(FileRecord).where(FileRecord.title == title).scalar_one_or_none()
        return db.execute(query)
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/", response_model=FileResponse)
def update_file(id: int, title: Optional[str] = None, content: Optional[str] = None, db: Session = Depends(get_db)) :
    try :
        file = db.get(FileRecord, id)
        if file :
            file_updated = file
            file_updated.content = content
            file_updated.title = title
            db.commit()
            db.refresh(file)
            return file_updated
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/")
def delete_file(id: int, db: Session = Depends(get_db)) :
    try :
        file = db.get(FileRecord, id)
        if not file:
            raise HTTPException(status_code=404, detail="Arquivo não encontrado")
        Path(file.path).unlink(missing_ok=True)
        db.delete(file)
        db.commit()
        return {"message": "Arquivo deletado"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


