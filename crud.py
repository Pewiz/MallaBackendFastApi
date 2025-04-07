from fastapi import HTTPException
from sqlalchemy.orm import Session, aliased, joinedload
from models import Carrera, Ramo, Prerequisito
from schemas import CarreraCreate, RamoCreate, PrerequisitoCreate, RamoResponse
from sqlalchemy import func
RamoRequisito = aliased(Ramo)


def create_carrera(db: Session, carrera: CarreraCreate):
    nueva_carrera = Carrera(nombre=carrera.nombre)
    db.add(nueva_carrera)
    db.commit()
    db.refresh(nueva_carrera)
    return nueva_carrera


def get_carrera_con_ramos(db: Session, carrera_id: int):
    # Consulta principal con todas las relaciones necesarias
    carrera = db.query(Carrera).options(
        joinedload(Carrera.ramos).subqueryload(Ramo.prerequisitos),
        joinedload(Carrera.ramos).subqueryload(Ramo.desbloquea)
    ).filter(Carrera.id == carrera_id).first()

    if not carrera:
        return None

    # Diccionario con información de todos los ramos: id -> nombre
    todos_ramos = {
        r.id: r.nombre
        for r in db.query(Ramo.id, Ramo.nombre).all()
    }

    ramos_procesados = []
    for ramo in carrera.ramos:
        # Lista de prerequisitos (nombres)
        prev_list = [todos_ramos.get(p.requisito_id) for p in ramo.prerequisitos]

        # Lista de ramos que desbloquea (nombres)
        next_list = []
        for d in ramo.desbloquea:
            unlocked_id = d.ramo_id
            unlocked_name = todos_ramos.get(unlocked_id)

            if not unlocked_name:
                continue

            # Puedes excluir ramos específicos si quieres seguir filtrando algunos:
            if unlocked_name in [
                "Práctica Profesional",
                "Anteproyecto de Título",
                "Taller Integrado I",
                "Taller Integrado II",
                "Internado Gestión del Cuidado I",
                "Internado Gestión del Cuidado II"
            ]:
                continue

            next_list.append(unlocked_name)

        ramo_data = {
            "id": ramo.id,
            "nombre": ramo.nombre,
            "semestre": ramo.semestre,
            "prev": prev_list,
            "next": next_list,
            "carreras": None
        }
        ramos_procesados.append(ramo_data)

    return {
        "id": carrera.id,
        "slug": carrera.slug,
        "nombre": carrera.nombre,
        "nombre_malla": carrera.nombre_malla,
        "url_image": carrera.url_image,
        "link_admision": carrera.link_admision,
        "ramos": ramos_procesados
    }


def get_carreras(db: Session):
    carreras = db.query(Carrera.id, Carrera.slug ,Carrera.nombre, Carrera.nombre_malla, Carrera.link_admision ,Carrera.url_image).all()
    
    return [{"id": c.id, "slug": c.slug ,"nombre": c.nombre, "nombre_malla": c.nombre_malla, "link_admision": c.link_admision ,"url_image": c.url_image} for c in carreras]


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
        raise HTTPException(
            status_code=404, detail="Ramo o requisito no encontrado")

    nuevo_prereq = Prerequisito(
        ramo_id=prereq.ramo_id, requisito_id=prereq.requisito_id)
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
