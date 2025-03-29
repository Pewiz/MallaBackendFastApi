from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import crud, schemas, models

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/ramos/", response_model=schemas.RamoResponse)
def crear_ramo(ramo: schemas.RamoCreate, db: Session = Depends(get_db)):
    return crud.create_ramo(db, ramo)

@router.get("/ramos/", response_model=list[schemas.RamoResponse])
def listar_ramos(db: Session = Depends(get_db)):
    return db.query(models.Ramo).all()

@router.get("/carreras/{carrera_id}/ramos/", response_model=list[schemas.RamoResponse])
def listar_ramos_por_carrera(carrera_id: int, db: Session = Depends(get_db)):
    ramos = crud.get_ramos_por_carrera(db, carrera_id)
    if not ramos:
        raise HTTPException(status_code=404, detail="No se encontraron ramos para esta carrera")
    return ramos

