from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Curso(Base):
    __tablename__ = "cursos"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, unique=True, index=True)
    descripcion = Column(String)
    tema = Column(String)
    contenido = Column(String)  # Nuevo campo

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    cleanpoints = Column(Integer, default=0)
    total_recycled_items = Column(Integer, default=0)
    fecha_registro = Column(DateTime, default=datetime.utcnow)
    avatar = Column(String, nullable=True)
    recompensas = relationship("Recompensa", back_populates="usuario")

class Recompensa(Base):
    __tablename__ = "recompensas"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String)
    puntos_requeridos = Column(Integer, nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)

    usuario = relationship("Usuario", back_populates="recompensas")

class Producto(Base):
    __tablename__ = "productos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True, nullable=False)
    descripcion = Column(String, nullable=True)
    precio = Column(Float, nullable=False)
    categoria = Column(String, nullable=False)
    imagen = Column(String, nullable=True)
    stock = Column(Integer, nullable=True)
    disponible = Column(Integer, default=1)  # 1 = True, 0 = False
    puntos_requeridos = Column(Integer, nullable=True)

class Compra(Base):
    __tablename__ = "compras"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    precio_pagado = Column(Float, nullable=False)
    descuento_aplicado = Column(Integer, nullable=False)
    fecha = Column(DateTime, default=datetime.utcnow)

    usuario = relationship("Usuario")
    producto = relationship("Producto")
