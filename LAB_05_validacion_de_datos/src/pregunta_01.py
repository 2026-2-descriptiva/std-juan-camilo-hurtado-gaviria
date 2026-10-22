import pandas as pd
from pathlib import Path
import re
import json

def main():
    """
    Antes de limpiar o analizar un conjunto de datos, un analista debe
    documentar qué problemas tiene. En este laboratorio usted no va a limpiar
    `data/ventas.csv.gz`: va a construir un reporte de calidad que deje evidencia
    de sus problemas, tal como están en el archivo.

    Lea `data/ventas.csv.gz` sin modificar sus valores. Para trabajar con los
    encabezados, normalícelos: páselos a minúsculas, elimine los espacios al
    inicio y al final (y cualquier marca BOM) y reemplace los espacios
    internos por `_`. Las columnas requeridas son `supplier_id`, `supplier`,
    `country`, `city`, `purchase_date`, `amount`, `discount`, `weight`,
    `units`, `unit_price` y `contact_email`.

    Escriba el reporte en `submission/data_quality_report.json` con estas
    claves:

    - `row_count`: cantidad de filas de datos.
    - `column_count`: cantidad de columnas.
    - `missing_required_columns`: lista ordenada de columnas requeridas que no
      están en el archivo.
    - `unexpected_columns`: lista ordenada de columnas del archivo que no son
      requeridas.
    - `duplicate_row_count`: cantidad de filas idénticas a una fila anterior.
    - `duplicate_supplier_id_row_count`: cantidad de filas cuyo `supplier_id`
      aparece más de una vez (cuente todas esas filas, no solo las
      repetidas).
    - `missing_value_count_by_column`: diccionario con la cantidad de valores
      faltantes de cada columna. Considere faltantes las celdas vacías y las
      que contienen `N/A`.
    - `invalid_email_count`: cantidad de valores de `contact_email` que no
      tienen la forma `usuario@dominio.extension`.
    - `invalid_unit_count`: cantidad de valores numéricos de `units` que no son
      enteros positivos. Los valores faltantes no se cuentan aquí.
    - `country_values`: lista ordenada de los valores distintos de `country`,
      escritos exactamente como aparecen en el archivo.

    La función también debe retornar el reporte como un diccionario.

    Ejemplo del formato del reporte:

        {
          "row_count": 103,
          "column_count": 11,
          "missing_required_columns": [],
          ...
          "country_values": [" Colombia ", "CO", ...]
        }
    """
    
    # Leer el archivo CSV sin modificar sus valores
    activity_dir = Path(__file__).resolve().parent.parent
    data_file = activity_dir / "data" / "ventas.csv.gz"
    df = pd.read_csv(data_file, compression='gzip', dtype=str)

    # Normalizar los encabezados
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

    # Columnas requeridas
    required_columns = {
        'supplier_id', 'supplier', 'country', 'city', 'purchase_date',
        'amount', 'discount', 'weight', 'units', 'unit_price', 'contact_email'
    }

    dup_supplier_count = int(df.duplicated(subset=['supplier_id'], keep=False).sum()) if 'supplier_id' in df.columns else 0
    missing_dict = {}
    for col in df.columns:
        s = df[col]
        is_missing = s.isna() | (s == '') | (s == 'N/A') | (s.str.strip() == '')
        missing_dict[col] = int(is_missing.sum())

    email_pattern = r'^[^@\s]+@[^@\s]+\.[^@\s]+$'
    def check_email(val):
        if pd.isna(val) or val in ['', 'N/A'] or not isinstance(val, str):
            return False
        return not bool(re.match(email_pattern, val.strip()))
    
    invalid_email_cnt = int(df['contact_email'].apply(check_email).sum()) if 'contact_email' in df.columns else 0

    def check_unit(val):
        if pd.isna(val) or val in ['', 'N/A']:
            return False
        try:
            num = float(val)
            # Debe ser un número entero estrictamente mayor a 0
            if num.is_integer() and int(num) > 0:
                return False
            return True
        except ValueError:
            return True

    invalid_unit_cnt = int(df['units'].apply(check_unit).sum()) if 'units' in df.columns else 0


    # Inicializar el reporte
    report = {
        "row_count": len(df),
        "column_count": len(df.columns),
        "missing_required_columns": sorted(list(required_columns - set(df.columns))),
        "unexpected_columns": sorted(list(set(df.columns) - required_columns)),
        "duplicate_row_count": int(df.duplicated().sum()),
        "duplicate_supplier_id_row_count": dup_supplier_count,
        "missing_value_count_by_column": missing_dict,
        "invalid_email_count": invalid_email_cnt,
        "invalid_unit_count": invalid_unit_cnt,
        "country_values": sorted(df['country'].dropna().unique().tolist()) if 'country' in df.columns else []
    }

    # Guardar el reporte en un archivo JSON
    submission_dir = activity_dir / "submission"
    submission_dir.mkdir(parents=True, exist_ok=True)
    report_file = submission_dir / "data_quality_report.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)

    return report

    




    
