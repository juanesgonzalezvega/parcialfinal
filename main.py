from fastapi import FastAPI, HTTPException
from typing import List
from schemas import Usuario, Mascota, Vuelo, Reserva
from database import USUARIOS, MASCOTAS, VUELOS, RESERVAS

app = FastAPI(title="ParcialFinal - Vuelos para Mascotas")

# Este es de USUARIOS
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
    return usuario

@app.put("/usuarios/{user_id}", response_model=Usuario)
def actualizar_usuario(user_id: int, usuario: Usuario):
    for i, user in enumerate(USUARIOS):
        if user.id == user_id:
            USUARIOS[i] = usuario
            return usuario
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.delete("/usuarios/{user_id}")
def eliminar_usuario(user_id: int):
    for i, user in enumerate(USUARIOS):
        if user.id == user_id:
            del USUARIOS[i]
            return {"ok": True}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

# Este es de MASCOTAS
@app.get("/mascotas", response_model=List[Mascota])
def listar_mascotas():
    return MASCOTAS

@app.get("/mascotas/{mascota_id}", response_model=Mascota)
def obtener_mascota(mascota_id: int):
    for mas in MASCOTAS:
        if mas.id == mascota_id:
            return mas
    raise HTTPException(status_code=404, detail="Mascota no encontrada")

@app.get("/usuarios/{user_id}/mascotas", response_model=List[Mascota])
def mascotas_por_usuario(user_id: int):
    return [m for m in MASCOTAS if m.duenio_id == user_id]

@app.post("/mascotas", response_model=Mascota)
def crear_mascota(mascota: Mascota):
    MASCOTAS.append(mascota)
    return mascota

@app.put("/mascotas/{mascota_id}", response_model=Mascota)
def actualizar_mascota(mascota_id: int, mascota: Mascota):
    for i, mas in enumerate(MASCOTAS):
        if mas.id == mascota_id:
            MASCOTAS[i] = mascota
            return mascota
    raise HTTPException(status_code=404, detail="Mascota no encontrada")

@app.delete("/mascotas/{mascota_id}")
def eliminar_mascota(mascota_id: int):
    for i, mas in enumerate(MASCOTAS):
        if mas.id == mascota_id:
            del MASCOTAS[i]
            return {"ok": True}
    raise HTTPException(status_code=404, detail="Mascota no encontrada")

# Este es de VUELOS
@app.get("/vuelos", response_model=List[Vuelo])
def listar_vuelos(origen: str = None, destino: str = None, fecha: str = None):
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
        if vuelo.localizador == localizador:
            return vuelo
    raise HTTPException(status_code=404, detail="Vuelo no encontrado")

@app.post("/vuelos", response_model=Vuelo)
def crear_vuelo(vuelo: Vuelo):
    VUELOS.append(vuelo)
    return vuelo

@app.put("/vuelos/{localizador}", response_model=Vuelo)
def actualizar_vuelo(localizador: str, vuelo: Vuelo):
    for i, v in enumerate(VUELOS):
        if v.localizador == localizador:
            VUELOS[i] = vuelo
            return vuelo
    raise HTTPException(status_code=404, detail="Vuelo no encontrado")

@app.delete("/vuelos/{localizador}")
def eliminar_vuelo(localizador: str):
    for i, vuelo in enumerate(VUELOS):
        if vuelo.localizador == localizador:
            del VUELOS[i]
            return {"ok": True}
    raise HTTPException(status_code=404, detail="Vuelo no encontrado")

@app.get("/vuelos/{localizador}/mascotas/count")
def contar_mascotas_en_vuelo(localizador: str):
    total = 0
    for reserva in RESERVAS:
        if reserva.vuelo_localizador == localizador:
            total += len(reserva.mascotas)
    return {"mascotas_en_vuelo": total}

# Este es de RESERVAS
@app.get("/reservas", response_model=List[Reserva])
def listar_reservas():
    return RESERVAS

@app.get("/reservas/{reserva_id}", response_model=Reserva)
def obtener_reserva(reserva_id: int):
    for r in RESERVAS:
        if r.id == reserva_id:
            return r
    raise HTTPException(status_code=404, detail="Reserva no encontrada")

@app.post("/reservas", response_model=Reserva)
def crear_reserva(reserva: Reserva):
    # Validar disponibilidad de sillas
    vuelo = next((v for v in VUELOS if v.localizador == reserva.vuelo_localizador), None)
    if vuelo is None:
        raise HTTPException(status_code=404, detail="Vuelo no encontrado")
    mascotas_en_vuelo = sum(len(r.mascotas) for r in RESERVAS if r.vuelo_localizador == vuelo.localizador)
    if mascotas_en_vuelo + len(reserva.mascotas) > vuelo.sillas_res:
        raise HTTPException(status_code=400, detail="No hay suficientes cupos para mascotas en este vuelo")
    RESERVAS.append(reserva)
    vuelo.sillas_ven += len(reserva.mascotas)
    return reserva

@app.put("/reservas/{reserva_id}", response_model=Reserva)
def actualizar_reserva(reserva_id: int, reserva: Reserva):
    for i, r in enumerate(RESERVAS):
        if r.id == reserva_id:
            RESERVAS[i] = reserva
            return reserva
    raise HTTPException(status_code=404, detail="Reserva no encontrada")

@app.post("/reservas/{reserva_id}/comprar")
def comprar_reserva(reserva_id: int):
    for r in RESERVAS:
        if r.id == reserva_id:
            r.pagado = True
            return {"ok": True}
    raise HTTPException(status_code=404, detail="Reserva no encontrada")

@app.delete("/reservas/{reserva_id}")
def eliminar_reserva(reserva_id: int):
    for i, r in enumerate(RESERVAS):
        if r.id == reserva_id:
            del RESERVAS[i]
            return {"ok": True}
    raise HTTPException(status_code=404, detail="Reserva no encontrada")
