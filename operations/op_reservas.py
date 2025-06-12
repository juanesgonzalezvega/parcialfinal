import csv
from typing import List
from models.reserva import Reserva

RESERVAS_CSV = "reservas.csv"

def listar_reservas() -> List[Reserva]:
    reservas = []
    try:
        with open(RESERVAS_CSV, newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                row['id'] = int(row['id'])
                row['vuelo_id'] = int(row['vuelo_id'])
                row['usuario_id'] = int(row['usuario_id'])
                reservas.append(Reserva(**row))
    except FileNotFoundError:
        pass
    return reservas

def crear_reserva(reserva: Reserva) -> Reserva:
    reservas = listar_reservas()
    if any(r.id == reserva.id for r in reservas):
        raise Exception("La reserva ya existe")
    with open(RESERVAS_CSV, "a", newline='', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=reserva.dict().keys())
        if csvfile.tell() == 0:
            writer.writeheader()
        writer.writerow(reserva.dict())
    return reserva

def obtener_reserva(reserva_id: int) -> Reserva:
    for reserva in listar_reservas():
        if reserva.id == reserva_id:
            return reserva
    raise Exception("Reserva no encontrada")

def actualizar_reserva(reserva_id: int, reserva: Reserva) -> Reserva:
    reservas = listar_reservas()
    actualizado = False
    for i, r in enumerate(reservas):
        if r.id == reserva_id:
            reservas[i] = reserva
            actualizado = True
            break
    if not actualizado:
        raise Exception("Reserva no encontrada")
    with open(RESERVAS_CSV, "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=reserva.dict().keys())
        writer.writeheader()
        for r in reservas:
            writer.writerow(r.dict())
    return reserva

def eliminar_reserva(reserva_id: int):
    reservas = listar_reservas()
    nuevos = [r for r in reservas if r.id != reserva_id]
    if len(nuevos) == len(reservas):
        raise Exception("Reserva no encontrada")
    with open(RESERVAS_CSV, "w", newline='', encoding="utf-8") as csvfile:
        if nuevos:
            writer = csv.DictWriter(csvfile, fieldnames=nuevos[0].dict().keys())
            writer.writeheader()
            for r in nuevos:
                writer.writerow(r.dict())
    return {"ok": True}
