from fastapi import HTTPException
from sqlalchemy.orm import Session, aliased, joinedload
from models import Carrera, Ramo, Prerequisito
from schemas import CarreraCreate, RamoCreate, PrerequisitoCreate, CarreraResponse, RamoResponse

RamoRequisito = aliased(Ramo)

def create_carrera(db: Session, carrera: CarreraCreate):
    nueva_carrera = Carrera(nombre=carrera.nombre)
    db.add(nueva_carrera)
    db.commit()
    db.refresh(nueva_carrera)
    return nueva_carrera


def get_carrera_con_ramos(db: Session, carrera_id: int):
    # Consulta principal con todas las relaciones
    carrera = db.query(Carrera).options(
        joinedload(Carrera.ramos).subqueryload(Ramo.prerequisitos),
        joinedload(Carrera.ramos).subqueryload(Ramo.desbloquea)
    ).filter(Carrera.id == carrera_id).first()
    
    if not carrera:
        return None
    
    # Mapeo de todos los ramos para evitar consultas adicionales
    todos_ramos = {r.id: r.nombre for r in db.query(Ramo.id, Ramo.nombre).all()}
    
    # Procesar ramos con relaciones
    ramos_procesados = []
    for ramo in carrera.ramos:
        ramo_data = {
            "id": ramo.id,
            "nombre": ramo.nombre,
            "semestre": ramo.semestre,
            "prev": [
                todos_ramos[p.requisito_id]
                for p in ramo.prerequisitos
                if p.requisito_id in todos_ramos
            ],
            "next": [
                todos_ramos[d.ramo_id]
                for d in ramo.desbloquea
                if d.ramo_id in todos_ramos
            ],
            "carreras": None
        }
        ramos_procesados.append(ramo_data)
    
    return {
        "id": carrera.id,
        "nombre": carrera.nombre,
        "ramos": ramos_procesados
    }

def get_carreras(db: Session):
    # Consulta principal con todas las relaciones necesarias
    carreras = db.query(Carrera).options(
        joinedload(Carrera.ramos).subqueryload(Ramo.prerequisitos),
        joinedload(Carrera.ramos).subqueryload(Ramo.desbloquea)
    ).all()
    
    # Obtenemos todos los ramos existentes en un diccionario
    todos_ramos = {r.id: r.nombre for r in db.query(Ramo.id, Ramo.nombre).all()}
    
    return [
        CarreraResponse(
            id=c.id,
            nombre=c.nombre,
            ramos=[
                RamoResponse(
                    id=r.id,
                    nombre=r.nombre,
                    semestre=r.semestre,
                    carreras=None,
                    prev=[
                        todos_ramos[p.requisito_id]
                        for p in r.prerequisitos
                        if p.requisito_id in todos_ramos
                    ],
                    next=[
                        todos_ramos[d.ramo_id]
                        for d in r.desbloquea
                        if d.ramo_id in todos_ramos
                    ]
                )
                for r in c.ramos
            ]
        )
        for c in carreras
    ]
def create_ramo(db: Session, ramo: RamoCreate, carreras_ids: list[int], semestre: int):
    db_ramo = db.query(Ramo).filter(
        Ramo.nombre == ramo.nombre, Ramo.semestre == semestre).first()

    if not db_ramo:
        db_ramo = Ramo(nombre=ramo.nombre, semestre=semestre)
        db.add(db_ramo)
        db.commit()
        db.refresh(db_ramo)

    for carrera_id in carreras_ids:
        carrera = db.query(Carrera).filter(Carrera.id == carrera_id).first()
        if carrera and db_ramo not in carrera.ramos:
            carrera.ramos.append(db_ramo)
            db.add(carrera)

    db.commit()
    db.refresh(db_ramo)
    return db_ramo


def get_ramos_por_carrera(db: Session, carrera_id: int):
    return db.query(Ramo).join(Carrera.ramos).filter(Carrera.id == carrera_id).all()


def create_prerequisito(db: Session, prereq: PrerequisitoCreate):
    ramo = db.query(Ramo).filter(Ramo.id == prereq.ramo_id).first()
    requisito = db.query(Ramo).filter(Ramo.id == prereq.requisito_id).first()
    
    if not ramo or not requisito:
        raise HTTPException(status_code=404, detail="Ramo o requisito no encontrado")

    nuevo_prereq = Prerequisito(ramo_id=prereq.ramo_id, requisito_id=prereq.requisito_id)
    db.add(nuevo_prereq)
    db.commit()
    db.refresh(nuevo_prereq)
    return {"ramo_id": ramo.id, "requisito_id": requisito.id}



def get_prerequisitos(db: Session, ramo_id: int):
    return db.query(
        Prerequisito.ramo_id,
        Prerequisito.requisito_id,
        Ramo.nombre.label("ramo_nombre"),
        RamoRequisito.nombre.label("requisito_nombre")
    ).select_from(Prerequisito)\
     .join(Ramo, Ramo.id == Prerequisito.ramo_id)\
     .join(RamoRequisito, RamoRequisito.id == Prerequisito.requisito_id)\
     .filter(Prerequisito.ramo_id == ramo_id)\
     .all()


def get_ramos_desbloqueados(db: Session, requisito_id: int):
    return db.query(
        Prerequisito.ramo_id,
        Prerequisito.requisito_id,
        Ramo.nombre.label("ramo_nombre"),
        RamoRequisito.nombre.label("requisito_nombre")
    ).select_from(Prerequisito)\
     .join(Ramo, Ramo.id == Prerequisito.ramo_id)\
     .join(RamoRequisito, RamoRequisito.id == Prerequisito.requisito_id)\
     .filter(Prerequisito.requisito_id == requisito_id)\
     .all()
