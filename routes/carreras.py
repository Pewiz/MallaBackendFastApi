from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, Form, File
from sqlalchemy.orm import Session
from cloudinary_config import upload_image
from database import SessionLocal
import crud
from models import Carrera
import schemas
from crud import get_carrera_con_ramos, get_carreras
from schemas import CarreraCompletaResponse, CarreraSimpleResponse

router = APIRouter(prefix="/carreras", tags=["Carreras"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/carreras", response_model=CarreraCompletaResponse)
async def crear_carrera(
    nombre: str = Form(...),
    nombre_malla: str = Form(...),
    link_admision: str = Form(...),
    area: str = Form(...),
    url_image: UploadFile = File(None),
    db: Session = Depends(get_db)
):

    # Subir imagen si existe
    url_imagee = None
    if url_image:
        url_imagee = await upload_image(url_image)

    # Crear la carrera
    db_carrera = Carrera(
        nombre=nombre,
        nombre_malla=nombre_malla,
        link_admision=link_admision,
        area=area,
        url_image=url_imagee
    )

    db.add(db_carrera)
    db.commit()
    db.refresh(db_carrera)

    return db_carrera


@router.get("/carreras", response_model=list[CarreraSimpleResponse])
def obtener_carreras(db: Session = Depends(get_db)):
    return get_carreras(db)


@router.get("/carreras/{carrera_id}", response_model=CarreraCompletaResponse)
def obtener_carrera(carrera_id: int, db: Session = Depends(get_db)):
    return get_carrera_con_ramos(db, carrera_id)
