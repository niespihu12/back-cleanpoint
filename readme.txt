# API de BackEnd - CleanPoint

## Descripción

Esta API permite gestionar cursos ambientales, usuarios, recompensas, un marketplace de productos y el historial de compras, integrando un sistema de puntos ("cleanpoints") para incentivar la participación y el canje de productos con descuentos.

---

## Características principales

- **Gestión de cursos:** Crear, listar, actualizar y eliminar cursos ambientales.
- **Gestión de usuarios:** Registro de usuarios, consulta y actualización de cleanpoints.
- **Recompensas:** Listado, creación y canje de recompensas usando cleanpoints.
- **Marketplace:** CRUD de productos, canje de productos con descuento según cleanpoints.
- **Compras:** Registro de compras y consulta de historial por usuario.

---

## Instalación

1. Clona el repositorio:
   ```
   git clone https://github.com/Benji-An/Back-CleanPoint.git
   cd Back-CleanPoint
   ```

2. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```

3. Configura la base de datos en `database.py` según tus necesidades.

4. Ejecuta el servidor:
   ```
   uvicorn cursos.main:app --reload
   ```

---

## Estructura del proyecto

```
cursos/
│
├── main.py
├── models.py
├── schemas.py
├── database.py
├── routers/
│   ├── cursos.py
│   ├── usuarios.py
│   ├── recompensas.py
│   ├── marketplace.py
│   └── compras.py
└── ...
```

---

## Endpoints principales

- `/cursos/`  
  CRUD de cursos.

- `/usuarios/`  
  Registro de usuarios, consulta de cleanpoints, completar cursos.

- `/recompensas/`  
  Listado, creación y canje de recompensas.

- `/marketplace/productos/`  
  CRUD de productos del marketplace.

- `/marketplace/canjear/`  
  Calcular descuento y precio final para canje de productos.

- `/compras/`  
  Registrar compras y consultar historial de compras por usuario.

---

## Uso de la API

Una vez iniciado el servidor, accede a la documentación interactiva en:  
[http://localhost:8000/docs](http://localhost:8000/docs)

---

## Notas

- Los cleanpoints se obtienen al completar cursos y se pueden usar para obtener descuentos en el marketplace o reclamar recompensas.
- El descuento en el marketplace es configurable y depende de los cleanpoints del usuario.
- El historial de compras permite a cada usuario ver sus transacciones y descuentos aplicados.

---