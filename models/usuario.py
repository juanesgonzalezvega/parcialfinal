from pydantic import BaseModel
from typing import Optional
from datetime import date


class Usuario(BaseModel):

id: int
nombre: str
cc: int
edad: int
descripcion: Optional[str] = None
imagen: Optional[str] = None
# Información de la mascota principal del usuario
nombre_mascota: str
edad_mascota: int
especie_mascota: Optional[str] = None
peso_mascota: Optional[float] = None