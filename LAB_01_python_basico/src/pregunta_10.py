import csv
import gzip
from pathlib import Path
def pregunta_10():
    """
    Para cada registro del archivo, en el mismo orden en que aparecen,
    retorne una tupla con la letra de la primera columna (`letter`), la
    cantidad de elementos de la cuarta columna (`codes`) y la cantidad de
    pares de la quinta columna (`metrics`). El resultado es una lista con una
    tupla por registro.

    Ejemplo del formato de la respuesta:

        [("E", 3, 5), ("A", 3, 4), ("B", 4, 4), ...]
    """

    PATH = Path(__file__).resolve().parents[1] / "data" / "data.csv.gz"
    with gzip.open(PATH, mode="rt", newline="", encoding="utf-8") as data_file:
        result = []
        for row in csv.reader(data_file, delimiter="\t"):
            letter = row[0]
            codes_count = len(row[3].split(","))
            metrics_count = len(row[4].split(","))
            result.append((letter, codes_count, metrics_count))
    return result
