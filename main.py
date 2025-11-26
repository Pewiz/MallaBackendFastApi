from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import engine, Base
import routes.carreras as carreras
import routes.ramos as ramos
import routes.requisitos as requisitos

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Maneja el ciclo de vida de la aplicación."""
    # Startup
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown (si necesitas hacer algo al cerrar la app)

app = FastAPI(lifespan=lifespan)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://malla-ulagos.netlify.app", "http://localhost:4321"],  # Puedes cambiarlo a ["http://localhost:4321"] si quieres más seguridad
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permite todos los headers
)

# Definir rutas
app.include_router(carreras.router, prefix="/api")
app.include_router(ramos.router, prefix="/api")
app.include_router(requisitos.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "API funcionando correctamente 🚀"}
