import json
from pathlib import Path
import numpy as np
import pandas as pd

def pregunta_01():
    """
    Una aseguradora quiere publicar datos de sus afiliados para que un grupo
    de investigación estudie el costo de los seguros, sin que nadie pueda
    reconocer a una persona. El archivo `data/insurance.csv.gz` tiene una fila
    por afiliado con su edad (`age`), sexo (`sex`), índice de masa corporal
    (`bmi`), número de hijos (`children`), si fuma (`smoker`), región
    (`region`) y el costo de su seguro (`charges`).

    El archivo no tiene nombres ni documentos, pero eso no basta: la edad, el
    sexo, el índice de masa corporal, el número de hijos y la región son
    cuasi-identificadores, porque combinados pueden señalar a una persona.
    `smoker` es el atributo sensible que se quiere proteger.

    En este laboratorio usted va a medir el riesgo de reidentificación y a
    decidir qué publicar. Use estas definiciones:

    - Una clase de equivalencia es un grupo de registros con los mismos
      valores en todos los cuasi-identificadores. Un conjunto de datos cumple
      k-anonimato si toda clase tiene al menos k registros. Use k = 5.
    - `age_group`: `18-29`, `30-39`, `40-49` o `50-64`.
    - `bmi_group`: `bajo peso` (menos de 18.5), `normal` (desde 18.5 y menos
      de 25), `sobrepeso` (desde 25 y menos de 30) u `obesidad` (30 o más).
    - `children_group`: `0`, `1-2` o `3+`.

    Evalúe dos esquemas de generalización:

    - `with_children`: `age_group`, `sex`, `bmi_group`, `children_group` y
      `region`.
    - `without_children`: `age_group`, `sex`, `bmi_group` y `region`; el
      número de hijos no se publica.

    En cada esquema, suprima (no publique) los registros de las clases con
    menos de 5 registros. Luego, entre las clases publicadas, identifique las
    que no tienen diversidad en el atributo sensible, es decir, aquellas en
    las que todos los afiliados fuman o ninguno fuma: en esas clases, saber
    que alguien pertenece a ellas revela si fuma.

    Escriba `submission/privacy_report.json` con estas claves:

    - `original_k`: el menor tamaño de clase usando los cuasi-identificadores
      originales, sin generalizar.
    - `original_unique_records`: cuántos registros son los únicos de su clase
      con los cuasi-identificadores originales.
    - `schemes`: un diccionario con una entrada por esquema (`with_children` y
      `without_children`), cada una con las claves `quasi_identifiers` (la
      lista de columnas del esquema), `equivalence_classes` (clases antes de
      suprimir), `k_before_suppression`, `suppressed_records`,
      `published_records`, `published_classes`,
      `classes_without_smoker_diversity` y
      `records_without_smoker_diversity`.
    - `selected_scheme`: el esquema que suprime menos registros.
    - `mean_charges_original` y `mean_charges_published`: el costo promedio
      de todos los afiliados y el de los registros publicados con el esquema
      seleccionado.
    - `smoker_rate_original` y `smoker_rate_published`: la proporción de
      fumadores en ambos casos.

    Escriba también `submission/insurance_published.csv`, sin el índice de
    Pandas, con los registros publicados del esquema seleccionado, en el
    mismo orden del archivo original, y las columnas del esquema seguidas de
    `smoker` y `charges`.

    La función también debe retornar el reporte como un diccionario.

    Ejemplo del formato del reporte:

        {
          "original_k": 1,
          "original_unique_records": 1330,
          "schemes": {
            "with_children": {
              "quasi_identifiers": ["age_group", "sex", ...],
              "equivalence_classes": 278,
              ...
            },
            ...
          },
          ...
        }
    """
    activity_dir = Path(__file__).resolve().parent.parent
    data_file = activity_dir / "data" / "insurance.csv.gz"
    output_report = activity_dir / "submission" / "privacy_report.json"
    output_csv = activity_dir / "submission" / "insurance_published.csv"

    K = 5

    df = pd.read_csv(data_file, compression="gzip")

    # ---------- Riesgo con los cuasi-identificadores originales ----------
    original_qi = ["age", "sex", "bmi", "children", "region"]
    original_sizes = df.groupby(original_qi)["smoker"].transform("size")
    original_k = int(original_sizes.min())
    original_unique_records = int((original_sizes == 1).sum())

    # ---------- Generalización (pd.cut con right=False, como en el notebook) ----------
    df["age_group"] = pd.cut(
        df["age"],
        bins=[18, 30, 40, 50, 65],
        labels=["18-29", "30-39", "40-49", "50-64"],
        right=False,
    ).astype(str)

    df["bmi_group"] = pd.cut(
        df["bmi"],
        bins=[-np.inf, 18.5, 25, 30, np.inf],
        labels=["bajo peso", "normal", "sobrepeso", "obesidad"],
        right=False,
    ).astype(str)

    df["children_group"] = pd.cut(
        df["children"],
        bins=[-np.inf, 1, 3, np.inf],
        labels=["0", "1-2", "3+"],
        right=False,
    ).astype(str)

    schemes_qi = {
        "with_children": ["age_group", "sex", "bmi_group", "children_group", "region"],
        "without_children": ["age_group", "sex", "bmi_group", "region"],
    }

    schemes = {}
    published_by_scheme = {}
    is_smoker = (df["smoker"] == "yes").astype(int)

    for name, qi in schemes_qi.items():
        class_size = df.groupby(qi)["smoker"].transform("size")
        keep = class_size >= K
        published = df[keep]

        # Diversidad del atributo sensible entre las clases publicadas
        by_class = (
            is_smoker[keep]
            .groupby([published[c] for c in qi])
            .agg(["mean", "size"])
        )
        no_diversity = by_class[(by_class["mean"] == 0) | (by_class["mean"] == 1)]

        schemes[name] = {
            "quasi_identifiers": qi,
            "equivalence_classes": int(df.groupby(qi).ngroups),
            "k_before_suppression": int(class_size.min()),
            "suppressed_records": int((~keep).sum()),
            "published_records": int(keep.sum()),
            "published_classes": int(len(by_class)),
            "classes_without_smoker_diversity": int(len(no_diversity)),
            "records_without_smoker_diversity": int(no_diversity["size"].sum()),
        }
        published_by_scheme[name] = published

    # ---------- Esquema seleccionado: el que menos registros suprime ----------
    selected_scheme = min(schemes, key=lambda s: schemes[s]["suppressed_records"])
    published = published_by_scheme[selected_scheme]

    report = {
        "original_k": original_k,
        "original_unique_records": original_unique_records,
        "schemes": schemes,
        "selected_scheme": selected_scheme,
        "mean_charges_original": float(df["charges"].mean()),
        "mean_charges_published": float(published["charges"].mean()),
        "smoker_rate_original": float((df["smoker"] == "yes").mean()),
        "smoker_rate_published": float((published["smoker"] == "yes").mean()),
    }

    # ---------- Guardar ----------
    output_report.parent.mkdir(parents=True, exist_ok=True)
    with open(output_report, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    columns = schemes_qi[selected_scheme] + ["smoker", "charges"]
    published[columns].to_csv(output_csv, index=False)

    return report

  
