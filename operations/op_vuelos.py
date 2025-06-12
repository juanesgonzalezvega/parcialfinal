import csv
from typing import List
from models.vuelo import Vuelo

VUELOS_CSV = "vuelos.csv"


def listar_vuelos(origen: str = None, destino: str = None, fecha: str = None) -> List[Vuelo]:
    vuelos = []
    try:
        with open(VUELOS_CSV, newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                row['id'] = int(row['id'])
                row['sillasReservadas'] = int(row['sillasReservadas'])
                row['sillasVendidas'] = int(row['sillasVendidas'])
                vuelo = Vuelo(**row)
                if (origen is None or vuelo.origen == origen) and \
                        (destino is None or vuelo.destino == destino) and \
                        (fecha is None or vuelo.fecha == fecha):
                    vuelos.append(vuelo)
    except FileNotFoundError:
        pass
    return vuelos


def obtener_vuelo(vuelo_id: int) -> Vuelo:
    try:
        with open(VUELOS_CSV, newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if int(row['id']) == vuelo_id:
                    row['sillasReservadas'] = int(row['sillasReservadas'])
                    row['sillasVendidas'] = int(row['sillasVendidas'])
                    return Vuelo(**row)
    except FileNotFoundError:
        raise Exception("Archivo de vuelos no encontrado")
    raise Exception("Vuelo no encontrado")


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
    vuelos = []
    actualizado = False
    try:
        with open(VUELOS_CSV, newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if int(row['id']) == vuelo_id:
                    row.update(vuelo.dict())
                    actualizado = True
                vuelos.append(Vuelo(**row))
    except FileNotFoundError:
        raise Exception("Archivo de vuelos no encontrado")

    if not actualizado:
        raise Exception("Vuelo no encontrado")

    with open(VUELOS_CSV, "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=vuelo.dict().keys())
        writer.writeheader()
        for v in vuelos:
            writer.writerow(v.dict())
    return vuelo


def eliminar_vuelo(vuelo_id: int):
    vuelos = []
    eliminado = False
    try:
        with open(VUELOS_CSV, newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if int(row['id']) != vuelo_id:
                    vuelos.append(Vuelo(**row))
                else:
                    eliminado = True
    except FileNotFoundError:
        raise Exception("Archivo de vuelos no encontrado")

    if not eliminado:
        raise Exception("Vuelo no encontrado")

    with open(VUELOS_CSV, "w", newline='', encoding="utf-8") as csvfile:
        if vuelos:
            writer = csv.DictWriter(csvfile, fieldnames=vuelos[0].dict().keys())
            writer.writeheader()
            for v in vuelos:
                writer.writerow(v.dict())
    return {"ok": True}
