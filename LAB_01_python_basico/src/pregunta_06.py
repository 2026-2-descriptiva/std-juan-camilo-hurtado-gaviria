import csv
import gzip
from pathlib import Path
 
def pregunta_06():
    """
    La quinta columna (`metrics`) contiene pares `clave:valor` separados por
    comas. Para cada clave, encuentre el valor mínimo y el valor máximo que
    aparecen en todo el archivo. Retorne una lista de tuplas
    `(clave, mínimo, máximo)` ordenada alfabéticamente por la clave.

    Observe que el orden es mínimo y luego máximo, al contrario de la
    pregunta 5.

    Ejemplo del formato de la respuesta:

        [("aaa", 1, 9), ("bbb", 1, 9), ...]
    """

    PATH = Path(__file__).resolve().parents[1] / "data" / "data.csv.gz"
    with gzip.open(PATH, mode="rt", newline="", encoding="utf-8") as data_file:
        metrics_values = {}
        for row in csv.reader(data_file, delimiter="\t"):
            metrics = row[4].split(",")
            for metric in metrics:
                key, value = metric.split(":")
                value = int(value)
                if key not in metrics_values:
                    metrics_values[key] = (value, value)  
                else:
                    current_min, current_max = metrics_values[key]
                    metrics_values[key] = (min(current_min, value), max(current_max, value))
    return sorted((key, min_val, max_val) for key, (min_val, max_val) in metrics_values.items())

print(pregunta_06())