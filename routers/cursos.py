from fastapi import APIRouter, Depends, HTTPException, Query
import os
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
    # Normalizar campo de imagen: preferir imagen_url, si no existe usar imagen
    payload = curso.dict()
    raw_img = payload.get('imagen_url') or payload.get('imagen') or None
    if raw_img:
        payload['imagen_url'] = raw_img
    db_curso = Curso(**{k: v for k, v in payload.items() if k in Curso.__table__.columns.keys()})
    db.add(db_curso)
    db.commit()
    db.refresh(db_curso)
    # Normalizar respuesta: asegurar que siempre haya imagen_url
    return _normalize_curso_output(db_curso)

@router.get("/", response_model=list[CursoOut])
def listar_cursos(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1), db: Session = Depends(get_db)):
    cursos = db.query(Curso).offset(skip).limit(limit).all()
    return [_normalize_curso_output(c) for c in cursos]

@router.get("/{curso_id}", response_model=CursoOut)
def obtener_curso(curso_id: int, db: Session = Depends(get_db)):
    curso = db.query(Curso).filter(Curso.id == curso_id).first()
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return _normalize_curso_output(curso)

@router.put("/{curso_id}", response_model=CursoOut)
def actualizar_curso(curso_id: int, curso: CursoCreate, db: Session = Depends(get_db)):
    db_curso = db.query(Curso).filter(Curso.id == curso_id).first()
    if not db_curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    payload = curso.dict()
    raw_img = payload.get('imagen_url') or payload.get('imagen')
    if raw_img is not None:
        payload['imagen_url'] = raw_img
    for key, value in payload.items():
        # Only set attributes that exist on the model
        if key in Curso.__table__.columns.keys():
            setattr(db_curso, key, value)
    db.commit()
    db.refresh(db_curso)
    return _normalize_curso_output(db_curso)

@router.delete("/{curso_id}", response_model=dict)
def eliminar_curso(curso_id: int, db: Session = Depends(get_db)):
    db_curso = db.query(Curso).filter(Curso.id == curso_id).first()
    if not db_curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    db.delete(db_curso)
    db.commit()
    return {"detail": "Curso eliminado exitosamente"}


def _normalize_curso_output(curso: Curso):
    """Return a dict-like object that always has imagen_url resolved.
    If imagen_url is relative, prepend BASE_URL env var if available."""
    base = os.environ.get('BASE_URL') or os.environ.get('BACKEND_BASE_URL') or ''
    img = getattr(curso, 'imagen_url', None) or getattr(curso, 'imagen', None) or ''
    if img and base and not img.lower().startswith('http'):
        img = f"{base.rstrip('/')}/{img.lstrip('/')}"

    # Build a dict with model fields plus imagen_url
    data = {col: getattr(curso, col) for col in curso.__table__.columns.keys()}
    data['imagen_url'] = img or None
    return data
