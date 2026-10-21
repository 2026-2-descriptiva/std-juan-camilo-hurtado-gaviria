import csv
import gzip
from pathlib import Path

def pregunta_03():
    """
    Sume los valores de la segunda columna (`value`) para cada letra de la
    primera columna (`letter`). Retorne una lista de tuplas `(letra, suma)`
    ordenada alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 53), ("B", 36), ("C", 27), ...]
    """

    data_path = Path(__file__).resolve().parents[1] / "data" / "data.csv.gz"
    with gzip.open(data_path, mode="rt", newline="", encoding="utf-8") as data_file:
        letter_sums = {}
        for row in csv.reader(data_file, delimiter="\t"):
            letter = row[0]
            value = int(row[1])
            letter_sums[letter] = letter_sums.get(letter, 0) + value

    return sorted(letter_sums.items())
