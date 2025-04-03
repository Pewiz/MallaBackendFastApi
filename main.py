from fastapi import FastAPI
from database import engine, Base
import routes.carreras as carreras
import routes.ramos as ramos
import routes.requisitos as requisitos

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes cambiarlo a ["http://localhost:4321"] si quieres más seguridad
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permite todos los headers
)


@app.on_event("startup")
async def startup():
    """Se ejecuta cuando la API inicia."""
    Base.metadata.create_all(bind=engine)

# Definir rutas
app.include_router(carreras.router, prefix="/api")
app.include_router(ramos.router, prefix="/api")
app.include_router(requisitos.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "API funcionando correctamente 🚀"}
