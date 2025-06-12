import csv
import os
from fastapi import FastAPI, HTTPException
from typing import List, Optional
from pydantic import BaseModel

# ------------------- MODELOS -------------------

class Usuario(BaseModel):
    id: int
    nombre: str
    edadUsuario: int
    CC: str
    nombreMascota: str
    edadMascota: int
    idMascota: int

class Vuelo(BaseModel):
    id: int
    origen: str
    destino: str
    fecha: str
    sillasReservadas: int
    sillasVendidas: int

USUARIOS_CSV = "usuarios.csv"
VUELOS_CSV = "vuelos.csv"

# ------------------- UTILIDADES CSV -------------------

def leer_usuarios() -> List[Usuario]:
    usuarios = []
    if not os.path.exists(USUARIOS_CSV):
        with open(USUARIOS_CSV, "w", newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=Usuario.__fields__.keys())
            writer.writeheader()
    with open(USUARIOS_CSV, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                row['id'] = int(row['id'])
                row['edadUsuario'] = int(row['edadUsuario'])
                row['edadMascota'] = int(row['edadMascota'])
                row['idMascota'] = int(row['idMascota'])
                usuarios.append(Usuario(**row))
            except Exception:
                continue
    return usuarios

def guardar_usuarios(usuarios: List[Usuario]):
    with open(USUARIOS_CSV, "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=Usuario.__fields__.keys())
        writer.writeheader()
        for usuario in usuarios:
            writer.writerow(usuario.dict())

def leer_vuelos() -> List[Vuelo]:
    vuelos = []
    if not os.path.exists(VUELOS_CSV):
        with open(VUELOS_CSV, "w", newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=Vuelo.__fields__.keys())
            writer.writeheader()
    with open(VUELOS_CSV, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                row['id'] = int(row['id'])
                row['sillasReservadas'] = int(row['sillasReservadas'])
                row['sillasVendidas'] = int(row['sillasVendidas'])
                vuelos.append(Vuelo(**row))
            except Exception:
                continue
    return vuelos

def guardar_vuelos(vuelos: List[Vuelo]):
    with open(VUELOS_CSV, "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=Vuelo.__fields__.keys())
        writer.writeheader()
        for vuelo in vuelos:
            writer.writerow(vuelo.dict())

# ------------------- FASTAPI APP -------------------

app = FastAPI(title="ParcialFinal - Vuelos para Mascotas")

## --- USUARIOS ---

@app.get("/usuarios", response_model=List[Usuario])
def get_usuarios():
    return leer_usuarios()

@app.get("/usuarios/{user_id}", response_model=Usuario)
def get_usuario(user_id: int):
    for usuario in leer_usuarios():
        if usuario.id == user_id:
            return usuario
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.post("/usuarios", response_model=Usuario)
def post_usuario(usuario: Usuario):
    usuarios = leer_usuarios()
    if any(u.id == usuario.id for u in usuarios):
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    usuarios.append(usuario)
    guardar_usuarios(usuarios)
    return usuario

@app.put("/usuarios/{user_id}", response_model=Usuario)
def put_usuario(user_id: int, usuario: Usuario):
    usuarios = leer_usuarios()
    for i, u in enumerate(usuarios):
        if u.id == user_id:
            usuarios[i] = usuario
            guardar_usuarios(usuarios)
            return usuario
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.delete("/usuarios/{user_id}")
def delete_usuario(user_id: int):
    usuarios = leer_usuarios()
    nuevos = [u for u in usuarios if u.id != user_id]
    if len(nuevos) == len(usuarios):
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    guardar_usuarios(nuevos)
    return {"ok": True}

## --- VUELOS ---

@app.get("/vuelos", response_model=List[Vuelo])
def get_vuelos(origen: Optional[str] = None, destino: Optional[str] = None, fecha: Optional[str] = None):
    vuelos = leer_vuelos()
    if origen:
        vuelos = [v for v in vuelos if v.origen == origen]
    if destino:
        vuelos = [v for v in vuelos if v.destino == destino]
    if fecha:
        vuelos = [v for v in vuelos if v.fecha == fecha]
    return vuelos

@app.get("/vuelos/{vuelo_id}", response_model=Vuelo)
def get_vuelo(vuelo_id: int):
    for vuelo in leer_vuelos():
        if vuelo.id == vuelo_id:
            return vuelo
    raise HTTPException(status_code=404, detail="Vuelo no encontrado")

@app.post("/vuelos", response_model=Vuelo)
def post_vuelo(vuelo: Vuelo):
    vuelos = leer_vuelos()
    if any(v.id == vuelo.id for v in vuelos):
        raise HTTPException(status_code=400, detail="El vuelo ya existe")
    vuelos.append(vuelo)
    guardar_vuelos(vuelos)
    return vuelo

@app.put("/vuelos/{vuelo_id}", response_model=Vuelo)
def put_vuelo(vuelo_id: int, vuelo: Vuelo):
    vuelos = leer_vuelos()
    for i, v in enumerate(vuelos):
        if v.id == vuelo_id:
            vuelos[i] = vuelo
            guardar_vuelos(vuelos)
            return vuelo
    raise HTTPException(status_code=404, detail="Vuelo no encontrado")

@app.delete("/vuelos/{vuelo_id}")
def delete_vuelo(vuelo_id: int):
    vuelos = leer_vuelos()
    nuevos = [v for v in vuelos if v.id != vuelo_id]
    if len(nuevos) == len(vuelos):
        raise HTTPException(status_code=404, detail="Vuelo no encontrado")
    guardar_vuelos(nuevos)
    return {"ok": True}