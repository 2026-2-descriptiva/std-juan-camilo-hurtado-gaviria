import csv
import gzip
from pathlib import Path
def pregunta_08():
    """
    Repita la pregunta 7, pero ahora cada lista de letras debe contener cada
    letra una sola vez y estar ordenada alfabéticamente. Retorne una lista de
    tuplas `(valor, letras)` ordenada por el valor.

    Ejemplo del formato de la respuesta:

        [(0, ["C"]), (1, ["B", "E"]), (2, ["A", "E"]), ...]
    """

    PATH = Path(__file__).resolve().parents[1] / "data" / "data.csv.gz"
    with gzip.open(PATH, mode="rt", newline="", encoding="utf-8") as data_file:
        value_to_letters = {}
        for row in csv.reader(data_file, delimiter="\t"):
            letter = row[0]
            value = int(row[1])
            if value not in value_to_letters:
                value_to_letters[value] = []
            value_to_letters[value].append(letter)

    
    for value in value_to_letters:
        value_to_letters[value] = sorted(list(set(value_to_letters[value])))

    return sorted(value_to_letters.items())
