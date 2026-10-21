
import csv
import gzip
from pathlib import Path


def pregunta_01():
    """
    Calcule la suma de los valores de la segunda columna (`value`) del
    archivo `data/data.csv.gz` y retorne el resultado como un número entero.

    Ejemplo del formato de la respuesta:

        214
    """

    data_path = Path(__file__).resolve().parents[1] / "data" / "data.csv.gz"
    with gzip.open(data_path, mode="rt", newline="", encoding="utf-8") as data_file:
       
        return sum(int(row[1]) for row in csv.reader(data_file, delimiter="\t"))




