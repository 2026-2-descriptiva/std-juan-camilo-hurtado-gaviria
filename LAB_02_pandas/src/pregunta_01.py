import pandas as pd
from pathlib import Path
def pregunta_01():
    """
    ¿Cuántos registros tiene la tabla `data/tbl0.tsv`? Retorne la cantidad
    como un número entero.

    Ejemplo del formato de la respuesta:

        40
    """
    INPUT_FILE=Path(__file__).resolve().parents[1] / "data" / "tbl0.tsv"
    df = pd.read_csv(INPUT_FILE, sep="\t")
    return len(df)

print(pregunta_01())
