from fastapi import FastAPI
from database import engine, Base 
import routes.carreras as carreras

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(carreras.router, prefix="/api")
