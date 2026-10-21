import csv
import gzip
from pathlib import Path
def pregunta_04():
    """
    Cuente cuántos registros hay en cada mes, usando la fecha de la tercera
    columna (`date`). Represente el mes como un texto de dos dígitos y retorne
    una lista de tuplas `(mes, cantidad)` ordenada por el mes.

    Ejemplo del formato de la respuesta:

        [("01", 3), ("02", 4), ("03", 2), ...]
    """

    data_path = Path(__file__).resolve().parents[1] / "data" / "data.csv.gz"
    with gzip.open(data_path, mode="rt", newline="", encoding="utf-8") as data_file:
        month_counts = {}
        for row in csv.reader(data_file, delimiter="\t"):
            date = row[2]
            month = date.split("-")[1]  
            month_counts[month] = month_counts.get(month, 0) + 1

    return sorted(month_counts.items())
