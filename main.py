from fastapi import FastAPI
from routers import cursos, usuarios, recompensas, marketplace, compras, auth, qr
from models import Base
from database import engine
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Backend de CleanPoints", version="1.0.0")

# Incluir todos los routers
app.include_router(auth.router)
app.include_router(qr.router)
app.include_router(cursos.router)
app.include_router(usuarios.router)
app.include_router(recompensas.router)
app.include_router(marketplace.router)
app.include_router(compras.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
