from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from models import Curso
from schemas import CursoCreate, CursoOut
from database import SessionLocal

router = APIRouter(prefix="/cursos", tags=["Cursos"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=CursoOut)
def crear_curso(curso: CursoCreate, db: Session = Depends(get_db)):
    if db.query(Curso).filter(Curso.titulo == curso.titulo).first():
        raise HTTPException(status_code=400, detail="Ya existe un curso con ese título")
    db_curso = Curso(**curso.dict())
    db.add(db_curso)
    db.commit()
    db.refresh(db_curso)
    return db_curso

@router.get("/", response_model=list[CursoOut])
def listar_cursos(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1), db: Session = Depends(get_db)):
    return db.query(Curso).offset(skip).limit(limit).all()

@router.get("/{curso_id}", response_model=CursoOut)
def obtener_curso(curso_id: int, db: Session = Depends(get_db)):
    curso = db.query(Curso).filter(Curso.id == curso_id).first()
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return curso

@router.put("/{curso_id}", response_model=CursoOut)
def actualizar_curso(curso_id: int, curso: CursoCreate, db: Session = Depends(get_db)):
    db_curso = db.query(Curso).filter(Curso.id == curso_id).first()
    if not db_curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    for key, value in curso.dict().items():
        setattr(db_curso, key, value)
    db.commit()
    db.refresh(db_curso)
    return db_curso

@router.delete("/{curso_id}", response_model=dict)
def eliminar_curso(curso_id: int, db: Session = Depends(get_db)):
    db_curso = db.query(Curso).filter(Curso.id == curso_id).first()
    if not db_curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    db.delete(db_curso)
    db.commit()
    return {"detail": "Curso eliminado exitosamente"}
