import csv
from typing import List
from models.reserva import Reserva

RESERVAS_CSV = "reservas.csv"


def listar_reservas_por_vuelo(vuelo_id: int) -> List[Reserva]:
    reservas = []
    try:
        with open(RESERVAS_CSV, newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if int(row['vuelo_id']) == vuelo_id:
                    row['id'] = int(row['id'])
                    reservas.append(Reserva(**row))
    except FileNotFoundError:
        pass
    return reservas


def obtener_reserva(reserva_id: int) -> Reserva:
    try:
        with open(RESERVAS_CSV, newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if int(row['id']) == reserva_id:
                    row['vuelo_id'] = int(row['vuelo_id'])
                    row['usuario_id'] = int(row['usuario_id'])
                    return Reserva(**row)
    except FileNotFoundError:
        raise Exception("Archivo de reservas no encontrado")
    raise Exception("Reserva no encontrada")


def crear_reserva(vuelo_id: int, reserva: Reserva) -> Reserva:
    reservas = listar_reservas_por_vuelo(vuelo_id)
    if any(r.id == reserva.id for r in reservas):
        raise Exception("La reserva ya existe")

    with open(RESERVAS_CSV, "a", newline='', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=reserva.dict().keys())
        if csvfile.tell() == 0:
            writer.writeheader()
        writer.writerow(reserva.dict())
    return reserva


def actualizar_reserva(reserva_id: int, reserva: Reserva) -> Reserva:
    reservas = []
    actualizado = False
    try:
        with open(RESERVAS_CSV, newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if int(row['id']) == reserva_id:
                    row.update(reserva.dict())
                    actualizado = True
                reservas.append(Reserva(**row))
    except FileNotFoundError:
        raise Exception("Archivo de reservas no encontrado")

    if not actualizado:
        raise Exception("Reserva no encontrada")

    with open(RESERVAS_CSV, "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=reserva.dict().keys())
        writer.writeheader()
        for r in reservas:
            writer.writerow(r.dict())
    return reserva


def eliminar_reserva(reserva_id: int):
    reservas = []
    eliminado = False
    try:
        with open(RESERVAS_CSV, newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if int(row['id']) != reserva_id:
                    reservas.append(Reserva(**row))
                else:
                    eliminado = True
    except FileNotFoundError:
        raise Exception("Archivo de reservas no encontrado")

    if not eliminado:
        raise Exception("Reserva no encontrada")

    with open(RESERVAS_CSV, "w", newline='', encoding="utf-8") as csvfile:
        if reservas:
            writer = csv.DictWriter(csvfile, fieldnames=reservas[0].dict().keys())
            writer.writeheader()
            for r in reservas:
                writer.writerow(r.dict())
    return {"ok": True}
