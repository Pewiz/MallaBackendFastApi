from pydantic import BaseModel
from typing import List, Optional

class CarreraBase (BaseModel):
    nombre: str

class CarreraCreate (CarreraBase):
    pass

class CarreraResponse (CarreraBase):
    id: int
    ramos: List["RamoResponse"]
    class Config:
        from_attributes = True
    
class RamoBase (BaseModel):
    nombre: str
    semestre: int

class RamoCreate (RamoBase):
    pass 

class RamoResponse (RamoBase):
    id: int
    carreras: Optional[List[CarreraBase]] = None
    prev: List[str] = []
    next: List[str] = []
    class Config:
        from_attributes = True

class PrerequisitoBase (BaseModel):
    ramo_nombre: str
    requisito_nombre: str

class PrerequisitoCreate(PrerequisitoBase):
    pass 
    
class PrerequisitoResponse(BaseModel):
    class Config:
        from_attributes = True