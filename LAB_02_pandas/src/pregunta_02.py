import pandas as pd
from pathlib import Path
def pregunta_02():
    """
    ¿Cuántas columnas tiene la tabla `data/tbl0.tsv`? Retorne la cantidad
    como un número entero.

    Ejemplo del formato de la respuesta:

        4
    """

    INPUT_FILE=Path(__file__).resolve().parents[1] / "data" / "tbl0.tsv"
    df = pd.read_csv(INPUT_FILE, sep="\t")
    return len(df.columns)
print(pregunta_02())
