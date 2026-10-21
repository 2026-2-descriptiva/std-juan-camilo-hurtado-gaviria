import pandas as pd
from pathlib import Path
def pregunta_05():
    """
    Usando `data/tbl0.tsv`, encuentre el valor máximo de la columna `c2` para
    cada categoría de la columna `c1`. Retorne una Serie de Pandas cuyo índice
    son las categorías, en orden alfabético, y cuyos valores son los máximos.

    Ejemplo del formato de la respuesta:

        c1
        A    9
        B    9
        C    9
        ...
    """

    INPUT_FILE=Path(__file__).resolve().parents[1] / "data" / "tbl0.tsv"
    df = pd.read_csv(INPUT_FILE, sep="\t")
    return df.groupby('c1')['c2'].max().sort_index()
