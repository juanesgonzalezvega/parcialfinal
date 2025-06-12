import csv
from typing import List, Optional
from models.vuelo import Vuelo

VUELOS_CSV = "vuelos.csv"

def listar_vuelos(origen: Optional[str] = None, destino: Optional[str] = None, fecha: Optional[str] = None) -> List[Vuelo]:
    vuelos = []
    try:
        with open(VUELOS_CSV, newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    row['id'] = int(row['id'])
                    row['sillasReservadas'] = int(row['sillasReservadas'])
                    row['sillasVendidas'] = int(row['sillasVendidas'])
                    vuelo = Vuelo(**row)
                    if (origen and vuelo.origen != origen):
                        continue
                    if (destino and vuelo.destino != destino):
                        continue
                    if (fecha and vuelo.fecha != fecha):
                        continue
                    vuelos.append(vuelo)
                except Exception:
                    continue
    except FileNotFoundError:
        pass
    return vuelos

def obtener_vuelo(vuelo_id: int) -> Optional[Vuelo]:
    for vuelo in listar_vuelos():
        if vuelo.id == vuelo_id:
            return vuelo
    return None

def crear_vuelo(vuelo: Vuelo) -> Vuelo:
    vuelos = listar_vuelos()
    if any(v.id == vuelo.id for v in vuelos):
        raise Exception("El vuelo ya existe")
    with open(VUELOS_CSV, "a", newline='', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=vuelo.dict().keys())
        if csvfile.tell() == 0:
            writer.writeheader()
        writer.writerow(vuelo.dict())
    return vuelo

def actualizar_vuelo(vuelo_id: int, vuelo: Vuelo) -> Vuelo:
    vuelos = listar_vuelos()
    actualizado = False
    for i, v in enumerate(vuelos):
        if v.id == vuelo_id:
            vuelos[i] = vuelo
            actualizado = True
            break
    if not actualizado:
        raise Exception("Vuelo no encontrado")
    with open(VUELOS_CSV, "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=vuelo.dict().keys())
        writer.writeheader()
        for v in vuelos:
            writer.writerow(v.dict())
    return vuelo

def eliminar_vuelo(vuelo_id: int):
    vuelos = listar_vuelos()
    nuevos = [v for v in vuelos if v.id != vuelo_id]
    if len(nuevos) == len(vuelos):
        raise Exception("Vuelo no encontrado")
    with open(VUELOS_CSV, "w", newline='', encoding="utf-8") as csvfile:
        if nuevos:
            writer = csv.DictWriter(csvfile, fieldnames=nuevos[0].dict().keys())
            writer.writeheader()
            for v in nuevos:
                writer.writerow(v.dict())
    return {"ok": True}