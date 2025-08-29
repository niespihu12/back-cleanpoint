from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Recompensa, Usuario
from schemas import RecompensaCreate, RecompensaOut
from database import SessionLocal

router = APIRouter(prefix="/recompensas", tags=["Recompensas"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[RecompensaOut])
def listar_recompensas(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Recompensa).offset(skip).limit(limit).all()

@router.post("/", response_model=RecompensaOut)
def crear_recompensa(recompensa: RecompensaCreate, db: Session = Depends(get_db)):
    db_recompensa = Recompensa(**recompensa.dict())
    db.add(db_recompensa)
    db.commit()
    db.refresh(db_recompensa)
    return db_recompensa

@router.post("/usuarios/{usuario_id}/reclamar/", response_model=RecompensaOut)
def reclamar_recompensa(usuario_id: int, recompensa: RecompensaCreate, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if usuario.cleanpoints < recompensa.puntos_requeridos:
        raise HTTPException(status_code=400, detail="No tienes suficientes cleanpoints")
    usuario.cleanpoints -= recompensa.puntos_requeridos
    db_recompensa = Recompensa(**recompensa.dict(), usuario_id=usuario_id)
    db.add(db_recompensa)
    db.commit()
    db.refresh(db_recompensa)
    return db_recompensa