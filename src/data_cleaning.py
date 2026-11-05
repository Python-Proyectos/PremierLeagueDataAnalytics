import pandas as pd


COLUMNAS_DEPORTIVAS = [
    "Div",
    "Date",
    "HomeTeam",
    "AwayTeam",
    "FTHG",
    "FTAG",
    "FTR",
    "HTHG",
    "HTAG",
    "HTR",
    "Referee",
    "HS",
    "AS",
    "HST",
    "AST",
    "HF",
    "AF",
    "HC",
    "AC",
    "HY",
    "AY",
    "HR",
    "AR"
]


def limpiar_datos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia y prepara los datos de la Premier League.

    Args:
        df: DataFrame original.

    Returns:
        DataFrame limpio.
    """

    print("\n=== INICIANDO LIMPIEZA DE DATOS ===")

    # Crear una copia para no modificar los datos originales
    df_limpio = df.copy()

    # Verificar que existan las columnas necesarias
    columnas_faltantes = [
        columna
        for columna in COLUMNAS_DEPORTIVAS
        if columna not in df_limpio.columns
    ]

    if columnas_faltantes:
        raise ValueError(
            f"Faltan columnas obligatorias: {columnas_faltantes}"
        )

    # Seleccionar únicamente las estadísticas deportivas
    df_limpio = df_limpio[COLUMNAS_DEPORTIVAS].copy()

    print("Columnas deportivas seleccionadas correctamente.")

    # Convertir fechas al formato datetime
    df_limpio["Date"] = pd.to_datetime(
        df_limpio["Date"],
        dayfirst=True,
        errors="raise"
    )

    print("Fechas convertidas correctamente.")

    # Eliminar espacios innecesarios en columnas de texto
    columnas_texto = [
        "Div",
        "HomeTeam",
        "AwayTeam",
        "FTR",
        "HTR",
        "Referee"
    ]

    for columna in columnas_texto:
        df_limpio[columna] = df_limpio[columna].str.strip()

    print("Columnas de texto normalizadas.")

    # Identificar registros duplicados
    duplicados = df_limpio.duplicated().sum()

    print(f"Registros duplicados encontrados: {duplicados}")

    # Eliminar registros duplicados exactos
    df_limpio = df_limpio.drop_duplicates()

    # Identificar valores nulos
    valores_nulos = df_limpio.isnull().sum().sum()

    print(f"Valores nulos encontrados: {valores_nulos}")

    # No eliminar automáticamente partidos con información faltante
    if valores_nulos > 0:
        raise ValueError(
            "El dataset contiene valores nulos que requieren revisión."
        )

    # Ordenar partidos cronológicamente
    df_limpio = df_limpio.sort_values(
        by="Date"
    ).reset_index(drop=True)

    print("Partidos ordenados cronológicamente.")

    print("\n=== LIMPIEZA FINALIZADA ===")

    print(f"Partidos disponibles: {len(df_limpio)}")
    print(f"Columnas disponibles: {len(df_limpio.columns)}")

    return df_limpio