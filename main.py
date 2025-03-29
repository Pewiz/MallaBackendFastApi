from fastapi import FastAPI
from database import engine, Base 
import routes.carreras as carreras
import routes.ramos as ramos

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(carreras.router, prefix="/api")
app.include_router(ramos.router, prefix="/api")