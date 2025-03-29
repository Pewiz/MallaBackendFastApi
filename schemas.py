from pydantic import BaseModel
from typing import List, Optional

class CarreraBase (BaseModel):
    nombre: str

class CarreraCreate (CarreraBase):
    pass

class CarreraResponse (CarreraBase):
    id: int
    class Config:
        orm_mode = True
    
class RamoBase (BaseModel):
    nombre: str
    semestre: int
    carrera_id: int 

class RamoCreate (RamoBase):
    pass 

class RamoResponse (RamoBase):
    id: int
    class Config:
        orm_mode = True

class PrerequisitoBase (BaseModel):
    ramo_id: int
    requisito_id: int

class PrerequisitoCreate(PrerequisitoBase):
    pass 
    