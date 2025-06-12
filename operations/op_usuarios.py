from fastapi import HTTPException
from typing import List
from schemas import Usuario
from database import USUARIOS

def listar_usuarios() -> List[Usuario]:
    return USUARIOS

def obtener_usuario(user_id: int) -> Usuario:
    for user in USUARIOS:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

def crear_usuario(usuario: Usuario) -> Usuario:
    USUARIOS.append(usuario)
    return usuario

def actualizar_usuario(user_id: int, usuario: Usuario) -> Usuario:
    for i, user in enumerate(USUARIOS):
        if user.id == user_id:
            USUARIOS[i] = usuario
            return usuario
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

def eliminar_usuario(user_id: int) -> dict:
    for i, user in enumerate(USUARIOS):
        if user.id == user_id:
            del USUARIOS[i]
            return {"ok": True}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")
