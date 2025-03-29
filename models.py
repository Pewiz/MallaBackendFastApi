from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

carrera_ramos = Table(
    "carreras_ramos",
    Base.metadata,
    Column("carrera_id", Integer, ForeignKey("carreras.id"), primary_key=True),
    Column("ramo_id", Integer, ForeignKey("ramos.id"), primary_key=True)
)

class Carrera (Base):
    __tablename__ = "carreras"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)

    #Relaciones
    ramos = relationship("Ramo", secondary=carrera_ramos ,back_populates="carreras")

class Ramo (Base): 
    __tablename__ = "ramos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    semestre = Column(Integer)
    

    carreras = relationship("Carrera", secondary=carrera_ramos ,back_populates="ramos")
    prerequisitos = relationship("Prerequisito", foreign_keys="[Prerequisito.ramo_id]", back_populates="ramo")
    desbloquea = relationship("Prerequisito", foreign_keys="[Prerequisito.requisito_id]", back_populates="requisito")



class Prerequisito (Base):
    __tablename__ = "prerequisitos"

    id = Column(Integer, primary_key=True, index=True)
    ramo_id = Column(Integer, ForeignKey("ramos.id"))
    requisito_id = Column(Integer, ForeignKey("ramos.id"))

    ramo = relationship("Ramo", foreign_keys=[ramo_id], back_populates="prerequisitos")
    requisito = relationship("Ramo", foreign_keys=[requisito_id], back_populates="desbloquea")

