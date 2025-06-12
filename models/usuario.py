from pydantic import BaseModel

class Usuario(BaseModel):
    id: int
    nombre: str
    edadUsuario: int
    idMascota: int
    nombreMascota: str
    edadMascota: int
