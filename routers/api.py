from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional

from models.usuario import Usuario
from models.vuelo import Vuelo
from operations import op_usuarios as usuarios_ops
from operations import op_vuelos as vuelos_ops

router = APIRouter()

# ----------------------------
# Endpoints de Usuarios
# ----------------------------

@router.get("/usuarios", response_model=List[Usuario])
def listar_usuarios():
    return usuarios_ops.listar_usuarios()

@router.get("/usuarios/{user_id}", response_model=Usuario)
def obtener_usuario(user_id: int):
    usuario = usuarios_ops.obtener_usuario(user_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.post("/usuarios", response_model=Usuario)
def crear_usuario(usuario: Usuario):
    try:
        return usuarios_ops.crear_usuario(usuario)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/usuarios/{user_id}", response_model=Usuario)
def actualizar_usuario(user_id: int, usuario: Usuario):
    try:
        return usuarios_ops.actualizar_usuario(user_id, usuario)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/usuarios/{user_id}")
def eliminar_usuario(user_id: int):
    try:
        return usuarios_ops.eliminar_usuario(user_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

# ----------------------------
# Endpoints de Vuelos
# ----------------------------

@router.get("/vuelos", response_model=List[Vuelo])
def listar_vuelos(origen: Optional[str] = Query(None), destino: Optional[str] = Query(None), fecha: Optional[str] = Query(None)):
    return vuelos_ops.listar_vuelos(origen, destino, fecha)

@router.get("/vuelos/{vuelo_id}", response_model=Vuelo)
def obtener_vuelo(vuelo_id: int):
    vuelo = vuelos_ops.obtener_vuelo(vuelo_id)
    if not vuelo:
        raise HTTPException(status_code=404, detail="Vuelo no encontrado")
    return vuelo

@router.post("/vuelos", response_model=Vuelo)
def crear_vuelo(vuelo: Vuelo):
    try:
        return vuelos_ops.crear_vuelo(vuelo)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/vuelos/{vuelo_id}", response_model=Vuelo)
def actualizar_vuelo(vuelo_id: int, vuelo: Vuelo):
    try:
        return vuelos_ops.actualizar_vuelo(vuelo_id, vuelo)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/vuelos/{vuelo_id}")
def eliminar_vuelo(vuelo_id: int):
    try:
        return vuelos_ops.eliminar_vuelo(vuelo_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))