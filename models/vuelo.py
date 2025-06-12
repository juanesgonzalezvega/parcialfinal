from pydantic import BaseModel

class Vuelo(BaseModel):
    id: int
    origen: str
    destino: str
    fecha: str   # puedes cambiar a datetime.date si lo deseas, pero para CSV es más sencillo string
    sillasReservadas: int
    sillasVendidas: int