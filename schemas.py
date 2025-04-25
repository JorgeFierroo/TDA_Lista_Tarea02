from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class EstadoVueloEnum(str, Enum):
    programado = "programado"
    emergencia = "emergencia"
    pendiente = "pendiente"

class VueloCreate(BaseModel):
    codigo: str
    estado: EstadoVueloEnum
    hora: datetime
    origen: str
    destino: str

class VueloOut(VueloCreate):
    id: int

    class Config:
        orm_mode = True
