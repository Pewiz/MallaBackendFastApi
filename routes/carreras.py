from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import SessionLocal
import crud
import schemas
from crud import get_carrera_con_ramos
from schemas import CarreraResponse

router = APIRouter(prefix="/carreras", tags=["Carreras"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.CarreraResponse)
def crear_carrera(
    nombre: str = Query(..., description="Nombre de la carrera"),
    db: Session = Depends(get_db)
):
    carrera = schemas.CarreraCreate(nombre=nombre)
    return crud.create_carrera(db, carrera)


@router.get("/", response_model=list[schemas.CarreraResponse])
def listar_carrera(db: Session = Depends(get_db)):
    return crud.get_carreras(db)


@router.get("/{carrera_id}", response_model=CarreraResponse)
def obtener_carrera(carrera_id: int, db: Session = Depends(get_db)):
    carrera_data = get_carrera_con_ramos(db, carrera_id)
    if not carrera_data:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")
    return carrera_data
