import pandas as pd
from pathlib import Path
import re

def pregunta_01():
    """
    El archivo `data/solicitudes_de_credito.csv.gz` contiene las solicitudes de
    un programa de crédito, pero llegó sucio: tiene una columna de índice que
    no pertenece a los datos, registros duplicados, registros incompletos y
    valores que representan lo mismo escritos de formas distintas en los
    campos de texto, las fechas, el estrato y el monto.

    Su tarea es limpiarlo y guardar el resultado en
    `submission/solicitudes_de_credito.csv`, usando punto y coma (`;`) como
    separador y sin el índice de Pandas.

    El archivo limpio debe cumplir lo siguiente:

    - Contiene solamente las nueve columnas `sexo`, `tipo_de_emprendimiento`,
      `idea_negocio`, `barrio`, `estrato`, `comuna_ciudadano`,
      `fecha_de_beneficio`, `monto_del_credito` y `línea_credito`, en ese
      orden.
    - Los campos de texto están en minúsculas y sus palabras separadas por
      espacios.
    - `estrato` y `monto_del_credito` son números enteros, sin símbolos ni
      separadores de miles.
    - Todas las fechas de `fecha_de_beneficio` usan un mismo formato, por
      ejemplo `AAAA-MM-DD`.
    - No hay registros incompletos. La única excepción es
      `comuna_ciudadano`: sus valores faltantes son parte de los datos
      originales y deben conservarse.
    - No hay registros duplicados.

    Ejemplo del formato del archivo:

        sexo;tipo_de_emprendimiento;idea_negocio;barrio;estrato;...
        femenino;comercio;almacen de ropa en;los cerros el vergel;2;...
        ...
    """

    activity_dir = Path(__file__).resolve().parent.parent
    data_file = activity_dir / "data" / "solicitudes_de_credito.csv.gz"
    output_file = activity_dir / "submission" / "solicitudes_de_credito.csv"
    
    df = pd.read_csv(data_file, compression="gzip", sep=";", dtype=str)

    df = df.loc[:, ~df.columns.str.contains("^unnamed|^Unnamed", case=False)]
    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])

    required_columns = [
        "sexo",
        "tipo_de_emprendimiento",
        "idea_negocio",
        "barrio",
        "estrato",
        "comuna_ciudadano",
        "fecha_de_beneficio",
        "monto_del_credito",
        "línea_credito",
    ]

    df = df[[col for col in required_columns if col in df.columns]]

    def clean_text(val):
      if pd.isna(val):
          return pd.NA
      s = str(val).lower().replace("_", " ").replace("-", " ")
      s = " ".join(s.split())
      return pd.NA if s in ("", "nan") else s

    text_cols = ["sexo", "tipo_de_emprendimiento", "idea_negocio", "barrio", "línea_credito"]
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].apply(clean_text)

    def clean_estrato(val):
        if pd.isna(val) or str(val).strip() == "" or str(val).strip().lower() == "nan":
            return pd.NA
        s = str(val).strip()
        if s.endswith(".0"):
            s = s[:-2]
        try:
            return int(float(s))
        except ValueError:
            return pd.NA

    if "estrato" in df.columns:
        df["estrato"] = df["estrato"].apply(clean_estrato)

    def clean_monto(val):
      if pd.isna(val):
          return pd.NA
      s = re.sub(r"[^\d.,]", "", str(val))       
      s = re.sub(r"[.,]\d{1,2}$", "", s)          
      s = re.sub(r"\D", "", s)                    
      return int(s) if s else pd.NA

    if "monto_del_credito" in df.columns:
        df["monto_del_credito"] = df["monto_del_credito"].apply(clean_monto)

    def clean_comuna(val):
        if pd.isna(val) or str(val).strip() == "" or str(val).strip().lower() == "nan":
            return pd.NA
        s = str(val).strip()
        if s.endswith(".0"):
            s = s[:-2]
        return s
    if "comuna_ciudadano" in df.columns:
            df["comuna_ciudadano"] = df["comuna_ciudadano"].apply(clean_comuna)

    def clean_fecha(val):
      if pd.isna(val):
          return pd.NaT
      s = str(val).strip().replace("-", "/")
      fmt = "%Y/%m/%d" if re.match(r"^\d{4}/", s) else "%d/%m/%Y"
      return pd.to_datetime(s, format=fmt, errors="coerce")



    df["fecha_de_beneficio"] = df["fecha_de_beneficio"].apply(clean_fecha).dt.strftime("%Y-%m-%d")

    cols_to_check = [c for c in required_columns if c != "comuna_ciudadano"]
    df = df.dropna(subset=cols_to_check)

    df["estrato"] = df["estrato"].astype(int)
    df["monto_del_credito"] = df["monto_del_credito"].astype(int)

    
    df["comuna_ciudadano"] = df["comuna_ciudadano"].fillna("MISSING_COMUNA")
    df = df.drop_duplicates()
    df["comuna_ciudadano"] = df["comuna_ciudadano"].replace("MISSING_COMUNA", pd.NA)

    output_file.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_file, sep=";", index=False)

    return df



