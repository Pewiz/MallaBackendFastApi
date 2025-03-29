from sqlalchemy.orm import Session
from models import Carrera, Ramo, Prerequisito
from schemas import CarreraCreate, RamoCreate, PrerequisitoCreate


def create_carrera(db: Session, carrera: CarreraCreate):
    nueva_carrera = Carrera(nombre=carrera.nombre)
    db.add(nueva_carrera)
    db.commit()
    db.refresh(nueva_carrera)
    return nueva_carrera


def get_carreras(db: Session):
    return db.query(Carrera).all()


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
    nuevo_prereq = Prerequisito(**prereq.dict())
    db.add(nuevo_prereq)
    db.commit()
    db.refresh(nuevo_prereq)
    return nuevo_prereq


def get_prerequisitos(db: Session, ramo_id: int):
    prerequisitos = db.query(Prerequisito).filter(Prerequisito.ramo_id == ramo_id).all()
    result = []
    for p in prerequisitos:
        ramo = db.query(Ramo).filter(Ramo.id == p.ramo_id).first()
        requisito = db.query(Ramo).filter(Ramo.id == p.requisito_id).first()
        result.append({
            "ramo_id": p.ramo_id,
            "ramo_nombre": ramo.nombre if ramo else "",
            "requisito_id": p.requisito_id,
            "requisito_nombre": requisito.nombre if requisito else ""
        })
    return result

def get_ramos_desbloqueados(db: Session, requisito_id: int):
    # Obtener todos los registros de desbloqueo
    desbloqueados = db.query(Prerequisito).filter(Prerequisito.requisito_id == requisito_id).all()
    
    if not desbloqueados:
        return []
    
    # Obtener todos los IDs de ramos involucrados
    ramo_ids = {d.ramo_id for d in desbloqueados}
    ramo_ids.add(requisito_id)  # Añadir el ramo requisito
    
    # Obtener todos los nombres de ramos en una sola consulta
    ramos = db.query(Ramo.id, Ramo.nombre).filter(Ramo.id.in_(ramo_ids)).all()
    ramos_dict = {r.id: r.nombre for r in ramos}
    
    # Construir la respuesta
    return [{
        "ramo_id": d.ramo_id,
        "ramo_nombre": ramos_dict.get(d.ramo_id, ""),
        "requisito_id": d.requisito_id,
        "requisito_nombre": ramos_dict.get(d.requisito_id, "")
    } for d in desbloqueados]
