from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from models import Producto, Usuario
from schemas import ProductoCreate, ProductoOut
from database import SessionLocal

router = APIRouter(prefix="/marketplace", tags=["Marketplace"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def calcular_descuento(cleanpoints: int, puntos_por_descuento: int = 10, max_descuento: int = 50) -> int:
    return min(cleanpoints // puntos_por_descuento, max_descuento)

@router.post("/productos/", response_model=ProductoOut)
def crear_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    if db.query(Producto).filter(Producto.nombre == producto.nombre).first():
        raise HTTPException(status_code=400, detail="Ya existe un producto con ese nombre")
    db_producto = Producto(**producto.dict())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

@router.get("/productos/", response_model=list[ProductoOut])
def listar_productos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Producto).offset(skip).limit(limit).all()

@router.get("/productos/{producto_id}", response_model=ProductoOut)
def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@router.put("/productos/{producto_id}", response_model=ProductoOut)
def actualizar_producto(producto_id: int, producto: ProductoCreate, db: Session = Depends(get_db)):
    db_producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    for key, value in producto.dict().items():
        setattr(db_producto, key, value)
    db.commit()
    db.refresh(db_producto)
    return db_producto

@router.delete("/productos/{producto_id}", response_model=dict)
def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    db_producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db.delete(db_producto)
    db.commit()
    return {"detail": "Producto eliminado exitosamente"}

@router.post("/canjear/", response_model=dict)
def canjear_marketplace(
    usuario_id: int = Body(..., embed=True),
    producto_id: int = Body(..., embed=True),
    precio_base: float = Body(..., embed=True),
    puntos_por_descuento: int = 10,
    max_descuento: int = 50,
    db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    descuento = calcular_descuento(usuario.cleanpoints, puntos_por_descuento, max_descuento)
    precio_final = precio_base * (1 - descuento / 100)
    return {
        "usuario_id": usuario_id,
        "producto_id": producto_id,
        "cleanpoints_usuario": usuario.cleanpoints,
        "precio_base": precio_base,
        "descuento_aplicado": f"{descuento}%",
        "precio_final": round(precio_final, 2),
        "detalle": f"Descuento de {descuento}% aplicado por {usuario.cleanpoints} cleanpoints"
    }