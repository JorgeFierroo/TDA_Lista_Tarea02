from sqlalchemy import Column, String, Enum, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
import enum
from datetime import datetime

Base = declarative_base()

class EstadoVueloEnum(str, enum.Enum):
    programado = "programado"
    emergencia = "emergencia"
    pendiente = "pendiente"

class Vuelo(Base):
    __tablename__ = "vuelos"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, unique=True, nullable=False)
    estado = Column(Enum(EstadoVueloEnum), default=EstadoVueloEnum.programado)
    hora = Column(DateTime, nullable=False, default=datetime.utcnow)
    origen = Column(String, nullable=False)
    destino = Column(String, nullable=False)
