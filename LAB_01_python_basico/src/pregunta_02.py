import csv
import gzip
from pathlib import Path

def pregunta_02():
    """
    Cuente cuántos registros hay para cada letra de la primera columna
    (`letter`). Retorne una lista de tuplas `(letra, cantidad)` ordenada
    alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 8), ("B", 7), ("C", 5), ...]
    """

    data_path = Path(__file__).resolve().parents[1] / "data" / "data.csv.gz"
    with gzip.open(data_path, mode="rt", newline="", encoding="utf-8") as data_file:
        letter_counts = {}
        for row in csv.reader(data_file, delimiter="\t"):
            letter = row[0]
            letter_counts[letter] = letter_counts.get(letter, 0) + 1

    return sorted(letter_counts.items())
