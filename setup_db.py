#!/usr/bin/env python3
"""
Script simple para configurar la base de datos desde cero.
"""

import os
from urllib.parse import urlparse

"""
Script para configurar la base de datos desde cero.

Soporta dos modos:
 - SQLite (por defecto): se comporta como antes y crea/actualiza cursos.db
 - PostgreSQL (o cualquier DB soportada por SQLAlchemy): usa SQLAlchemy
   para crear tablas basadas en los modelos (Base.metadata.create_all).

Usar la variable de entorno DATABASE_URL para señalar la DB.
Ejemplo Postgres: postgresql://user:password@localhost:5432/mi_db
"""

from database import DATABASE_URL, engine, Base

def setup_database():
    # Si usamos SQLite, intentamos mantener la lógica existente para migraciones ligeras
    if DATABASE_URL.startswith("sqlite"):
        # Extraer ruta del archivo sqlite (sqlite:///./cursos.db o sqlite:///cursos.db)
        path = DATABASE_URL.replace("sqlite:///", "")
        db_exists = os.path.exists(path)
        if db_exists:
            print("⚠️  Base de datos SQLite existente detectada: ejecutando migraciones ligeras si es necesario...")
            # Reusar migrate_db.py behavior (import y ejecutar)
            try:
                import migrate_db
                migrate_db.migrate_database()
            except Exception as e:
                print(f"❌ Error al ejecutar migraciones SQLite: {e}")
            return

        # Si no existe, crear tablas usando SQLAlchemy (más simple y consistente)
        print("🗄️  Creando nueva base de datos SQLite usando SQLAlchemy...")
        Base.metadata.create_all(bind=engine)
        print("✅ Base de datos SQLite creada exitosamente con tablas desde modelos.")
        return

    # Para PostgreSQL u otras DBs, usar SQLAlchemy para crear tablas faltantes
    print("🔌 DATABASE_URL detectada para DB remota. Creando/asegurando tablas con SQLAlchemy...")
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Tablas creadas/aseguradas en la base de datos remota.")
    except Exception as e:
        print(f"❌ Error creando tablas en la base de datos remota: {e}")


if __name__ == "__main__":
    setup_database()
