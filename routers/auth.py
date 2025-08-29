from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import jwt
import bcrypt
from typing import Optional

from models import Usuario
from schemas import LoginRequest, RegisterRequest, AuthResponse, UsuarioOut
from database import SessionLocal

router = APIRouter(prefix="/auth", tags=["Autenticación"])

# Configuración JWT
SECRET_KEY = "tu_clave_secreta_super_segura_aqui_cambiala_en_produccion"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

security = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_password_hash(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = db.query(Usuario).filter(Usuario.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

@router.post("/register", response_model=AuthResponse)
def register(user_data: RegisterRequest, db: Session = Depends(get_db)):
    # Verificar si el email ya existe
    existing_user = db.query(Usuario).filter(Usuario.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )
    
    # Verificar si el nombre ya existe
    existing_name = db.query(Usuario).filter(Usuario.nombre == user_data.nombre).first()
    if existing_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de usuario ya está en uso"
        )
    
    # Crear nuevo usuario
    hashed_password = get_password_hash(user_data.password)
    db_user = Usuario(
        nombre=user_data.nombre,
        email=user_data.email,
        password_hash=hashed_password,
        cleanpoints=0,
        fecha_registro=datetime.utcnow()
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Crear token de acceso
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(db_user.id)}, expires_delta=access_token_expires
    )
    
    # Crear respuesta
    user_out = UsuarioOut(
        id=db_user.id,
        nombre=db_user.nombre,
        email=db_user.email,
        cleanpoints=db_user.cleanpoints,
        fecha_registro=db_user.fecha_registro,
        avatar=db_user.avatar
    )
    
    return AuthResponse(
        user=user_out,
        token=access_token,
        refresh_token=None
    )

@router.post("/login", response_model=AuthResponse)
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    # Buscar usuario por email
    user = db.query(Usuario).filter(Usuario.email == credentials.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos"
        )
    
    # Verificar contraseña
    if not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos"
        )
    
    # Crear token de acceso
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    
    # Crear respuesta
    user_out = UsuarioOut(
        id=user.id,
        nombre=user.nombre,
        email=user.email,
        cleanpoints=user.cleanpoints,
        fecha_registro=user.fecha_registro,
        avatar=user.avatar
    )
    
    return AuthResponse(
        user=user_out,
        token=access_token,
        refresh_token=None
    )

@router.post("/refresh")
def refresh_token(current_user: Usuario = Depends(get_current_user)):
    # Crear nuevo token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(current_user.id)}, expires_delta=access_token_expires
    )
    
    return {"token": access_token}

@router.post("/logout")
def logout():
    # En JWT, el logout se maneja del lado del cliente eliminando el token
    # Aquí podrías implementar una lista negra de tokens si es necesario
    return {"message": "Sesión cerrada exitosamente"}

@router.get("/me", response_model=UsuarioOut)
def get_current_user_info(current_user: Usuario = Depends(get_current_user)):
    return UsuarioOut(
        id=current_user.id,
        nombre=current_user.nombre,
        email=current_user.email,
        cleanpoints=current_user.cleanpoints,
        fecha_registro=current_user.fecha_registro,
        avatar=current_user.avatar
    )
