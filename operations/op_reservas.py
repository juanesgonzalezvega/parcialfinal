from fastapi import HTTPException
from typing import List
from schemas import Reserva
from database import RESERVAS

def listar_reservas() -> List[Reserva]:
    return RESERVAS

def obtener_reserva(reserva_id: int) -> Reserva:
    for reserva in RESERVAS:
        if reserva.id == reserva_id:
            return reserva
    raise HTTPException(status_code=404, detail="Reserva no encontrada")

def crear_reserva(reserva: Reserva) -> Reserva:
    RESERVAS.append(reserva)
    return reserva

def actualizar_reserva(reserva_id: int, reserva: Reserva) -> Reserva:
    for i, r in enumerate(RESERVAS):
        if r.id == reserva_id:
            RESERVAS[i] = reserva
            return reserva
    raise HTTPException(status_code=404, detail="Reserva no encontrada")

def eliminar_reserva(reserva_id: int) -> dict:
    for i, reserva in enumerate(RESERVAS):
        if reserva.id == reserva_id:
            del RESERVAS[i]
            return {"ok": True}
    raise HTTPException(status_code=404, detail="Reserva no encontrada")

def comprar_reserva(reserva_id: int) -> dict:
    for reserva in RESERVAS:
        if reserva.id == reserva_id:
            if getattr(reserva, "comprada", False):
                raise HTTPException(status_code=400, detail="La reserva ya está comprada")
            reserva.comprada = True
            return {"ok": True, "detalle": "Reserva comprada exitosamente"}
    raise HTTPException(status_code=404, detail="Reserva no encontrada")