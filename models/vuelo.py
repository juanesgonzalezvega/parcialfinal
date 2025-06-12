from pydantic import BaseModel
from datetime import date


class Vuelo(BaseModel):

localizador: str
origen: str
destino: str
fecha: date
sillas_res: int
sillas_ven: int