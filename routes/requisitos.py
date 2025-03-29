from fastapi import APIRouter, Depends, HTTPException
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


@router.post("/prerequisitos/", response_model=schemas.PrerequisitoBase)
def agregar_prerequisito(prereq: schemas.PrerequisitoCreate, db: Session = Depends(get_db)):
    return crud.create_prerequisito(db, prereq)

@router.get("/ramos/{ramo_id}/prerequisitos/", response_model=list[schemas.PrerequisitoBase])
def obtener_prerequisitos(ramo_id: int, db: Session = Depends(get_db)):
    prerequisitos = crud.get_prerequisitos(db, ramo_id)
    if not prerequisitos:
        raise HTTPException(status_code=404, detail="Este ramo no tiene prerequisitos")
    return prerequisitos

@router.get("/ramos/{requisito_id}/desbloquea/", response_model=list[schemas.PrerequisitoBase])
def obtener_ramos_desbloqueados(requisito_id: int, db: Session = Depends(get_db)):
    desbloqueados = crud.get_ramos_desbloqueados(db, requisito_id)
    if not desbloqueados:
        raise HTTPException(status_code=404, detail="Este ramo no desbloquea ningún ramo")
    return desbloqueados
    