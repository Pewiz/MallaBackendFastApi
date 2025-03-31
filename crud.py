from fastapi import HTTPException
from sqlalchemy.orm import Session, aliased, joinedload
from models import Carrera, Ramo, Prerequisito
from schemas import CarreraCreate, RamoCreate, PrerequisitoCreate, CarreraResponse, RamoResponse
from sqlalchemy import func
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
    todos_ramos = {r.id: r.nombre for r in db.query(
        Ramo.id, Ramo.nombre).all()}

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

    # Diccionario con información de todos los ramos: id -> {nombre, semestre}
    todos_ramos = {
        r.id: {"nombre": r.nombre, "semestre": r.semestre}
        for r in db.query(Ramo.id, Ramo.nombre, Ramo.semestre).all()
    }

    # Calcular el máximo semestre de prerequisitos por ramo usando SQL
    max_prereq_sem = db.query(
        Prerequisito.ramo_id,
        func.max(Ramo.semestre).label('max_sem')
    ).join(Ramo, Prerequisito.requisito_id == Ramo.id).group_by(Prerequisito.ramo_id).all()

    max_pre_semester = {ramo_id: max_sem for ramo_id,
                        max_sem in max_prereq_sem}

    resultado = []
    for c in carreras:
        carrera_resp = {
            "id": c.id,
            "nombre": c.nombre,
            "ramos": []
        }
        for r in c.ramos:
            # 'prev' incluye todos los prerequisitos (nombres)
            prev_list = [todos_ramos[p.requisito_id]["nombre"]
                         for p in r.prerequisitos]

            # 'next' filtra cursos desbloqueados según condiciones
            next_list = []
            for d in r.desbloquea:
                unlocked_id = d.ramo_id
                unlocked_info = todos_ramos[unlocked_id]
                unlocked_name = unlocked_info["nombre"]

                if unlocked_name in ["Práctica Profesional", "Anteproyecto de Título"]:
                    continue

                # Verificar si el semestre máximo de prerequisitos coincide con el semestre actual
                if unlocked_id in max_pre_semester:
                    if max_pre_semester[unlocked_id] == r.semestre:
                        next_list.append(unlocked_name)
                else:
                    # Si no tiene prerequisitos, se incluye (caso válido si es consistente)
                    next_list.append(unlocked_name)

            ramo_resp = {
                "id": r.id,
                "nombre": r.nombre,
                "semestre": r.semestre,
                "carreras": None,
                "prev": prev_list,
                "next": next_list
            }
            carrera_resp["ramos"].append(ramo_resp)
        resultado.append(carrera_resp)

    return resultado


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
