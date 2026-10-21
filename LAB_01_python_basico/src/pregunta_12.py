import csv
import gzip
from pathlib import Path
def pregunta_12():
    """
    Para cada letra de la primera columna (`letter`), sume todos los valores
    numéricos de los pares `clave:valor` de la quinta columna (`metrics`).
    Retorne un diccionario `{letra: suma}` con las letras en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"A": 177, "B": 187, "C": 114, ...}
    """

    PATH = Path(__file__).resolve().parents[1] / "data" / "data.csv.gz"
    with gzip.open(PATH, mode="rt", newline="", encoding="utf-8") as data_file:
        letter_sums = {}
        for row in csv.reader(data_file, delimiter="\t"):
            letter = row[0]
            metrics = row[4].split(",")
            total_value = sum(int(metric.split(":")[1]) for metric in metrics)
            letter_sums[letter] = letter_sums.get(letter, 0) + total_value
    return dict(sorted(letter_sums.items()))
