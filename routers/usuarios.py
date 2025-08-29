from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models import Usuario, Curso
from schemas import UsuarioCreate, UsuarioOut
from database import SessionLocal
from routers.auth import get_current_user

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=UsuarioOut)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    # Verificar si el email ya existe
    existing_user = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )
    
    # Verificar si el nombre ya existe
    existing_name = db.query(Usuario).filter(Usuario.nombre == usuario.nombre).first()
    if existing_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de usuario ya está en uso"
        )
    
    # Crear nuevo usuario (sin password_hash aquí, se maneja en auth)
    db_usuario = Usuario(
        nombre=usuario.nombre,
        email=usuario.email,
        password_hash="",  # Se maneja en el router de auth
        cleanpoints=0
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

@router.get("/{usuario_id}", response_model=UsuarioOut)
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.get("/{usuario_id}/cleanpoints", response_model=int)
def consultar_cleanpoints(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario.cleanpoints

@router.put("/{usuario_id}", response_model=UsuarioOut)
def actualizar_usuario(
    usuario_id: int, 
    usuario_data: dict, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    # Verificar que el usuario actual está actualizando su propio perfil
    if current_user.id != usuario_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para actualizar este usuario"
        )
    
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Actualizar campos permitidos
    for field, value in usuario_data.items():
        if hasattr(usuario, field) and field not in ['id', 'password_hash']:
            setattr(usuario, field, value)
    
    db.commit()
    db.refresh(usuario)
    return usuario

@router.post("/{usuario_id}/completar_curso/{curso_id}", response_model=UsuarioOut)
def completar_curso(
    usuario_id: int, 
    curso_id: int, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    # Verificar que el usuario actual está completando su propio curso
    if current_user.id != usuario_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para completar cursos de otro usuario"
        )
    
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    curso = db.query(Curso).filter(Curso.id == curso_id).first()
    if not usuario or not curso:
        raise HTTPException(status_code=404, detail="Usuario o curso no encontrado")
    
    # Otorgar CleanPoints por completar el curso
    cleanpoints_earned = 10
    usuario.cleanpoints += cleanpoints_earned
    db.commit()
    db.refresh(usuario)
    return usuario