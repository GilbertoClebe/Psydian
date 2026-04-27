from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from database import get_db
from models import Connection
from schemas import ConnectionCreate, ConnectionOut
import logging

router = APIRouter(prefix="/connections", tags=["connections"])

@router.post("/", response_model=ConnectionOut)
def create_connection(conn: ConnectionCreate, db: Session = Depends(get_db)) :
    try :
        db_conn = Connection(
            source_id = conn.source_id,
            target_id = conn.target_id,
            label = conn.label,
            metadata_ = conn.metadata_
        )
        
        db.add(db_conn)
        db.commit()
        db.refresh(db_conn)
        return db_conn
            
    except SQLAlchemyError as e:
        db.rollback()
        logging.error(f"Erro no commit do banco de dados: {e}")
        raise HTTPException(status_code=500, detail="Erro ao realizar a conexão com o banco de dados")

@router.get("/")
def list_connections(db: Session = Depends(get_db)) :
    try :
        return db.query(Connection).all()
    except SQLAlchemyError as e :
        db.rollback()
        logging.error(f"Erro ao listar conexões: {e}")
        raise HTTPException(status_code=500, detail="Erro ao buscar conexões no banco de dados. ")

@router.delete("/{conn_id}")
def delete_connections(conn_id: int, db: Session = Depends(get_db)) :
    try :

        conn = db.query(Connection).filter(Connection.id == conn_id).first()
        
        if not conn :
            raise HTTPException(status_code=404, detail="Connection not found")
    
        db.delete(conn)
        db.commit()
        return {"Ok": True}

    except SQLAlchemyError as e:
        db.rollback()
        logging.exception(f"Erro ao buscar conexão: {e}")
        raise HTTPException(status_code=500, detail="Erro ao buscar a conexão no banco de dados")