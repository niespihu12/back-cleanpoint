from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from models import Compra, Usuario, Producto
from schemas import CompraOut
from database import SessionLocal

router = APIRouter(prefix="/compras", tags=["Compras"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def calcular_descuento(cleanpoints: int, puntos_por_descuento: int = 10, max_descuento: int = 50) -> int:
    return min(cleanpoints // puntos_por_descuento, max_descuento)

from schemas import CompraOut, CompraResponse


@router.post("/", response_model=CompraResponse)
def comprar_producto(
    usuario_id: int = Body(..., embed=True),
    producto_id: int = Body(..., embed=True),
    db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not usuario or not producto:
        raise HTTPException(status_code=404, detail="Usuario o producto no encontrado")
    # Para comportamiento esperado por el cliente: descontar el precio del producto
    # (sin descuentos automáticos). Si se desea soporte de descuentos, agregar
    # lógica controlada explícitamente.
    precio_final = float(producto.precio)

    # Verificar que el usuario tenga saldo suficiente
    puntos_a_descontar = int(round(precio_final))
    current_points = usuario.cleanpoints or 0
    if current_points < puntos_a_descontar:
        raise HTTPException(status_code=400, detail="No tienes suficientes CleanPoints para esta compra")

    # Crear la compra y descontar los CleanPoints del usuario en una sola transacción
    compra = Compra(
        usuario_id=usuario_id,
        producto_id=producto_id,
        precio_pagado=round(precio_final, 2),
        descuento_aplicado=0
    )

    # Descontar los puntos del usuario (redondear a entero)
    usuario.cleanpoints = max(0, current_points - puntos_a_descontar)

    db.add(compra)
    db.add(usuario)
    db.commit()
    db.refresh(compra)
    db.refresh(usuario)

    return {"compra": compra, "new_balance": usuario.cleanpoints}

@router.get("/historial/{usuario_id}", response_model=list[CompraOut])
def historial_compras(usuario_id: int, db: Session = Depends(get_db)):
    return db.query(Compra).filter(Compra.usuario_id == usuario_id).order_by(Compra.fecha.desc()).all()