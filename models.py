from sqlalchemy import Column, Integer, String, Enum, DateTime
from app.database import Base
from app.enums import EstadoVuelo
from datetime import datetime

class Vuelo(Base):
    __tablename__ = "vuelos"
    
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, unique=True, index=True)
    estado = Column(Enum(EstadoVuelo))
    hora = Column(DateTime, default=datetime.utcnow)
    origen = Column(String)
    destino = Column(String)