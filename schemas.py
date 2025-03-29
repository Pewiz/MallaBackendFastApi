from pydantic import BaseModel
from typing import List, Optional

class CarreraBase (BaseModel):
    nombre: str

class CarreraCreate (CarreraBase):
    pass

class CarreraResponse (CarreraBase):
    id: int
    ramos: List[str]
    class Config:
        from_attributes = True
    
class RamoBase (BaseModel):
    nombre: str
    semestre: int

class RamoCreate (RamoBase):
    pass 

class RamoResponse (RamoBase):
    id: int
    carreras: List[CarreraBase]
    class Config:
        from_attributes = True

class PrerequisitoBase (BaseModel):
    ramo_id: int
    requisito_id: int

class PrerequisitoCreate(PrerequisitoBase):
    pass 
    
class PrerequisitoResponse(BaseModel):
    ramo_id: int
    ramo_nombre: str
    requisito_id: int
    requisito_nombre: str

    class Config:
        from_attributes = True