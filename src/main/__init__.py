from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.banco.database import engine, Base
from src.modelos import modelo_banco
from src.routes import ordens, auth, dashboard, motoristas

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["Autenticação"])
app.include_router(ordens.orden, prefix="/api/veiculos", tags=["Veículos"])
app.include_router(dashboard.orden, prefix="/api", tags=["Dashboard"])
app.include_router(motoristas.orden, prefix="/api/motoristas", tags=["Motoristas"])
