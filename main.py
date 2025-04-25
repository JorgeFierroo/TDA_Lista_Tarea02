from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Vuelo
from schemas import VueloCreate, VueloOut
from dll import _ListaVuelos
from dll import *

app = FastAPI()

app.title = 'Vuelos con listas enlazadas'

dll = _ListaVuelos()

@app.post("/vuelos/")
def crear_vuelo(vuelo: VueloCreate, db: Session = Depends(get_db)):
    vuelo_existente = db.query(Vuelo).filter(Vuelo.codigo == vuelo.codigo).first()
    if vuelo_existente:
        raise HTTPException(status_code=400, detail="Código de vuelo ya registrado")

    nuevo_vuelo = Vuelo(**vuelo.dict())
    db.add(nuevo_vuelo)
    db.commit()
    db.refresh(nuevo_vuelo)
    return nuevo_vuelo