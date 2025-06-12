import csv
from typing import List
from models.usuario import Usuario

USUARIOS_CSV = "usuarios.csv"


def listar_usuarios() -> List[Usuario]:
    usuarios = []
    try:
        with open(USUARIOS_CSV, newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                row['id'] = int(row['id'])
                usuarios.append(Usuario(**row))
    except FileNotFoundError:
        pass
    return usuarios


def obtener_usuario(user_id: int) -> Usuario:
    try:
        with open(USUARIOS_CSV, newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if int(row['id']) == user_id:
                    return Usuario(**row)
    except FileNotFoundError:
        raise Exception("Archivo de usuarios no encontrado")
    raise Exception("Usuario no encontrado")


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
    usuarios = []
    actualizado = False
    try:
        with open(USUARIOS_CSV, newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if int(row['id']) == user_id:
                    row.update(usuario.dict())
                    actualizado = True
                usuarios.append(Usuario(**row))
    except FileNotFoundError:
        raise Exception("Archivo de usuarios no encontrado")

    if not actualizado:
        raise Exception("Usuario no encontrado")

    with open(USUARIOS_CSV, "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=usuario.dict().keys())
        writer.writeheader()
        for u in usuarios:
            writer.writerow(u.dict())
    return usuario


def eliminar_usuario(user_id: int):
    usuarios = []
    eliminado = False
    try:
        with open(USUARIOS_CSV, newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if int(row['id']) != user_id:
                    usuarios.append(Usuario(**row))
                else:
                    eliminado = True
    except FileNotFoundError:
        raise Exception("Archivo de usuarios no encontrado")

    if not eliminado:
        raise Exception("Usuario no encontrado")

    with open(USUARIOS_CSV, "w", newline='', encoding="utf-8") as csvfile:
        if usuarios:
            writer = csv.DictWriter(csvfile, fieldnames=usuarios[0].dict().keys())
            writer.writeheader()
            for u in usuarios:
                writer.writerow(u.dict())
    return {"ok": True}
