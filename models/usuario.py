from pydantic import BaseModel

class Usuario(BaseModel):
    id: int
    nombre: str
    edadUsuario: int
    CC: str
    nombreMascota: str
    edadMascota: int
    idMascota: int