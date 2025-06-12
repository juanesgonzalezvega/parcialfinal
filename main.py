import csv
import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import List

from models.usuario import Usuario
from models.vuelo import Vuelo
from models.reserva import Reserva
from routers import api  # Importa el router que contiene los endpoints

USUARIOS_CSV = "usuarios.csv"
VUELOS_CSV = "vuelos.csv"
RESERVAS_CSV = "reservas.csv"

app = FastAPI(title="ParcialFinal - Vuelos para Mascotas")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ---------- CARGA Y GUARDADO CSV ----------

def cargar_usuarios() -> List[Usuario]:
    usuarios = []
    if not os.path.exists(USUARIOS_CSV):
        with open(USUARIOS_CSV, "w", newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=Usuario.__annotations__.keys())
            writer.writeheader()
    with open(USUARIOS_CSV, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            row['id'] = int(row['id'])
            row['edadUsuario'] = int(row['edadUsuario'])
            row['edadMascota'] = int(row['edadMascota'])
            row['idMascota'] = int(row['idMascota'])
            usuarios.append(Usuario(**row))
    return usuarios

def guardar_usuarios(usuarios: List[Usuario]):
    with open(USUARIOS_CSV, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=Usuario.__annotations__.keys())
        writer.writeheader()
        for usuario in usuarios:
            writer.writerow({k: str(v) for k, v in usuario.dict().items()})

def cargar_vuelos() -> List[Vuelo]:
    vuelos = []
    if not os.path.exists(VUELOS_CSV):
        with open(VUELOS_CSV, "w", newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=Vuelo.__annotations__.keys())
            writer.writeheader()
    with open(VUELOS_CSV, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            row['id'] = int(row['id'])
            row['sillasReservadas'] = int(row['sillasReservadas'])
            row['sillasVendidas'] = int(row['sillasVendidas'])
            vuelos.append(Vuelo(**row))
    return vuelos

def guardar_vuelos(vuelos: List[Vuelo]):
    with open(VUELOS_CSV, "w", newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=Vuelo.__annotations__.keys())
        writer.writeheader()
        for vuelo in vuelos:
            writer.writerow({k: str(v) for k, v in vuelo.dict().items()})

def cargar_reservas() -> List[Reserva]:
    reservas = []
    if not os.path.exists(RESERVAS_CSV):
        with open(RESERVAS_CSV, "w", newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=Reserva.__annotations__.keys())
            writer.writeheader()
    with open(RESERVAS_CSV, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            row['id'] = int(row['id'])
            row['vuelo_id'] = int(row['vuelo_id'])
            row['usuario_id'] = int(row['usuario_id'])
            reservas.append(Reserva(**row))
    return reservas

def guardar_reservas(reservas: List[Reserva]):
    with open(RESERVAS_CSV, "w", newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=Reserva.__annotations__.keys())
        writer.writeheader()
        for reserva in reservas:
            writer.writerow({k: str(v) for k, v in reserva.dict().items()})

# ---------- CARGA INICIAL ----------

USUARIOS = cargar_usuarios()
VUELOS = cargar_vuelos()
RESERVAS = cargar_reservas()

# ---------- RUTAS ----------

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

# Incluir el router de la API
app.include_router(api.router)

# ---------- Manejadores de Errores ----------

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse("404.html", {"request": request, "detail": exc.detail}, status_code=exc.status_code)