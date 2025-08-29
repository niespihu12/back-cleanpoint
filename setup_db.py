#!/usr/bin/env python3
"""
Script simple para configurar la base de datos desde cero.
"""

import os
import sqlite3

def setup_database():
    """Configura la base de datos desde cero."""
    # Si la base de datos ya existe, intentar migrar (añadir columnas nuevas) en lugar de eliminar
    db_exists = os.path.exists('cursos.db')
    if db_exists:
        print("⚠️  Base de datos existente detectada: ejecutando migraciones ligeras si es necesario...")
        conn = sqlite3.connect('cursos.db')
        cursor = conn.cursor()

        # Verificar si la columna total_recycled_items existe en la tabla usuarios
        cursor.execute("PRAGMA table_info('usuarios')")
        cols = [row[1] for row in cursor.fetchall()]
        if 'total_recycled_items' not in cols:
            print("➡️  Añadiendo columna 'total_recycled_items' a la tabla 'usuarios'...")
            try:
                cursor.execute("ALTER TABLE usuarios ADD COLUMN total_recycled_items INTEGER DEFAULT 0")
                conn.commit()
                print("✅ Columna 'total_recycled_items' añadida correctamente.")
            except Exception as e:
                print(f"❌ Error al añadir columna: {e}")
        else:
            print("✅ La columna 'total_recycled_items' ya existe. No se requiere migración.")

        conn.close()
        return

    print("🗄️  Creando nueva base de datos...")
    conn = sqlite3.connect('cursos.db')
    cursor = conn.cursor()
    
    try:
        # Crear tabla de usuarios con todos los campos necesarios
        cursor.execute('''
            CREATE TABLE usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                cleanpoints INTEGER DEFAULT 0,
                total_recycled_items INTEGER DEFAULT 0,
                fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
                avatar TEXT
            )
        ''')
        
        # Crear tabla de cursos
        cursor.execute('''
            CREATE TABLE cursos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT UNIQUE NOT NULL,
                descripcion TEXT NOT NULL,
                tema TEXT NOT NULL,
                contenido TEXT NOT NULL,
                duracion_minutos INTEGER DEFAULT 30,
                nivel TEXT DEFAULT 'principiante',
                imagen_url TEXT
            )
        ''')
        
        # Crear tabla de productos
        cursor.execute('''
            CREATE TABLE productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT UNIQUE NOT NULL,
                descripcion TEXT,
                precio REAL NOT NULL,
                categoria TEXT NOT NULL,
                imagen TEXT NOT NULL,
                stock INTEGER DEFAULT 10,
                disponible BOOLEAN DEFAULT 1,
                puntos_requeridos INTEGER DEFAULT 100
            )
        ''')
        
        # Crear tabla de recompensas
        cursor.execute('''
            CREATE TABLE recompensas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                puntos_requeridos INTEGER NOT NULL,
                usuario_id INTEGER,
                imagen_url TEXT,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
            )
        ''')
        
        # Crear tabla de compras
        cursor.execute('''
            CREATE TABLE compras (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                producto_id INTEGER NOT NULL,
                precio_pagado REAL NOT NULL,
                descuento_aplicado INTEGER DEFAULT 0,
                fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id),
                FOREIGN KEY (producto_id) REFERENCES productos (id)
            )
        ''')
        
        # Crear tabla de progreso de cursos
        cursor.execute('''
            CREATE TABLE curso_progreso (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                progress_percentage INTEGER DEFAULT 0,
                completed BOOLEAN DEFAULT 0,
                fecha_inicio DATETIME DEFAULT CURRENT_TIMESTAMP,
                fecha_completado DATETIME,
                FOREIGN KEY (course_id) REFERENCES cursos (id),
                FOREIGN KEY (user_id) REFERENCES usuarios (id)
            )
        ''')
        
        print("✅ Base de datos creada exitosamente!")
        print("📋 Tablas creadas:")
        print("   - usuarios (con email, password_hash, etc.)")
        print("   - cursos")
        print("   - productos")
        print("   - recompensas")
        print("   - compras")
        print("   - curso_progreso")
        
    except Exception as e:
        print(f"❌ Error creando la base de datos: {e}")
        conn.rollback()
    finally:
        conn.commit()
        conn.close()

if __name__ == "__main__":
    setup_database()
