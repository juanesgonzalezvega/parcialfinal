from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class Usuario(BaseModel):
    id: int
    nombre: str
    correo: str

class Mascota(BaseModel):
    id: int
    nombre: str
    especie: str
    usuario_id: int

class Vuelo(BaseModel):
    localizador: str
    origen: str
    destino: str
    fecha: date

class Reserva(BaseModel):
    id: int
    usuario_id: int
    vuelo_localizador: str
    mascotas: List[int]
    comprada: Optional[bool] = False