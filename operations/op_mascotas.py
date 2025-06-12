from fastapi import HTTPException
from typing import List
from schemas import Mascota
from database import MASCOTAS

def listar_mascotas() -> List[Mascota]:
    return MASCOTAS

def obtener_mascota(mascota_id: int) -> Mascota:
    for mascota in MASCOTAS:
        if mascota.id == mascota_id:
            return mascota
    raise HTTPException(status_code=404, detail="Mascota no encontrada")

def mascotas_por_usuario(user_id: int) -> List[Mascota]:
    return [mascota for mascota in MASCOTAS if mascota.usuario_id == user_id]

def crear_mascota(mascota: Mascota) -> Mascota:
    MASCOTAS.append(mascota)
    return mascota

def actualizar_mascota(mascota_id: int, mascota: Mascota) -> Mascota:
    for i, m in enumerate(MASCOTAS):
        if m.id == mascota_id:
            MASCOTAS[i] = mascota
            return mascota
    raise HTTPException(status_code=404, detail="Mascota no encontrada")

def eliminar_mascota(mascota_id: int) -> dict:
    for i, mascota in enumerate(MASCOTAS):
        if mascota.id == mascota_id:
            del MASCOTAS[i]
            return {"ok": True}
    raise HTTPException(status_code=404, detail="Mascota no encontrada")