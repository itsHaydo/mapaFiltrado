import csv

def obtener_rangos_de_datos(archivo_csv, nombre_columna, intervalo):
    rangos = {}
    with open(archivo_csv, 'r') as archivo:
        lector_csv = csv.DictReader(archivo)
        for fila in lector_csv:
            dato = float(fila[nombre_columna])
            indice_rango = int(dato // intervalo)
            rango = f"{indice_rango * intervalo + 1}-{(indice_rango + 1) * intervalo}"
            rangos.setdefault(rango, 0)
            rangos[rango] += 1

    for rango, cantidad in rangos.items():
        print(f"{rango}: {cantidad}")

# Ejemplo de uso:
obtener_rangos_de_datos('CSV\housing.csv', 'population', 5000)
