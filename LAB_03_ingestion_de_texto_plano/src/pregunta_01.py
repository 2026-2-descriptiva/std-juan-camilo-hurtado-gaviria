import pandas as pd
from pathlib import Path
import re

def pregunta_01():
    """
    El archivo `data/clusters_report.txt` es un reporte de clústeres de
    palabras clave pensado para ser leído por una persona, no por un programa:
    los encabezados ocupan varias líneas, las columnas están alineadas con
    espacios y la lista de palabras clave de un clúster continúa en las líneas
    siguientes.

    Su tarea es convertir ese reporte en un DataFrame de Pandas con una fila
    por clúster y las columnas:

    - `cluster`: número del clúster, como entero.
    - `cantidad_de_palabras_clave`: como entero.
    - `porcentaje_de_palabras_clave`: como número decimal; por ejemplo, el
      texto `15,9 %` debe quedar como `15.9`.
    - `principales_palabras_clave`: todas las palabras clave del clúster en un
      solo texto, separadas por una coma y un único espacio.

    Retorne el DataFrame.

    Ejemplo del formato de la respuesta (se omite la última columna):

           cluster  cantidad_de_palabras_clave  porcentaje_de_palabras_clave
        0        1                         105                          15.9
        1        2                         102                          15.4
        ...
    """

    INPUT_FILE=Path(__file__).resolve().parents[1] / "data" / "clusters_report.txt"
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    data = []
    current_cluster = None
    current_cantidad = None
    current_porcentaje = None
    current_keywords = []

    
    pattern = re.compile(r'^\s*(\d+)\s+(\d+)\s+([\d,]+)\s*%\s+(.*)$')

    for line in lines[4:]:  
        if not line.strip():
            continue
        
        match = pattern.match(line)
        if match:
            
            if current_cluster is not None:
                kw_text = " ".join(" ".join(current_keywords).split())
                kw_text = kw_text.rstrip('.')
                data.append([current_cluster, current_cantidad, current_porcentaje, kw_text])
            
            current_cluster = int(match.group(1))
            current_cantidad = int(match.group(2))
            current_porcentaje = float(match.group(3).replace(',', '.'))
            current_keywords = [match.group(4).strip()]
        else:
            if current_cluster is not None:
                current_keywords.append(line.strip())

    if current_cluster is not None:
        kw_text = " ".join(" ".join(current_keywords).split())
        kw_text = kw_text.rstrip('.')
        data.append([current_cluster, current_cantidad, current_porcentaje, kw_text])

    df = pd.DataFrame(
        data,
        columns=[
            'cluster',
            'cantidad_de_palabras_clave',
            'porcentaje_de_palabras_clave',
            'principales_palabras_clave',
        ]
    )
    
    return df

print(pregunta_01())



    
