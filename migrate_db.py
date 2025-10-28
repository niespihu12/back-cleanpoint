#!/usr/bin/env python3
"""
Script para migrar la base de datos existente y agregar nuevos campos.
Ejecutar este script después de actualizar los modelos.
"""

import os
from database import DATABASE_URL, engine, Base

"""
Script para migrar/asegurar la base de datos.

Si se usa SQLite, mantiene la lógica antigua para alteraciones sencillas via sqlite3.
Si se usa otra DB (p. ej. Postgres), usa SQLAlchemy `Base.metadata.create_all` para
crear las tablas que falten (no hace migraciones complejas).
"""

def migrate_database():
    if DATABASE_URL.startswith("sqlite"):
        # Si es sqlite, reusar la implementación antigua (más específica)
        try:
            import sqlite3
            db_path = DATABASE_URL.replace("sqlite:///", "")
            if not os.path.exists(db_path):
                print("Base de datos SQLite no encontrada. Creando nueva con modelos...")
                Base.metadata.create_all(bind=engine)
                print("✅ Base de datos SQLite creada.")
                return

            print("Migrando base de datos SQLite (operaciones limitadas)...")
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            # Aquí pueden conservarse los cambios específicos que se hacían antes
            # para añadir columnas existentes. Para simplicidad, mantenemos las
            # comprobaciones de columnas mínimas.
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
                print("✅ No se requieren cambios adicionales en usuarios.")
            conn.close()
            return
        except Exception as e:
            print(f"Error durante migración SQLite: {e}")
            return

    # Para otras DBs (Postgres, MySQL, etc.) usar SQLAlchemy para crear tablas
    print("Usando SQLAlchemy para crear/asegurar tablas en la base de datos remota...")
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Tablas creadas/aseguradas en la base de datos remota.")
    except Exception as e:
        print(f"❌ Error creando tablas en la base de datos remota: {e}")


if __name__ == "__main__":
    migrate_database()
