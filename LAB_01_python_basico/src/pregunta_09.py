import csv
import gzip
from pathlib import Path
def pregunta_09():
    """
    Cuente cuántas veces aparece cada clave en la quinta columna (`metrics`)
    de todo el archivo. Retorne un diccionario `{clave: cantidad}` con las
    claves en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"aaa": 13, "bbb": 16, "ccc": 23, ...}
    """

    PATH = Path(__file__).resolve().parents[1] / "data" / "data.csv.gz"
    with gzip.open(PATH, mode="rt", newline="", encoding="utf-8") as data_file:
        key_counts = {}
        for row in csv.reader(data_file, delimiter="\t"):
            metrics = row[4].split(",")
            for metric in metrics:
                key, _ = metric.split(":")
                key_counts[key] = key_counts.get(key, 0) + 1
    return dict(sorted(key_counts.items()))



    
