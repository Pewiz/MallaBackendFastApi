from sqlalchemy.orm import Session
from models import Carrera, Ramo, Prerequisito
from schemas import CarreraCreate, RamoCreate, PrerequisitoCreate

def create_carrera(db: Session, carrera: CarreraCreate):
    nueva_carrera = Carrera(nombre = carrera.nombre)
    db.add(nueva_carrera)
    db.commit()
    db.refresh(nueva_carrera)
    return nueva_carrera

def get_carreras(db: Session):
    return db.query(Carrera).all()

def create_ramo(db: Session, ramo: RamoCreate):
    nuevo_ramo = Ramo(**ramo.dict())
    db.add(nuevo_ramo)
    db.commit()
    db.refresh(nuevo_ramo)
    return nuevo_ramo

def get_ramos_por_carrera (db: Session, prereq: PrerequisitoCreate):
    nuevo_prereq = Prerequisito(**prereq.dict())
    db.add(nuevo_prereq)
    db.commit()
    db.refresh(nuevo_prereq)
    return nuevo_prereq

def get_prerequisitos(db: Session, ramo_id: int):
    return db.query(Prerequisito).filter(Prerequisito.ramo_id == ramo_id).all()

def get_ramos_desbloqueados(db: Session, requisito_id: int):
    return db.query(Prerequisito).filter(Prerequisito.requisito_id == requisito_id).all()
