import csv
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import List, Optional
from models.usuario import Usuario  # Importar el modelo Usuario
from models.vuelo import Vuelo  # Importar el modelo Vuelo

USUARIOS_CSV = "usuarios.csv"
VUELOS_CSV = "vuelos.csv"

app = FastAPI(title="ParcialFinal - Vuelos para Mascotas")

# Configura carpetas para archivos estáticos y plantillas
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Cargar datos desde archivos CSV
def cargar_usuarios():
    usuarios = []
    with open(USUARIOS_CSV, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            usuarios.append(Usuario(**row))  # Asegúrate de que los campos coincidan con el modelo Usuario
    return usuarios

def cargar_vuelos():
    vuelos = []
    with open(VUELOS_CSV, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            vuelos.append(Vuelo(**row))  # Asegúrate de que los campos coincidan con el modelo Vuelo
    return vuelos

# Guardar datos en archivos CSV
def guardar_usuarios():
    with open(USUARIOS_CSV, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=Usuario.__annotations__.keys())
        writer.writeheader()
        for usuario in USUARIOS:
            writer.writerow(usuario.dict())

def guardar_vuelos():
    with open(VUELOS_CSV, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=Vuelo.__annotations__.keys())
        writer.writeheader()
        for vuelo in VUELOS:
            writer.writerow(vuelo.dict())

# Cargar datos al iniciar la aplicación
USUARIOS = cargar_usuarios()
VUELOS = cargar_vuelos()

# Portada opcional (index.html)
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ------------------- USUARIOS -------------------

@app.get("/usuarios", response_model=List[Usuario])
def listar_usuarios():
    return USUARIOS

@app.get("/usuarios/{user_id}", response_model=Usuario)
def obtener_usuario(user_id: int):
    for user in USUARIOS:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.post("/usuarios", response_model=Usuario)
def crear_usuario(usuario: Usuario):
    USUARIOS.append(usuario)
    guardar_usuarios()  # Guardar cambios en el archivo CSV
    return usuario

@app.put("/usuarios/{user_id}", response_model=Usuario)
def actualizar_usuario(user_id: int, usuario: Usuario):
    for i, user in enumerate(USUARIOS):
        if user.id == user_id:
            USUARIOS[i] = usuario
            guardar_usuarios()  # Guardar cambios en el archivo CSV
            return usuario
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.delete("/usuarios/{user_id}")
def eliminar_usuario(user_id: int):
    for i, user in enumerate(USUARIOS):
        if user.id == user_id:
            del USUARIOS[i]
            guardar_usuarios()  # Guardar cambios en el archivo CSV
            return {"ok": True}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

# ------------------- MASCOTAS -------------------

# Aquí puedes agregar la lógica para manejar las mascotas si es necesario.
# Asegúrate de que el modelo de Mascota esté definido y que se maneje correctamente.

# ------------------- VUELOS -------------------

@app.get("/vuelos", response_model=List[Vuelo])
def listar_vuelos(origen: Optional[str] = None, destino: Optional[str] = None, fecha: Optional[str] = None):
    vuelos_filtrados = VUELOS
    if origen:
        vuelos_filtrados = [v for v in vuelos_filtrados if v.origen == origen]
    if destino:
        vuelos_filtrados = [v for v in vuelos_filtrados if v.destino == destino]
    if fecha:
        vuelos_filtrados = [v for v in vuelos_filtrados if str(v.fecha) == fecha]
    return vuelos_filtrados

@app.get("/vuelos/{localizador}", response_model=Vuelo)
def obtener_vuelo(localizador: str):
    for vuelo in VUELOS:
        if vuelo.id == localizador:  # Cambié localizador a id para que coincida con el modelo
            return vuelo
    raise HTTPException(status_code=404, detail="Vuelo no encontrado")

@app.post("/vuelos", response_model=Vuelo)
def crear_vuelo(vuelo: Vuelo):
    VUELOS.append(vuelo)
    guardar_vuelos()  # Guardar cambios en el archivo CSV
    return vuelo

@app.put("/vuelos/{localizador}", response_model=Vuelo)
def actualizar_vuelo(localizador: str, vuelo: Vuelo):
    for i, v in enumerate(VUELOS):
        if v.id == localizador:  # Cambié localizador a id para que coincida con el modelo
            VUELOS[i] = vuelo
            guardar_vuelos()  # Guardar cambios en el archivo CSV
            return vuelo
    raise HTTPException(status_code=404, detail="Vuelo no encontrado")

@app.delete("/vuelos/{localizador}")
def eliminar_vuelo(localizador: str):
    for i, vuelo in enumerate(VUELOS):
        if vuelo.id == localizador:  # Cambié localizador a id para que coincida con el modelo
            del VUELOS[i]
            guardar_vuelos()  # Guardar cambios en el archivo CSV
            return {"ok": True}
    raise HTTPException(status_code=404, detail="Vuelo no encontrado")

# Aquí puedes agregar la lógica para manejar reservas si es necesario.
