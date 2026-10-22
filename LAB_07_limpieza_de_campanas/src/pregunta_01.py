import pandas as pd
from pathlib import Path


def clean_campaign_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Los datos de una campaña de mercadeo bancario llegaron repartidos en diez
    archivos comprimidos, `data/bank-marketing-campaing-*.csv.gz`, con
    información mezclada del cliente, de la campaña y del contexto económico.
    Su tarea es leerlos directamente desde los archivos comprimidos, sin
    descomprimirlos a mano, y separarlos en tres tablas limpias.

    Guarde cada tabla como un CSV sin comprimir en `submission/`, sin el índice
    de Pandas y con las columnas en el orden indicado:

    1. `client.csv`: `client_id`, `age`, `job`, `marital`, `education`,
       `credit_default` y `mortgage`.
       - En `job`, elimine los puntos y cambie los guiones por guiones bajos.
       - En `education`, cambie los puntos por guiones bajos y deje el valor
         `unknown` como faltante.
       - En `credit_default` y `mortgage`, escriba 1 si el valor es `yes` y 0
         en cualquier otro caso.

    2. `campaign.csv`: `client_id`, `number_contacts`, `contact_duration`,
       `previous_campaign_contacts`, `previous_outcome`, `campaign_outcome` y
       `last_contact_date`.
       - En `previous_outcome`, escriba 1 si el valor es `success` y 0 en
         cualquier otro caso.
       - En `campaign_outcome`, escriba 1 si el valor es `yes` y 0 en
         cualquier otro caso.
       - Construya `last_contact_date` a partir de las columnas `month` y
         `day`, usando el año 2022 y el formato `AAAA-MM-DD`.

    3. `economics.csv`: `client_id`, `cons_price_idx` y
       `euribor_three_months`.

    La función también debe retornar las tres tablas, en el orden `client`,
    `campaign` y `economics`.

    Ejemplo del formato de `campaign.csv`:

        client_id,number_contacts,contact_duration,...,last_contact_date
        0,1,261,...,2022-05-13
        ...
    """

    activity_dir = Path(__file__).resolve().parent.parent
    data_file0 = activity_dir / "data" / "bank-marketing-campaing-0.csv.gz"
    data_file1 = activity_dir / "data" / "bank-marketing-campaing-1.csv.gz"
    data_file2 = activity_dir / "data" / "bank-marketing-campaing-2.csv.gz"
    data_file3 = activity_dir / "data" / "bank-marketing-campaing-3.csv.gz"
    data_file4 = activity_dir / "data" / "bank-marketing-campaing-4.csv.gz"
    data_file5 = activity_dir / "data" / "bank-marketing-campaing-5.csv.gz"
    data_file6 = activity_dir / "data" / "bank-marketing-campaing-6.csv.gz"
    data_file7 = activity_dir / "data" / "bank-marketing-campaing-7.csv.gz"
    data_file8 = activity_dir / "data" / "bank-marketing-campaing-8.csv.gz"
    data_file9 = activity_dir / "data" / "bank-marketing-campaing-9.csv.gz"

    output_file1 = activity_dir / "submission" / "client.csv"
    output_file2 = activity_dir / "submission" / "campaign.csv"
    output_file3 = activity_dir / "submission" / "economics.csv"

    # Leer los archivos comprimidos y concatenarlos en un solo DataFrame
    df_list = []
    for data_file in [
        data_file0,
        data_file1,
        data_file2,
        data_file3,
        data_file4,
        data_file5,
        data_file6,
        data_file7,
        data_file8,
        data_file9,
    ]:
        df = pd.read_csv(data_file, compression="gzip", sep=",", dtype=str)
        df_list.append(df)

    df = pd.concat(df_list, ignore_index=True)
   
    df = df.loc[:, ~df.columns.str.contains("^unnamed", case=False)]

   
    cat_cols = [
        "job", "marital", "education", "credit_default", "mortgage",
        "month", "previous_outcome", "campaign_outcome",
    ]
    for col in cat_cols:
        df[col] = df[col].str.strip().str.lower()

    df["client_id"] = pd.to_numeric(df["client_id"]).astype(int)

    # client 
    client = df[
        ["client_id", "age", "job", "marital", "education",
         "credit_default", "mortgage"]
    ].copy()

    client["age"] = pd.to_numeric(client["age"]).astype(int)
    client["job"] = (
        client["job"]
        .str.replace(".", "", regex=False)
        .str.replace("-", "_", regex=False)
    )
    client["education"] = client["education"].str.replace(".", "_", regex=False)
    client["education"] = client["education"].mask(client["education"] == "unknown")
    client["credit_default"] = (client["credit_default"] == "yes").astype(int)
    client["mortgage"] = (client["mortgage"] == "yes").astype(int)

    # campaign 
    campaign = df[
        ["client_id", "number_contacts", "contact_duration",
         "previous_campaign_contacts", "previous_outcome",
         "campaign_outcome", "month", "day"]
    ].copy()

    for col in ["number_contacts", "contact_duration", "previous_campaign_contacts"]:
        campaign[col] = pd.to_numeric(campaign[col]).astype(int)

    campaign["previous_outcome"] = (campaign["previous_outcome"] == "success").astype(int)
    campaign["campaign_outcome"] = (campaign["campaign_outcome"] == "yes").astype(int)

    months = {
        "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
        "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
    }
    campaign["last_contact_date"] = pd.to_datetime(
        {
            "year": 2022,
            "month": campaign["month"].map(months),
            "day": pd.to_numeric(campaign["day"]).astype(int),
        }
    ).dt.strftime("%Y-%m-%d")

    campaign = campaign.drop(columns=["month", "day"])

    # economics
    economics = df[["client_id", "cons_price_idx", "euribor_three_months"]].copy()
    economics["cons_price_idx"] = pd.to_numeric(economics["cons_price_idx"])
    economics["euribor_three_months"] = pd.to_numeric(economics["euribor_three_months"])

    # guardar
    output_file1.parent.mkdir(parents=True, exist_ok=True)
    client.to_csv(output_file1, index=False)
    campaign.to_csv(output_file2, index=False)
    economics.to_csv(output_file3, index=False)

    return client, campaign, economics




    
