# 🚀 Backend de CleanPoints - FastAPI

Este es el backend de la aplicación CleanPoints, construido con FastAPI y SQLAlchemy.

## 🏗️ Estructura del Proyecto

```
cursos/
├── main.py                 # Aplicación principal FastAPI
├── database.py             # Configuración de la base de datos
├── models.py               # Modelos SQLAlchemy
├── schemas.py              # Esquemas Pydantic
├── requirements.txt        # Dependencias Python
├── migrate_db.py           # Script de migración de BD
├── start_backend.py        # Script de inicio automático
├── README_BACKEND.md       # Este archivo
└── routers/                # Routers de la API
    ├── auth.py             # Autenticación (login, registro)
    ├── qr.py               # Validación QR + IA
    ├── usuarios.py         # Gestión de usuarios
    ├── cursos.py           # Gestión de cursos
    ├── marketplace.py      # Gestión de productos
    ├── compras.py          # Gestión de compras
    └── recompensas.py      # Gestión de recompensas
```

## 🚀 Inicio Rápido

### Opción 1: Inicio Automático (Recomendado)
```bash
cd cursos
python start_backend.py
```

### Opción 2: Inicio Manual
```bash
cd cursos

# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Migrar base de datos
python migrate_db.py

# 3. Iniciar servidor
python -m uvicorn main:app --reload --host 127.0.0.1 --port 5000
```

## 🌐 Endpoints Disponibles

### 🔐 Autenticación (`/auth`)
- `POST /auth/register` - Registro de usuario
- `POST /auth/login` - Inicio de sesión
- `POST /auth/logout` - Cerrar sesión
- `POST /auth/refresh` - Renovar token
- `GET /auth/me` - Información del usuario actual

### 📱 Validación QR (`/qr`)
- `POST /qr/validate` - Validar reciclaje con IA

### 👥 Usuarios (`/usuarios`)
- `GET /usuarios/{id}` - Obtener usuario
- `PUT /usuarios/{id}` - Actualizar usuario
- `GET /usuarios/{id}/cleanpoints` - Consultar CleanPoints
- `POST /usuarios/{id}/completar_curso/{curso_id}` - Completar curso

### 📚 Cursos (`/cursos`)
- `GET /cursos/` - Listar cursos
- `GET /cursos/{id}` - Obtener curso específico

### 🛍️ Marketplace (`/marketplace`)
- `GET /marketplace/productos/` - Listar productos
- `GET /marketplace/productos/{id}` - Obtener producto

### 🛒 Compras (`/compras`)
- `POST /compras/` - Crear compra
- `GET /compras/` - Listar compras

### 🏆 Recompensas (`/recompensas`)
- `GET /recompensas/` - Listar recompensas

## 🔧 Configuración

### Variables de Entorno
Crea un archivo `.env` en el directorio `cursos/`:

```env
# Base de datos
# Por defecto en desarrollo usamos SQLite. Para usar Postgres establezca:
# DATABASE_URL=postgresql://USER:PASSWORD@HOST:PORT/DBNAME
DATABASE_URL=sqlite:///./cursos.db

# JWT
SECRET_KEY=tu_clave_secreta_super_segura_aqui_cambiala_en_produccion
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Aplicación
DEBUG=True
ENVIRONMENT=development
```

### Base de Datos
- **SQLite**: Base de datos por defecto (desarrollo)
- **PostgreSQL/MySQL**: Para producción (cambiar `DATABASE_URL`).

Ejemplo de `DATABASE_URL` para PostgreSQL:

```
postgresql://mi_usuario:mi_contraseña@localhost:5432/mi_basedatos
```

Si usas Postgres, instala dependencias y luego ejecuta:

```bash
# Instalar dependencias (incluye psycopg2-binary)
pip install -r requirements.txt

# Crear/asegurar tablas en la DB remota
python setup_db.py
```

## 📊 Migración de Base de Datos

El script `migrate_db.py` automáticamente:
- Agrega nuevos campos a las tablas existentes
- Crea nuevas tablas si es necesario
- Mantiene los datos existentes

## 🔒 Seguridad

- **JWT**: Autenticación basada en tokens
- **bcrypt**: Hashing seguro de contraseñas
- **CORS**: Configurado para el frontend Next.js
- **Validación**: Esquemas Pydantic para todos los endpoints

## 🧪 Testing

### Documentación Interactiva
- **Swagger UI**: http://127.0.0.1:5000/docs
- **ReDoc**: http://127.0.0.1:5000/redoc

### Ejemplo de Registro
```bash
curl -X POST "http://127.0.0.1:5000/auth/register" \
     -H "Content-Type: application/json" \
     -d '{
       "nombre": "Usuario Test",
       "email": "test@example.com",
       "password": "password123"
     }'
```

## 🚨 Solución de Problemas

### Error 404 en `/auth/register`
- Verificar que `auth.router` esté incluido en `main.py`
- Verificar que el archivo `routers/auth.py` exista
- Reiniciar el servidor después de cambios

### Error de Dependencias
```bash
pip install --upgrade -r requirements.txt
```

### Error de Base de Datos
```bash
python migrate_db.py
```

### Puerto en Uso
```bash
# Cambiar puerto en start_backend.py o usar:
python -m uvicorn main:app --reload --port 5001
```

## 📝 Notas de Desarrollo

- **Hot Reload**: El servidor se reinicia automáticamente al cambiar archivos
- **Logs**: Los logs aparecen en la consola
- **Base de Datos**: Se crea automáticamente si no existe
- **CORS**: Configurado para `localhost:3000` (Next.js)

## 🔄 Actualizaciones

Para actualizar el backend:
1. Detener el servidor (Ctrl+C)
2. Ejecutar `python migrate_db.py` si hay cambios en modelos
3. Reiniciar con `python start_backend.py`

## 📞 Soporte

Si encuentras problemas:
1. Verificar logs del servidor
2. Ejecutar migración de base de datos
3. Verificar que todas las dependencias estén instaladas
4. Revisar la documentación de la API en `/docs`
