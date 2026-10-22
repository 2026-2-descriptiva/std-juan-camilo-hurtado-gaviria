import pandas as pd
from pathlib import Path

def pregunta_01():
    """
    Las frases de este laboratorio no están en una tabla, sino en miles de
    archivos de texto organizados en carpetas. Dentro de `data/` hay dos
    carpetas, `train/` y `test/`, y cada una contiene las carpetas
    `negative/`, `neutral/` y `positive/`. Cada archivo `.txt` contiene una
    frase, y la carpeta donde se encuentra indica su sentimiento.

    Su tarea es construir un dataset para cada división y guardarlo en:

    - `submission/train_dataset.csv`
    - `submission/test_dataset.csv`

    Cada archivo debe tener dos columnas: `phrase`, con el texto de la frase,
    y `target`, con el nombre de la carpeta de sentimiento (`negative`,
    `neutral` o `positive`). Recorra las carpetas y los archivos en orden
    alfabético, de modo que el resultado sea siempre el mismo. No guarde el
    índice de Pandas en el CSV.

    Ejemplo del formato de cada archivo:

        phrase,target
        "The real estate company posted a net loss ...",negative
        ...
        "Cardona slowed her vehicle , turned around ...",neutral
        ...
    """
    
    activity_dir = Path(__file__).resolve().parent.parent
    train_dir = activity_dir / "data" / "train"
    test_dir = activity_dir / "data" / "test"
    submission_dir = activity_dir / "submission"
    submission_dir.mkdir(parents=True, exist_ok=True)

    # Crear listas para almacenar las frases y sus etiquetas
    train_data = []
    test_data = []

    # Función para procesar un directorio y extraer frases y etiquetas
    def process_directory(directory, data_list):
        for sentiment_dir in sorted(directory.iterdir()):
            if sentiment_dir.is_dir():
                sentiment = sentiment_dir.name
                for txt_file in sorted(sentiment_dir.glob("*.txt")):
                    with open(txt_file, "r", encoding="utf-8") as file:
                        phrase = file.read().strip()
                        data_list.append({"phrase": phrase, "target": sentiment})

    # Procesar los directorios de entrenamiento y prueba
    process_directory(train_dir, train_data)
    process_directory(test_dir, test_data)

    # Crear DataFrames a partir de las listas de datos
    train_df = pd.DataFrame(train_data)
    test_df = pd.DataFrame(test_data)

    # Guardar los DataFrames en archivos CSV sin índice
    train_df.to_csv(submission_dir / "train_dataset.csv", index=False)
    test_df.to_csv(submission_dir / "test_dataset.csv", index=False)

    
