import pandas as pd
from pathlib import Path

def pregunta_01() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Una cadena de suministros de oficina vende mucho, pero la gerencia
    sospecha que parte de esas ventas no deja utilidad. El archivo
    `data/superstore_orders.csv.gz` tiene una fila por línea de pedido, con
    el número de pedido (`Order ID`), las ventas (`Sales`), la utilidad
    (`Profit`), el descuento aplicado (`Discount`, como proporción), el
    segmento del cliente (`Customer Segment`) y la categoría del producto
    (`Product Category`). Una utilidad negativa significa que la línea se
    vendió con pérdida.

    Use estas definiciones:

    - Margen (`profit_margin`): utilidad sobre ventas.
    - Línea con pérdida: una línea cuya utilidad es negativa.
    - `loss_line_rate`: la proporción de líneas con pérdida.
    - `lost_profit`: la suma de las pérdidas de las líneas con pérdida,
      escrita como número positivo.
    - Rango de descuento (`discount_band`): `0%` si no hubo descuento,
      `1%-5%` si fue mayor que 0 y hasta 5 %, `6%-10%` si fue mayor que 5 % y
      hasta 10 %, y `más de 10%` en otro caso.

    Genere tres archivos en `submission/`, sin el índice de Pandas y con las
    columnas en el orden indicado:

    1. `profitability_summary.csv`, con una sola fila: `lines` (cantidad de
       líneas), `orders` (pedidos distintos), `sales`, `profit`,
       `profit_margin`, `loss_lines` (cantidad de líneas con pérdida),
       `loss_line_rate` y `lost_profit`.

    2. `discount_summary.csv`, con una fila por rango de descuento, en el
       orden en que se definieron arriba: `discount_band`, `lines`, `sales`,
       `profit`, `profit_margin`, `loss_line_rate` y `lost_profit`.

    3. `priority_segments.csv`, con los cinco segmentos segmento–categoría
       que más utilidad pierden: `Customer Segment`, `Product Category`,
       `lines`, `sales`, `profit`, `profit_margin` y `lost_profit`. Considere
       solamente segmentos con al menos 100 líneas y ordénelos por
       `lost_profit` de mayor a menor.

    La función también debe retornar las tres tablas, en el mismo orden.

    Ejemplo del formato de `discount_summary.csv`:

        discount_band,lines,sales,profit,profit_margin,loss_line_rate,...
        0%,166,170539.05,29472.3789,0.1728,0.488,...
        ...
    """

    activity_dir = Path(__file__).resolve().parent.parent
    data_file = activity_dir / "data" / "superstore_orders.csv.gz"
    output_file0 = activity_dir / "submission" / "profitability_summary.csv"
    output_file1 = activity_dir / "submission" / "discount_summary.csv"
    output_file2 = activity_dir / "submission" / "priority_segments.csv"

    submission_dir = activity_dir / "submission"
    submission_dir.mkdir(parents=True, exist_ok=True)


    df = pd.read_csv(data_file, compression="gzip", sep=";")

    for col in ['Sales', 'Profit', 'Discount']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(',', '.', regex=False).astype(float)

    # 1. profitability_summary.csv
    lines = len(df)
    orders = df['Order ID'].nunique()
    sales = df['Sales'].sum()
    profit = df['Profit'].sum()
    profit_margin = profit / sales if sales != 0 else 0
    loss_lines = df[df['Profit'] < 0].shape[0]
    loss_line_rate = loss_lines / lines if lines != 0 else 0
    lost_profit = df[df['Profit'] < 0]['Profit'].abs().sum()

    df_profitability = pd.DataFrame([{
        'lines': lines,
        'orders': orders,
        'sales': sales,
        'profit': profit,
        'profit_margin': profit_margin,
        'loss_lines': loss_lines,
        'loss_line_rate': loss_line_rate,
        'lost_profit': lost_profit
    }])
    df_profitability.to_csv(output_file0, index=False)

    # 2. discount_summary.csv
    def assign_discount_band(d):
        if d == 0:
            return '0%'
        elif d <= 0.05:
            return '1%-5%'
        elif d <= 0.10:
            return '6%-10%'
        else:
            return 'más de 10%'

    df['discount_band'] = df['Discount'].apply(assign_discount_band)
    band_order = ['0%', '1%-5%', '6%-10%', 'más de 10%']

    discount_rows = []
    for band in band_order:
        sub = df[df['discount_band'] == band]
        sub_lines = len(sub)
        sub_sales = sub['Sales'].sum()
        sub_profit = sub['Profit'].sum()
        sub_margin = sub_profit / sub_sales if sub_sales != 0 else 0
        sub_loss_lines = (sub['Profit'] < 0).sum()
        sub_loss_rate = sub_loss_lines / sub_lines if sub_lines != 0 else 0
        sub_lost_profit = sub.loc[sub['Profit'] < 0, 'Profit'].abs().sum()
        
        discount_rows.append({
            'discount_band': band,
            'lines': sub_lines,
            'sales': sub_sales,
            'profit': sub_profit,
            'profit_margin': sub_margin,
            'loss_line_rate': sub_loss_rate,
            'lost_profit': sub_lost_profit
        })

    df_discount = pd.DataFrame(discount_rows)
    df_discount.to_csv(output_file1, index=False)

    # 3. priority_segments.csv 
    segment_groups = df.groupby(['Customer Segment', 'Product Category'])
    
    seg_rows = []
    for (seg, cat), sub in segment_groups:
        sub_lines = len(sub)
        if sub_lines >= 100:
            sub_sales = sub['Sales'].sum()
            sub_profit = sub['Profit'].sum()
            sub_margin = sub_profit / sub_sales if sub_sales != 0 else 0
            sub_lost_profit = sub.loc[sub['Profit'] < 0, 'Profit'].abs().sum()
            
            seg_rows.append({
                'Customer Segment': seg,
                'Product Category': cat,
                'lines': sub_lines,
                'sales': sub_sales,
                'profit': sub_profit,
                'profit_margin': sub_margin,
                'lost_profit': sub_lost_profit
            })

    df_priority = pd.DataFrame(seg_rows)
    if not df_priority.empty:
        df_priority = df_priority.sort_values(by='lost_profit', ascending=False).head(5)
    df_priority.to_csv(output_file2, index=False)

    return df_profitability, df_discount, df_priority






    
      


    
