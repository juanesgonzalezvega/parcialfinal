from pydantic import BaseModel

class Reserva(BaseModel):
    id: int
    vuelo_id: int  # ID del vuelo al que pertenece la reserva
    usuario_id: int  # ID del usuario que realiza la reserva
    nombre_mascota: str  # Nombre de la mascota asociada a la reserva
    fecha_reserva: str  # Fecha en que se realiza la reserva
    estado: str  # Estado de la reserva (ej. "confirmada", "cancelada")
