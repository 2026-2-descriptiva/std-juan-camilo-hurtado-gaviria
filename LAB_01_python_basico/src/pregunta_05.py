import csv
import gzip
from pathlib import Path
def pregunta_05():
    """
    Para cada letra de la primera columna (`letter`), encuentre el valor
    máximo y el valor mínimo de la segunda columna (`value`). Retorne una lista
    de tuplas `(letra, máximo, mínimo)` ordenada alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 9, 2), ("B", 9, 1), ...]
    """

    data_path = Path(__file__).resolve().parents[1] / "data" / "data.csv.gz"
    with gzip.open(data_path, mode="rt", newline="", encoding="utf-8") as data_file:
        letter_values = {}
        for row in csv.reader(data_file, delimiter="\t"):
            letter = row[0]
            value = int(row[1])
            if letter not in letter_values:
                letter_values[letter] = (value, value)  
            else:
                current_max, current_min = letter_values[letter]
                letter_values[letter] = (max(current_max, value), min(current_min, value))

    return sorted((letter, max_val, min_val) for letter, (max_val, min_val) in letter_values.items())
