import csv
from typing import List, Optional
from models.usuario import Usuario

USUARIOS_CSV = "usuarios.csv"

def listar_usuarios() -> List[Usuario]:
    usuarios = []
    try:
        with open(USUARIOS_CSV, newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    row['id'] = int(row['id'])
                    row['edadUsuario'] = int(row['edadUsuario'])
                    row['edadMascota'] = int(row['edadMascota'])
                    row['idMascota'] = int(row['idMascota'])
                    usuarios.append(Usuario(**row))
                except Exception:
                    continue  # Salta filas corruptas
    except FileNotFoundError:
        pass
    return usuarios

def obtener_usuario(user_id: int) -> Optional[Usuario]:
    for usuario in listar_usuarios():
        if usuario.id == user_id:
            return usuario
    return None

def crear_usuario(usuario: Usuario) -> Usuario:
    usuarios = listar_usuarios()
    if any(u.id == usuario.id for u in usuarios):
        raise Exception("El usuario ya existe")
    with open(USUARIOS_CSV, "a", newline='', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=usuario.dict().keys())
        if csvfile.tell() == 0:
            writer.writeheader()
        writer.writerow(usuario.dict())
    return usuario

def actualizar_usuario(user_id: int, usuario: Usuario) -> Usuario:
    usuarios = listar_usuarios()
    actualizado = False
    for i, u in enumerate(usuarios):
        if u.id == user_id:
            usuarios[i] = usuario
            actualizado = True
            break
    if not actualizado:
        raise Exception("Usuario no encontrado")
    with open(USUARIOS_CSV, "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=usuario.dict().keys())
        writer.writeheader()
        for u in usuarios:
            writer.writerow(u.dict())
    return usuario

def eliminar_usuario(user_id: int):
    usuarios = listar_usuarios()
    nuevos = [u for u in usuarios if u.id != user_id]
    if len(nuevos) == len(usuarios):
        raise Exception("Usuario no encontrado")
    with open(USUARIOS_CSV, "w", newline='', encoding="utf-8") as csvfile:
        if nuevos:
            writer = csv.DictWriter(csvfile, fieldnames=nuevos[0].dict().keys())
            writer.writeheader()
            for u in nuevos:
                writer.writerow(u.dict())
    return {"ok": True}