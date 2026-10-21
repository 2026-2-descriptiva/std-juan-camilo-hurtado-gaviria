import pandas as pd
from pathlib import Path
def pregunta_06():
    """
    Usando `data/tbl1.tsv`, obtenga los valores distintos de la columna `c4`,
    conviértalos a mayúsculas y retórnelos como una lista ordenada
    alfabéticamente.

    Ejemplo del formato de la respuesta:

        ["A", "B", "C", "D", "E", "F", "G"]
    """

    INPUT_FILE=Path(__file__).resolve().parents[1] / "data" / "tbl1.tsv"
    df = pd.read_csv(INPUT_FILE, sep="\t")
    return sorted(df['c4'].str.upper().unique().tolist())
