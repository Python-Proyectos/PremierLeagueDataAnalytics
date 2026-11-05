import pandas as pd
from pathlib import Path


def cargar_datos():
    """
    Carga el dataset de la Premier League 2018-2019.

    Returns:
        pd.DataFrame: Datos de los partidos.
    """

    # Obtener la ubicación principal del proyecto
    ruta_proyecto = Path(__file__).resolve().parent.parent

    # Construir la ruta del archivo CSV
    ruta_csv = ruta_proyecto / "data" / "soccer18-19.csv"

    # Comprobar que el archivo existe
    if not ruta_csv.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo: {ruta_csv}"
        )

    # Leer el archivo CSV
    df = pd.read_csv(ruta_csv)

    return df