import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

def build_cohort_analysis() -> pd.DataFrame:
    """
    Una tienda quiere saber si sus clientes vuelven a comprar después de su
    primera compra. Para responder, agrupe a los clientes en cohortes según
    el mes de su primera compra y mida, mes a mes, qué proporción de cada
    cohorte vuelve a comprar. Use `data/sales.csv.gz`, que tiene una fila por
    orden con su cliente (`CustomerID`) y su fecha (`OrderDate`).

    Use estas definiciones:

    - `cohort_month`: el mes de la primera compra del cliente, escrito como
      `AAAA-MM`.
    - `period_index`: los meses transcurridos desde `cohort_month`; es 0 en el
      mes de la primera compra, 1 en el mes siguiente, y así sucesivamente.
    - `active_customers`: la cantidad de clientes distintos de la cohorte que
      compraron en ese período.
    - `cohort_size`: la cantidad de clientes de la cohorte, es decir, sus
      clientes activos en el período 0.
    - `retention_rate`: `active_customers` sobre `cohort_size`.

    Genere dos archivos en `submission/`:

    1. `cohort_retention.csv`, sin el índice de Pandas, con las columnas
       `cohort_month`, `period_index`, `active_customers`, `cohort_size` y
       `retention_rate`, y una fila por cada combinación cohorte–período
       observada, ordenadas por cohorte y período.

    2. `cohort_retention_heatmap.png`, un mapa de calor de `retention_rate`
       con una fila por cohorte (eje vertical) y una columna por período
       (eje horizontal). Muestre los valores como porcentajes. Los períodos
       que todavía no se pueden observar para una cohorte no significan
       retención cero: déjelos vacíos en el mapa.

    La función también debe retornar la tabla de retención.

    Ejemplo del formato de `cohort_retention.csv`:

        cohort_month,period_index,active_customers,cohort_size,retention_rate
        2022-01,0,100,100,1.0
        2022-01,1,26,100,0.26
        ...
    """

    activity_dir = Path(__file__).resolve().parent.parent
    data_file = activity_dir / "data" / "sales.csv.gz"
    submission_dir = activity_dir / "submission"
    submission_dir.mkdir(parents=True, exist_ok=True)
    
    output_csv = submission_dir / "cohort_retention.csv"
    output_png = submission_dir / "cohort_retention_heatmap.png"

    df = pd.read_csv(data_file, compression="gzip", sep=",")

    df['OrderDate'] = pd.to_datetime(df['OrderDate'])
    df['order_year_month'] = df['OrderDate'].dt.to_period('M')

    df['cohort_month_period'] = df.groupby('CustomerID')['order_year_month'].transform('min')
    
    year_diff = df['order_year_month'].dt.year - df['cohort_month_period'].dt.year
    month_diff = df['order_year_month'].dt.month - df['cohort_month_period'].dt.month
    df['period_index'] = year_diff * 12 + month_diff

    df['cohort_month'] = df['cohort_month_period'].dt.strftime('%Y-%m')

    cohort_counts = df.groupby(['cohort_month', 'period_index'])['CustomerID'].nunique().reset_index()
    cohort_counts = cohort_counts.rename(columns={'CustomerID': 'active_customers'})

    cohort_sizes = cohort_counts[cohort_counts['period_index'] == 0][['cohort_month', 'active_customers']]
    cohort_sizes = cohort_sizes.rename(columns={'active_customers': 'cohort_size'})
    
    cohort_counts = pd.merge(cohort_counts, cohort_sizes, on='cohort_month')

    cohort_counts['retention_rate'] = cohort_counts['active_customers'] / cohort_counts['cohort_size']

    cohort_counts = cohort_counts.sort_values(['cohort_month', 'period_index']).reset_index(drop=True)
    
    cohort_counts = cohort_counts[['cohort_month', 'period_index', 'active_customers', 'cohort_size', 'retention_rate']]

    # Guardar el archivo CSV 
    cohort_counts.to_csv(output_csv, index=False)

    pivot_table = cohort_counts.pivot(index='cohort_month', columns='period_index', values='retention_rate')

    plt.figure(figsize=(12, 8))
    sns.heatmap(pivot_table, annot=True, fmt='.0%', cmap='Blues', cbar=True, linewidths=.5)
    plt.title('Cohort Analysis - Retention Rate', fontsize=14, pad=15)
    plt.xlabel('Period Index (Months)', fontsize=12)
    plt.ylabel('Cohort Month', fontsize=12)
    plt.tight_layout()

    plt.savefig(output_png)
    plt.close()

    return cohort_counts

    
