from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import SessionLocal
import crud
import schemas

router = APIRouter(prefix="/prerequisitos", tags=["Prerequisitos"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.PrerequisitoBase)
def agregar_prerequisito(
    ramo_id: int = Query(...,
                         description="ID del ramo que tiene el requisito"),
    requisito_id: int = Query(...,
                              description="ID del ramo que es el requisito"),
    db: Session = Depends(get_db),
):
    prereq_data = schemas.PrerequisitoCreate(
        ramo_id=ramo_id, requisito_id=requisito_id)
    return crud.create_prerequisito(db, prereq_data)


@router.get("/ramos/{ramo_id}/prerequisitos/", response_model=list[schemas.PrerequisitoResponse])
def obtener_prerequisitos(ramo_id: int, db: Session = Depends(get_db)):
    prerequisitos = crud.get_prerequisitos(db, ramo_id)
    if not prerequisitos:
        raise HTTPException(
            status_code=404, detail="Este ramo no tiene prerequisitos")
    return prerequisitos


@router.get("/ramos/{requisito_id}/desbloquea/", response_model=list[schemas.RamosDesbloqueadosResponse])
def obtener_ramos_desbloqueados(requisito_id: int, db: Session = Depends(get_db)):
    desbloqueados = crud.get_ramos_desbloqueados(db, requisito_id)
    if not desbloqueados:
        raise HTTPException(
            status_code=404, detail="Este ramo no desbloquea ningún ramo")
    return desbloqueados
