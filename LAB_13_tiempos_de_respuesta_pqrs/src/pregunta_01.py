import pandas as pd
from pathlib import Path


def pregunta_01() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Una entidad pública recibe peticiones, quejas, reclamos y sugerencias
    (PQRS) por dos canales, la página web y las cartas, y la ley le da 15 días
    hábiles para responder cada una. Su tarea es medir si la entidad cumple
    ese plazo.

    Los archivos `data/historical_requests_web.csv.gz` y
    `data/historical_requests_letter.csv.gz` tienen una fila por solicitud
    recibida entre 2016 y 2021 por cada canal, con su identificador
    (`record_id`), la fecha de entrada (`in_date`), el día de la semana de
    entrada (`day_name`) y la fecha de respuesta (`out_date`). Si `out_date`
    está vacía, la solicitud todavía no ha sido respondida.

    Tenga en cuenta lo siguiente:

    - Algunas solicitudes aparecen repetidas: elimine las filas idénticas
      dentro de cada canal, para contar cada solicitud una sola vez. Las
      filas sin `record_id` son solicitudes válidas.
    - Llame `letter` al canal de las cartas y `web` al de la página web.
    - Los días hábiles de respuesta son los días de lunes a viernes
      posteriores a la fecha de entrada, hasta la fecha de respuesta
      incluida. Por ejemplo, una solicitud que entra un viernes y se responde
      el lunes siguiente tardó 1 día hábil. No considere los festivos.
    - Los días calendario de respuesta son la diferencia entre la fecha de
      respuesta y la de entrada.
    - Una solicitud cumple el plazo si fue respondida en 15 días hábiles o
      menos. Una solicitud pendiente no ha cumplido el plazo.
    - `on_time_rate` es la proporción de solicitudes que cumplen el plazo,
      sobre el total de solicitudes, incluidas las pendientes.
    - Las medianas de días se calculan solamente con las solicitudes
      respondidas.

    Genere tres archivos en `submission/`, sin el índice de Pandas y con las
    columnas en el orden indicado:

    1. `channel_summary.csv`, con una fila por canal, en orden alfabético:
       `channel`, `requests`, `answered`, `pending`,
       `median_business_days` y `on_time_rate`.

    2. `yearly_summary.csv`, con una fila por año de entrada y canal,
       ordenada por año y luego por canal: `year`, `channel`, `requests`,
       `pending` y `on_time_rate`.

    3. `entry_day_summary.csv`, con una fila por día de entrada, de lunes a
       domingo, con los dos canales juntos: `day_name`, `requests`,
       `median_calendar_days` y `median_business_days`.

    Observe en el tercer archivo cómo cambia la lectura del tiempo de
    respuesta según se cuenten días calendario o días hábiles.

    La función también debe retornar las tres tablas, en el mismo orden.

    Ejemplo del formato de `channel_summary.csv`:

        channel,requests,answered,pending,median_business_days,on_time_rate
        letter,28138,...
        ...
    """

    activity_dir = Path(__file__).resolve().parent.parent
    data_file0 = activity_dir / "data" / "historical_requests_letter.csv.gz"
    data_file1 = activity_dir / "data" / "historical_requests_web.csv.gz"
    submission_dir = activity_dir / "submission"
    submission_dir.mkdir(parents=True, exist_ok=True)
    
    output_file0 = submission_dir / "channel_summary.csv"
    output_file1 = submission_dir / "yearly_summary.csv"
    output_file2 = submission_dir / "entry_day_summary.csv"

    df_letter = pd.read_csv(data_file0, parse_dates=["in_date", "out_date"])
    df_letter["channel"] = "letter"
    df_web = pd.read_csv(data_file1, parse_dates=["in_date", "out_date"])
    df_web["channel"] = "web"

    df_letter = df_letter.drop_duplicates()
    df_web = df_web.drop_duplicates()

    df = pd.concat([df_letter, df_web], ignore_index=True)

    df["calendar_days"] = (df["out_date"] - df["in_date"]).dt.days

    def compute_business_days(row):
        if pd.isna(row["out_date"]):
            return pd.NA
        return int(pd.bdate_range(start=row["in_date"] + pd.Timedelta(days=1), end=row["out_date"]).size)

    df["business_days"] = df.apply(compute_business_days, axis=1)

    df["answered"] = df["out_date"].notna()
    df["pending"] = df["out_date"].isna()
    df["on_time"] = df["answered"] & (df["business_days"] <= 15)

    df["year"] = df["in_date"].dt.year

    channel_groups = df.groupby("channel")
    channel_rows = []
    for channel, sub in channel_groups:
        requests = len(sub)
        answered = int(sub["answered"].sum())
        pending = int(sub["pending"].sum())
        median_business_days = float(sub.loc[sub["answered"], "business_days"].median()) if answered > 0 else 0.0
        on_time_rate = float(sub["on_time"].sum() / requests) if requests > 0 else 0.0

        channel_rows.append({
            "channel": channel,
            "requests": requests,
            "answered": answered,
            "pending": pending,
            "median_business_days": median_business_days,
            "on_time_rate": on_time_rate
        })

    df_channel = pd.DataFrame(channel_rows).sort_values("channel").reset_index(drop=True)
    df_channel.to_csv(output_file0, index=False)

    yearly_groups = df.groupby(["year", "channel"])
    yearly_rows = []
    for (year, channel), sub in yearly_groups:
        requests = len(sub)
        pending = int(sub["pending"].sum())
        on_time_rate = float(sub["on_time"].sum() / requests) if requests > 0 else 0.0

        yearly_rows.append({
            "year": year,
            "channel": channel,
            "requests": requests,
            "pending": pending,
            "on_time_rate": on_time_rate
        })

    df_yearly = pd.DataFrame(yearly_rows).sort_values(["year", "channel"]).reset_index(drop=True)
    df_yearly.to_csv(output_file1, index=False)

    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_groups = df.groupby("day_name")
    
    day_rows = []
    for day in day_order:
        if day in df["day_name"].values:
            sub = day_groups.get_group(day)
            requests = len(sub)
            median_calendar_days = float(sub.loc[sub["answered"], "calendar_days"].median()) if sub["answered"].sum() > 0 else 0.0
            median_business_days = float(sub.loc[sub["answered"], "business_days"].median()) if sub["answered"].sum() > 0 else 0.0
        else:
            requests = 0
            median_calendar_days = 0.0
            median_business_days = 0.0

        day_rows.append({
            "day_name": day,
            "requests": requests,
            "median_calendar_days": median_calendar_days,
            "median_business_days": median_business_days
        })

    df_entry_day = pd.DataFrame(day_rows)
    df_entry_day.to_csv(output_file2, index=False)

    return df_channel, df_yearly, df_entry_day
