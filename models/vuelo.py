from pydantic import BaseModel

class Vuelo(BaseModel):
    id: int
    origen: str
    destino: str
    fecha: str
    sillasReservadas: int
    sillasVendidas: int
