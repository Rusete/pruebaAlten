import requests
import csv
import os

# Configuración del ContextBroker
CONTEXT_BROKER_URL = "http://localhost:1026/v2/entities"

def borrar_entidades(archivo_csv):
    with open(archivo_csv, 'r', encoding='utf-8') as file:
            lector = csv.DictReader(file)
            
            # Extraer nombres y atributos
            campos = lector.fieldnames
            atributos = []
            
            for campo in campos[2:]:  # Ignorar entityID y entityType para poder procesar cada vila.
                nombre, tipo = campo.split("<")
                tipo = tipo.strip(">")
                atributos.append((nombre.strip(), tipo.strip()))
            
            # Procesar cada fila
            for fila in lector:
                entity = {
                    "id": fila["entityID"],
                    "type": fila["entityType"]
                }

                response = requests.delete(CONTEXT_BROKER_URL + '/' + entity['id'])
                if response.status_code == 204:
                    print(f"Entidad {entity['id']} borrada!")
                else:
                    print(f"Error {response.status_code} en {entity['id']}: {response.text}")

def procesar_carpeta(carpeta):
    # recuperar los archivos csv, en caso de haberlos.
    archivos_csv = [f for f in os.listdir(carpeta) if f.endswith(".csv")]
    
    if not archivos_csv:
        print(f"No hay archivos CSV en la carpeta {carpeta}.")
        return
    
    # ejecutar el script para cada uno de los archivos csv.
    for archivo in archivos_csv:
        ruta_archivo = os.path.join(carpeta, archivo)
        print(f"\nProcesando {ruta_archivo}...")
        borrar_entidades(ruta_archivo)

# Ejecutar
procesar_carpeta("entities")