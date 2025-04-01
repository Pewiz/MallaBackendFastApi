from pydantic import BaseModel
from typing import List, Optional
from fastapi import UploadFile


class CarreraBase (BaseModel):
    nombre: str
    nombre_malla:str
    link_admision: str
    url_image: Optional[UploadFile] = None

class CarreraCreate (CarreraBase):
    pass


class CarreraSimpleResponse(CarreraBase):
    id: int    
    nombre: str
    nombre_malla:str
    link_admision: str
    url_image: Optional[str]
    class Config:
        from_attributes = True
    

class CarreraCompletaResponse (CarreraBase):
    id: int    
    nombre: str
    nombre_malla:str
    link_admision: str
    url_image: Optional[str]
    ramos: List["RamoSimpleResponse"]
    class Config:
        from_attributes = True


class RamoBase (BaseModel):
    nombre: str
    semestre: int


class RamoCreate (RamoBase):
    pass


class RamoSimpleResponse (RamoBase):
    id: int
    prev: List[str] = []
    next: List[str] = []
    class Config:
        from_attributes = True

class RamoResponse (RamoBase):
    id: int
    carreras: Optional[List[CarreraBase]] = None
    prev: List[str] = []
    next: List[str] = []

    class Config:
        from_attributes = True


class PrerequisitoBase(BaseModel):
    ramo_id: int
    requisito_id: int


class PrerequisitoCreate(PrerequisitoBase):
    pass


class PrerequisitoResponse(BaseModel):
    ramo_id: int
    requisito_id: int
    ramo_nombre: str
    requisito_nombre: str

    class Config:
        from_attributes = True


class RamosDesbloqueadosResponse(BaseModel):
    ramo_id: int
    requisito_id: int
    ramo_nombre: str
    requisito_nombre: str

    class Config:
        from_attributes = True
