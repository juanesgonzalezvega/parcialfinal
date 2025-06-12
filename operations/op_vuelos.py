from fastapi import HTTPException
from typing import List
from schemas import Vuelo
from database import VUELOS, RESERVAS

def listar_vuelos(origen: str = None, destino: str = None, fecha: str = None) -> List[Vuelo]:
    vuelos_filtrados = VUELOS
    if origen:
        vuelos_filtrados = [v for v in vuelos_filtrados if v.origen == origen]
    if destino:
        vuelos_filtrados = [v for v in vuelos_filtrados if v.destino == destino]
    if fecha:
        vuelos_filtrados = [v for v in vuelos_filtrados if str(v.fecha) == fecha]
    return vuelos_filtrados

def obtener_vuelo(localizador: str) -> Vuelo:
    for vuelo in VUELOS:
        if vuelo.localizador == localizador:
            return vuelo
    raise HTTPException(status_code=404, detail="Vuelo no encontrado")

def crear_vuelo(vuelo: Vuelo) -> Vuelo:
    VUELOS.append(vuelo)
    return vuelo

def actualizar_vuelo(localizador: str, vuelo: Vuelo) -> Vuelo:
    for i, v in enumerate(VUELOS):
        if v.localizador == localizador:
            VUELOS[i] = vuelo
            return vuelo
    raise HTTPException(status_code=404, detail="Vuelo no encontrado")

def eliminar_vuelo(localizador: str) -> dict:
    for i, vuelo in enumerate(VUELOS):
        if vuelo.localizador == localizador:
            del VUELOS[i]
            return {"ok": True}
    raise HTTPException(status_code=404, detail="Vuelo no encontrado")

def contar_mascotas_en_vuelo(localizador: str) -> dict:
    total = 0
    for reserva in RESERVAS:
        if reserva.vuelo_localizador == localizador:
            total += len(reserva.mascotas)
    return {"mascotas_en_vuelo": total}
