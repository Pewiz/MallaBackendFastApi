from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import SessionLocal
import crud, schemas

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/carreras/", response_model=schemas.CarreraResponse)
def crear_carrera(
    nombre: str = Query(..., description="Nombre de la carrera"),
    db: Session = Depends(get_db)
):
    carrera = schemas.CarreraCreate(nombre=nombre)
    return crud.create_carrera(db, carrera)

@router.get("/carreras/", response_model=list[schemas.CarreraResponse])
def listar_carrera(db: Session = Depends(get_db)):
    return crud.get_carreras(db)

