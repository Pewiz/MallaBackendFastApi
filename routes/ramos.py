from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import SessionLocal
import crud
import schemas
import models

router = APIRouter(prefix="/ramos", tags=["Ramos"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.RamoResponse)
def crear_ramo(
    ramo_nombre: str = Query(..., description="Nombre del ramo"),
    semestre: int = Query(..., description="Semestre del ramo"),
    carreras_ids: List[int] = Query(..., description="IDs de las carreras"),
    db: Session = Depends(get_db)
):
    ramo = schemas.RamoCreate(nombre=ramo_nombre, semestre=semestre)
    return crud.create_ramo(db, ramo, carreras_ids, semestre)


@router.get("/", response_model=list[schemas.RamoResponse])
def listar_ramos(db: Session = Depends(get_db)):
    return db.query(models.Ramo).all()


@router.get("/carreras/{carrera_id}/ramos/", response_model=list[schemas.RamoResponse])
def listar_ramos_por_carrera(carrera_id: int, db: Session = Depends(get_db)):
    ramos = crud.get_ramos_por_carrera(db, carrera_id)
    if not ramos:
        raise HTTPException(
            status_code=404, detail="No se encontraron ramos para esta carrera")
    return ramos
