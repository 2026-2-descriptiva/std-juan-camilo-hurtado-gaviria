import pandas as pd
from pathlib import Path
def pregunta_10():
    """
    Usando `data/tbl0.tsv`, construya para cada categoría de la columna `c1`
    un texto con todos sus valores de la columna `c2`, ordenados de menor a
    mayor y separados por `:`. Retorne un DataFrame cuyo índice son las
    categorías, en orden alfabético, con una única columna llamada `c2`.

    Ejemplo del formato de la respuesta:

                           c2
        c1
        A     1:1:2:3:6:7:8:9
        B       1:3:4:5:6:8:9
        C           0:5:6:7:9
        ...
    """

    INPUT_FILE=Path(__file__).resolve().parents[1] / "data" / "tbl0.tsv"
    df = pd.read_csv(INPUT_FILE, sep="\t")
    df_grouped = df.groupby('c1')['c2'].apply(lambda x: ':'.join(map(str, sorted(x)))).reset_index()
    df_grouped.columns = ['c1', 'c2']
    return df_grouped.set_index('c1').sort_index()
