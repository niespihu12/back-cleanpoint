from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# ===== AUTHENTICATION SCHEMAS =====
class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    nombre: str
    email: str
    password: str

class AuthResponse(BaseModel):
    user: "UsuarioOut"
    token: str
    refresh_token: Optional[str] = None

# ===== USER SCHEMAS =====
class UsuarioBase(BaseModel):
    nombre: str
    email: str

class UsuarioCreate(BaseModel):
    nombre: str
    email: str
    password: str

class UsuarioOut(BaseModel):
    id: int
    nombre: str
    email: str
    cleanpoints: int
    total_recycled_items: int = 0
    fecha_registro: Optional[datetime] = None
    avatar: Optional[str] = None
    
    class Config:
        orm_mode = True

# ===== COURSE SCHEMAS =====
class CursoBase(BaseModel):
    titulo: str
    descripcion: str
    tema: str
    contenido: str  # Nuevo campo

class CursoCreate(CursoBase):
    # Permitir ambos nombres para compatibilidad: imagen_url (nuevo) o imagen (antiguo)
    imagen_url: Optional[str] = None
    imagen: Optional[str] = None
    duracion_minutos: Optional[int] = None
    nivel: Optional[str] = None

class CursoOut(CursoBase):
    id: int
    duracion_minutos: Optional[int] = None
    nivel: Optional[str] = None
    imagen_url: Optional[str] = None

    class Config:
        orm_mode = True

# ===== COURSE PROGRESS SCHEMAS =====
class CourseProgress(BaseModel):
    course_id: int
    user_id: int
    progress_percentage: int
    completed: bool
    fecha_inicio: Optional[datetime] = None
    fecha_completado: Optional[datetime] = None

    class Config:
        orm_mode = True

# ===== MARKETPLACE SCHEMAS =====
class ProductoBase(BaseModel):
    nombre: str
    descripcion: str | None = None
    precio: float
    categoria: str
    imagen: str
    stock: Optional[int] = None
    disponible: Optional[bool] = True
    puntos_requeridos: Optional[int] = None

class ProductoCreate(ProductoBase):
    pass

class ProductoOut(ProductoBase):
    id: int
    class Config:
        orm_mode = True

# ===== PURCHASE SCHEMAS =====
class CompraBase(BaseModel):
    usuario_id: int
    producto_id: int
    precio_pagado: float
    descuento_aplicado: int

class CompraCreate(CompraBase):
    pass

class CompraOut(CompraBase):
    id: int
    fecha: datetime
    producto: Optional[ProductoOut] = None
    usuario_cleanpoints: Optional[int] = None

    class Config:
        orm_mode = True


class CompraResponse(BaseModel):
    compra: CompraOut
    new_balance: int

    class Config:
        orm_mode = True

# ===== REWARDS SCHEMAS =====
class RecompensaBase(BaseModel):
    nombre: str
    puntos_requeridos: int

class RecompensaCreate(RecompensaBase):
    pass

class RecompensaOut(BaseModel):
    id: int
    nombre: str
    descripcion: str | None = None
    puntos_requeridos: int
    usuario_id: int | None = None
    imagen_url: Optional[str] = None

    class Config:
        orm_mode = True

# ===== QR VALIDATION SCHEMAS =====
class QRValidationRequest(BaseModel):
    qr_code: str
    image_data: str  # base64 encoded image
    user_id: int

class QRValidationResponse(BaseModel):
    success: bool
    valid: bool
    cleanpoints_earned: int
    message: str
    timestamp: datetime

# ===== API RESPONSE SCHEMAS =====
class ApiResponse(BaseModel):
    data: dict
    message: Optional[str] = None
    success: bool = True

class ApiError(BaseModel):
    detail: str
    status_code: int
    timestamp: Optional[datetime] = None
