from fastapi import APIRouter, HTTPException, Query, Body
from typing import List, Optional

from schemas import Usuario, Mascota, Vuelo, Reserva
import op_usuarios as usuarios_ops
import op_mascotas as mascotas_ops
import op_vuelos as vuelos_ops
import op_reservas as reservas_ops

router = APIRouter()

# ----------------------------
# Endpoints de Usuarios
# ----------------------------

@router.get("/usuarios", response_model=List[Usuario])
def listar_usuarios():
    return usuarios_ops.listar_usuarios()

@router.get("/usuarios/{user_id}", response_model=Usuario)
def obtener_usuario(user_id: int):
    return usuarios_ops.obtener_usuario(user_id)

@router.post("/usuarios", response_model=Usuario)
def crear_usuario(usuario: Usuario):
    return usuarios_ops.crear_usuario(usuario)

@router.put("/usuarios/{user_id}", response_model=Usuario)
def actualizar_usuario(user_id: int, usuario: Usuario):
    return usuarios_ops.actualizar_usuario(user_id, usuario)

@router.delete("/usuarios/{user_id}")
def eliminar_usuario(user_id: int):
    return usuarios_ops.eliminar_usuario(user_id)

# ----------------------------
# Endpoints de Mascotas
# ----------------------------

@router.get("/mascotas", response_model=List[Mascota])
def listar_mascotas():
    return mascotas_ops.listar_mascotas()

@router.get("/mascotas/{mascota_id}", response_model=Mascota)
def obtener_mascota(mascota_id: int):
    return mascotas_ops.obtener_mascota(mascota_id)

@router.get("/usuarios/{user_id}/mascotas", response_model=List[Mascota])
def mascotas_por_usuario(user_id: int):
    return mascotas_ops.mascotas_por_usuario(user_id)

@router.post("/mascotas", response_model=Mascota)
def crear_mascota(mascota: Mascota):
    return mascotas_ops.crear_mascota(mascota)

@router.put("/mascotas/{mascota_id}", response_model=Mascota)
def actualizar_mascota(mascota_id: int, mascota: Mascota):
    return mascotas_ops.actualizar_mascota(mascota_id, mascota)

@router.delete("/mascotas/{mascota_id}")
def eliminar_mascota(mascota_id: int):
    return mascotas_ops.eliminar_mascota(mascota_id)

# ----------------------------
# Endpoints de Vuelos
# ----------------------------

@router.get("/vuelos", response_model=List[Vuelo])
def listar_vuelos(origen: Optional[str] = Query(None), destino: Optional[str] = Query(None), fecha: Optional[str] = Query(None)):
    return vuelos_ops.listar_vuelos(origen, destino, fecha)

@router.get("/vuelos/{localizador}", response_model=Vuelo)
def obtener_vuelo(localizador: str):
    return vuelos_ops.obtener_vuelo(localizador)

@router.post("/vuelos", response_model=Vuelo)
def crear_vuelo(vuelo: Vuelo):
    return vuelos_ops.crear_vuelo(vuelo)

@router.put("/vuelos/{localizador}", response_model=Vuelo)
def actualizar_vuelo(localizador: str, vuelo: Vuelo):
    return vuelos_ops.actualizar_vuelo(localizador, vuelo)

@router.delete("/vuelos/{localizador}")
def eliminar_vuelo(localizador: str):
    return vuelos_ops.eliminar_vuelo(localizador)

@router.get("/vuelos/{localizador}/mascotas/count")
def contar_mascotas_en_vuelo(localizador: str):
    return vuelos_ops.contar_mascotas_en_vuelo(localizador)

# ----------------------------
# Endpoints de Reservas
# ----------------------------

@router.get("/reservas", response_model=List[Reserva])
def listar_reservas():
    return reservas_ops.listar_reservas()

@router.get("/reservas/{reserva_id}", response_model=Reserva)
def obtener_reserva(reserva_id: int):
    return reservas_ops.obtener_reserva(reserva_id)

@router.post("/reservas", response_model=Reserva)
def crear_reserva(reserva: Reserva):
    return reservas_ops.crear_reserva(reserva)

@router.put("/reservas/{reserva_id}", response_model=Reserva)
def actualizar_reserva(reserva_id: int, reserva: Reserva):
    return reservas_ops.actualizar_reserva(reserva_id, reserva)

@router.post("/reservas/{reserva_id}/comprar")
def comprar_reserva(reserva_id: int):
    return reservas_ops.comprar_reserva(reserva_id)

@router.delete("/reservas/{reserva_id}")
def eliminar_reserva(reserva_id: int):
    return reservas_ops.eliminar_reserva(reserva_id)
