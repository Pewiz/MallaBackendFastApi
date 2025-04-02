from fastapi import FastAPI
from database import engine, Base
import routes.carreras as carreras
import routes.ramos as ramos
import routes.requisitos as requisitos

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(carreras.router, prefix="/api")
app.include_router(ramos.router, prefix="/api")
app.include_router(requisitos.router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "API funcionando correctamente 🚀"}
