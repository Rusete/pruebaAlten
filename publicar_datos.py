import requests
import csv
import os

# Configuración del ContextBroker
CONTEXT_BROKER_URL = "http://localhost:1026/v2/entities"

def procesar_csv(archivo_csv):
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
            
            # construir atributos dinámicamente
            for (nombre_atributo, tipo_atributo) in atributos:
                valor = fila[f"{nombre_atributo}<{tipo_atributo}>"]
                
                # convertir tipo de dato
                if tipo_atributo == "Number":
                    valor = float(valor) if "." in valor else int(valor)
                elif tipo_atributo == "Boolean":
                    valor = True if valor.lower() == "true" else False # Para que se coma también fallos de formato al escribir en el csv, Ejemplo: True, trUe, TRUE, etc. Se presupone que cualquier otro contenido es False
                else:  # Text, DateTime, etc.
                    valor = str(valor)
                
                entity[nombre_atributo] = {
                    "value": valor,
                    "type": tipo_atributo
                }
            
            # publicar en el ContextBroker
            response = requests.post(CONTEXT_BROKER_URL, json=entity)
            if response.status_code == 201:
                print(f"Entidad {entity['id']} creada!")
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
        procesar_csv(ruta_archivo)

# Ejecutar
procesar_carpeta("entities")