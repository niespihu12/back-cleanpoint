#!/usr/bin/env python3
"""
Script para migrar la base de datos existente y agregar nuevos campos.
Ejecutar este script después de actualizar los modelos.
"""

import sqlite3
import os

def migrate_database():
    """Migra la base de datos existente para incluir nuevos campos."""
    
    db_path = "cursos.db"
    
    if not os.path.exists(db_path):
        print("Base de datos no encontrada. Creando nueva...")
        return
    
    print("Migrando base de datos...")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Verificar si la tabla usuarios existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='usuarios'")
        if cursor.fetchone():
            # Verificar si el campo email existe
            cursor.execute("PRAGMA table_info(usuarios)")
            columns = [column[1] for column in cursor.fetchall()]
            
            if 'email' not in columns:
                print("Agregando campo 'email' a la tabla usuarios...")
                cursor.execute("ALTER TABLE usuarios ADD COLUMN email TEXT")
                
            if 'password_hash' not in columns:
                print("Agregando campo 'password_hash' a la tabla usuarios...")
                cursor.execute("ALTER TABLE usuarios ADD COLUMN password_hash TEXT")
                
            if 'fecha_registro' not in columns:
                print("Agregando campo 'fecha_registro' a la tabla usuarios...")
                cursor.execute("ALTER TABLE usuarios ADD COLUMN fecha_registro DATETIME")
                
            if 'avatar' not in columns:
                print("Agregando campo 'avatar' a la tabla usuarios...")
                cursor.execute("ALTER TABLE usuarios ADD COLUMN avatar TEXT")
            
            # Verificar si la tabla productos existe y tiene el campo categoria
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='productos'")
            if cursor.fetchone():
                cursor.execute("PRAGMA table_info(productos)")
                product_columns = [column[1] for column in cursor.fetchall()]
                
                if 'categoria' not in product_columns:
                    print("Agregando campo 'categoria' a la tabla productos...")
                    cursor.execute("ALTER TABLE productos ADD COLUMN categoria TEXT")
                    
                if 'imagen' not in product_columns:
                    print("Agregando campo 'imagen' a la tabla productos...")
                    cursor.execute("ALTER TABLE productos ADD COLUMN imagen TEXT")
                    
                if 'stock' not in product_columns:
                    print("Agregando campo 'stock' a la tabla productos...")
                    cursor.execute("ALTER TABLE productos ADD COLUMN stock INTEGER")
                    
                if 'disponible' not in product_columns:
                    print("Agregando campo 'disponible' a la tabla productos...")
                    cursor.execute("ALTER TABLE productos ADD COLUMN disponible BOOLEAN DEFAULT 1")
                    
                if 'puntos_requeridos' not in product_columns:
                    print("Agregando campo 'puntos_requeridos' a la tabla productos...")
                    cursor.execute("ALTER TABLE productos ADD COLUMN puntos_requeridos INTEGER")
            
            # Verificar si la tabla cursos existe y tiene nuevos campos
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='cursos'")
            if cursor.fetchone():
                cursor.execute("PRAGMA table_info(cursos)")
                course_columns = [column[1] for column in cursor.fetchall()]
                
                if 'duracion_minutos' not in course_columns:
                    print("Agregando campo 'duracion_minutos' a la tabla cursos...")
                    cursor.execute("ALTER TABLE cursos ADD COLUMN duracion_minutos INTEGER")
                    
                if 'nivel' not in course_columns:
                    print("Agregando campo 'nivel' a la tabla cursos...")
                    cursor.execute("ALTER TABLE cursos ADD COLUMN nivel TEXT")
                    
                if 'imagen_url' not in course_columns:
                    print("Agregando campo 'imagen_url' a la tabla cursos...")
                    cursor.execute("ALTER TABLE cursos ADD COLUMN imagen_url TEXT")
            
            # Verificar si la tabla recompensas existe y tiene el campo imagen_url
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='recompensas'")
            if cursor.fetchone():
                cursor.execute("PRAGMA table_info(recompensas)")
                reward_columns = [column[1] for column in cursor.fetchall()]
                
                if 'imagen_url' not in reward_columns:
                    print("Agregando campo 'imagen_url' a la tabla recompensas...")
                    cursor.execute("ALTER TABLE recompensas ADD COLUMN imagen_url TEXT")
            
            # Crear tabla para progreso de cursos si no existe
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS curso_progreso (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    course_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    progress_percentage INTEGER DEFAULT 0,
                    completed BOOLEAN DEFAULT 0,
                    fecha_inicio DATETIME,
                    fecha_completado DATETIME,
                    FOREIGN KEY (course_id) REFERENCES cursos (id),
                    FOREIGN KEY (user_id) REFERENCES usuarios (id)
                )
            """)
            
            print("Migración completada exitosamente!")
            
        else:
            print("Tabla usuarios no encontrada. La base de datos será creada automáticamente.")
            
    except Exception as e:
        print(f"Error durante la migración: {e}")
        conn.rollback()
    finally:
        conn.commit()
        conn.close()

if __name__ == "__main__":
    migrate_database()
