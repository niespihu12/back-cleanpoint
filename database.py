from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Cargar variables definidas en un archivo .env si existe
load_dotenv()

# Configuración de la base de datos: usar la variable de entorno DATABASE_URL.
# Ejemplos:
#  - SQLite (desarrollo): sqlite:///./cursos.db
#  - PostgreSQL: postgresql://user:password@host:port/dbname
# Nota: soportamos que la variable pueda venir con comillas o espacios alrededor.
raw_db = os.getenv("DATABASE_URL", "sqlite:///./cursos.db")
# Limpiar comillas y espacios residuales si el .env contiene: DATABASE_URL = "..."
DATABASE_URL = raw_db.strip().strip('"').strip("'")

# Crear engine con parámetros adecuados según el driver
if DATABASE_URL.startswith("sqlite"):
    # SQLite necesita check_same_thread cuando se usa con SQLAlchemy en entornos síncronos
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    # Para bases de datos remotas (Postgres, MySQL, etc.) habilitamos pool_pre_ping
    # para reconectar conexiones estaleadas automáticamente.
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Crear sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos (compartida con models.py)
Base = declarative_base()
