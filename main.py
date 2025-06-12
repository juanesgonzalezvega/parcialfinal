import csv
import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import List

from models.usuario import Usuario
from models.vuelo import Vuelo
from routers import api

USUARIOS_CSV = "usuarios.csv"
VUELOS_CSV = "vuelos.csv"

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
            try:
                row['id'] = int(row['id'])
                row['sillasReservadas'] = int(row['sillasReservadas'])
                row['sillasVendidas'] = int(row['sillasVendidas'])
                vuelos.append(Vuelo(**row))
            except ValueError as e:
                print(f"Error al convertir datos en la fila: {row}. Error: {e}")
    return vuelos

def guardar_vuelos(vuelos: List[Vuelo]):
    with open(VUELOS_CSV, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=Vuelo.__annotations__.keys())
        writer.writeheader()
        for vuelo in vuelos:
            writer.writerow({k: str(v) for k, v in vuelo.dict().items()})

# ---------- CARGA INICIAL ----------

USUARIOS = cargar_usuarios()
VUELOS = cargar_vuelos()

# ---------- RUTAS ----------

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Incluir el router de la API
app.include_router(api.router)

# ---------- Manejadores de Errores ----------

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse("404.html", {"request": request, "detail": exc.detail}, status_code=exc.status_code)

# ---------- Lifespan Event ----------

@app.on_event("lifespan")
async def lifespan(event):
    # Cargar datos al inicio
    yield
    # Guardar datos al final
    guardar_usuarios(USUARIOS)
    guardar_vuelos(VUELOS)
