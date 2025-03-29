from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Carrera (Base):
    __tablenam__ = "carreras"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)

    #Relaciones
    ramos = relationship("Ramo", back_populates="carrera")

class Ramo (Base): 
    __tablename__ = "ramos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    semestre = Column(Integer)
    carrera_id = Column(Integer, ForeignKey("carrera.id"))

    carrera = relationship("Carrera", back_populates="ramos")
    prerequisitos = relationship("Prerequisito", foreign_keys="[Prerequisito.ramo_id]", back_populates="ramo")
    desbloquea = relationship("Prerequisito", foreign_keys="[Prerequisito.requisito_id]", back_populates="requisito")

class Prerequisito (Base):
    __tablename__ = "prerequisitos"

    id = Column(Integer, primary_key=True, index=True)
    ramo_id = Column(Integer, ForeignKey("ramos.id"))
    requisito_id = Column(Integer, ForeignKey("ramos.id"))

    ramo = relationship("Ramo", foreign_keys=[ramo_id], back_populates="prerequisitos")
    requisito = relationship("Ramo", foreign_keys=[requisito_id], back_populates="desbloquea")