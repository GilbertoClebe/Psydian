from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from database import get_db
from models import FileModel
from schemas import FileCreate, FileUpdate, FileResponse
from pathlib import Path
from typing import Optional
import os, logging

router = APIRouter(prefix="/files", tags=["files"])
WORKSPACE_DIR = Path("./files")
WORKSPACE_DIR.mkdir(exist_ok=True)

#Finalizada e revisada
@router.post("/", response_model=FileResponse, status_code=201)
def create_file(file: FileCreate, db: Session = Depends(get_db)) :
    file_title_lowercase = f"{file.title.lower().replace(' ', '_')}.md"
    file_path = WORKSPACE_DIR / file_title_lowercase
    if file_path.exists() : 
        raise HTTPException(
            status_code=409, 
            detail=f"O arquivo: {file_title_lowercase} já existe no servidor")
    os.makedirs(WORKSPACE_DIR, exist_ok=True)
    
    try :
        file_path.write_text(file.content, encoding="utf-8")
        
        try :
            new_file = FileModel(
                title = file.title,
                content = file.content,
                tags = ",".join(file.tags),
                path = str(file_path)
            )
            db.add(new_file)
            db.commit()
            db.refresh(new_file)
            return new_file
        
        except SQLAlchemyError as error:
            db.rollback()
            file_path.unlink()
            logging.error(f"Erro de banco de dados: {error}")
            raise HTTPException(status_code=500, detail="Erro ao salvar dados no banco")
        
    except Exception as e :
        logging.error(f"Erro inesperado {e}")
        raise HTTPException(status_code=500, detail="Ocorreu um erro ao processar o arquivo")
#Finalizada e revisada
@router.get("/", response_model=list[FileResponse])
def list_files(db: Session = Depends(get_db)) :
    try :
        
        return db.execute(select(FileModel).order_by(FileModel.title)).scalars().all()
    
    except SQLAlchemyError as error :
        
        logging.error(f"Erro ao acessar os arquivos: {error}")
        raise HTTPException(status_code=500, detail="Não foi possivel acessar a lista")
@router.get("/search", response_model=FileResponse)
def file_by_title(title: str, db: Session = Depends(get_db)) :
    try :
        founded_file = db.execute(select(FileModel).where(FileModel.title == title)).scalar_one_or_none()
        
        if not founded_file :
            logging.error(f"Inconsistencia: Titulo {title} no banco, mas arquivo físico ausente")
            raise HTTPException(status_code=404 , detail="Arquivo registrado no banco, mas não localizado no disco")
        
        return founded_file
    
    except SQLAlchemyError as error:
        db.rollback()
        logging.error(f"Erro ao buscar por titulo: {error}")
        
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao processar a busca no banco de dados."
        )
#Finalizada e revisada
@router.get("/{id}", response_model=FileResponse, status_code=200)
def file_by_id(id: int, db: Session = Depends(get_db)) :
    try:
        found_file = db.get(FileModel, id)
        if not Path(found_file.path).exists() :
            raise HTTPException(status_code=404, detail=f"Caminho do arquivo errado")
        try:
            if found_file :
                return found_file
        except Exception as e :
            raise HTTPException(status_code=404, detail=f"Arquivo não encontrado: {e}")
        
    except SQLAlchemyError as error :
        db.rollback()
        logging.error("Erro ao encontrar arquivo: {error}")
        raise HTTPException(
            status_code=404,
            detail=f"Arquivo não foi encontrado no sistema"
            )
#Finalizada e revisada 
@router.put("/{id}")
def update_file(id: int, file_new: FileUpdate, db: Session = Depends(get_db)) :
    try:
        found_file = db.get(FileModel, id)
        
        if not found_file :
            raise HTTPException(status_code=404, detail="O arquivo é não foi encontrado")
        
        old_path = Path(found_file.path)
        new_title_lower = f"{file_new.title.lower().replace(' ', '_')}.md"
        new_path = WORKSPACE_DIR / new_title_lower
        
        if old_path.exists() :
            
            if old_path != new_path :
                
                if new_path.exists() :
                    raise HTTPException(status_code=409, detail="Já existe um arquivo com esse novo título.")
                
                old_path.rename(new_path)
            new_path.write_text(file_new.content, encoding="utf-8")
            
        else:
            new_path.write_text(file_new.content, encoding="utf-8")
            
        try:
            updated_file = found_file
            if file_new.title:
                new_title_lower = f"{file_new.title.lower().replace(' ', '_')}.md"
                new_path = WORKSPACE_DIR / new_title_lower
                if old_path.exists() and old_path != new_path:
                    if new_path.exists():
                        raise HTTPException(status_code=409, detail="Já existe um arquivo com esse novo título.")
                    old_path.rename(new_path)
                found_file.title = file_new.title
                found_file.path = str(new_path)
            if file_new.content :
                updated_file.content = file_new.content
            if file_new.tags :
                updated_file.tags = ",".join(file_new.tags)
            
            db.add(updated_file)
            db.commit()
            db.refresh(updated_file)
            return updated_file
        
        except SQLAlchemyError as error :
            logging.error(f"Erro ao atualizar os dados do arquivo: {error}")
            raise HTTPException(status_code=304, detail="Os dados não puderem ser alterados no banco")
    
    except SQLAlchemyError as error:
        db.rollback()
        logging.error(f"Arquivo não encontrado: {error}")
        raise HTTPException(status_code=404, detail="O arquivo não foi encontrado pelo id inserido")
#Finalizado e revisado
@router.delete("/{id}")
def delete_file(id: int, db: Session = Depends(get_db)) :
    try :
        found_file = db.get(FileModel, id)
        if not found_file :
            raise HTTPException(
            status_code=404, 
            detail="O arquivo solicitado não existe em nossos registros."
        )
        
        try :
            Path(found_file.path).unlink(missing_ok=True)
            try :
                db.delete(found_file)
                db.commit()
                
                return {"Message": "Arquivo deletado"}
            
            except SQLAlchemyError as error :
                logging.error(f"Não foi possivel deletar o arquivo do banco de dados: {error}")
                raise HTTPException(status_code=500, detail="Não foi possivel remover o arquivo do banco de dados")
        
        except Exception as error :
            logging.error("Não foi possivel deletar o arquivo do disco: {error}")
            raise HTTPException(status_code=500, detail=f"Não foi possivel deletar o arquivo")
    
    except SQLAlchemyError as error :
        logging.error(f"Não foi possivel achar o arquivo a ser deletado: {error}")
        raise HTTPException(
            status_code=404,
            detail="Arquivo não encontrado"
            )
        