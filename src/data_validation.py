import pandas as pd


def validar_datos(df: pd.DataFrame) -> None:
    """
    Valida la integridad deportiva del dataset
    de la Premier League 2018-2019.
    """

    print("\n=== VALIDACIÓN DE CALIDAD DE DATOS ===")

    errores = []

    # 1. Verificar cantidad de equipos
    equipos = set(df["HomeTeam"]) | set(df["AwayTeam"])

    print(f"\nEquipos encontrados: {len(equipos)}")

    if len(equipos) != 20:
        errores.append(
            f"Se esperaban 20 equipos, pero se encontraron {len(equipos)}."
        )

    # 2. Verificar partidos por equipo
    partidos_local = df["HomeTeam"].value_counts()
    partidos_visitante = df["AwayTeam"].value_counts()

    partidos_totales = (
        partidos_local.add(partidos_visitante, fill_value=0)
        .astype(int)
    )

    print("\n=== PARTIDOS POR EQUIPO ===")
    print(partidos_totales.sort_index().to_string())

    equipos_incorrectos = partidos_totales[
        partidos_totales != 38
    ]

    if not equipos_incorrectos.empty:
        errores.append(
            "Existen equipos que no disputaron 38 partidos."
        )

    # 3. Verificar resultados de los partidos
    resultado_esperado = pd.Series(
        "D",
        index=df.index
    )

    resultado_esperado.loc[
        df["FTHG"] > df["FTAG"]
    ] = "H"

    resultado_esperado.loc[
        df["FTHG"] < df["FTAG"]
    ] = "A"

    resultados_incorrectos = (
        df["FTR"] != resultado_esperado
    ).sum()

    print(
        f"\nResultados inconsistentes: {resultados_incorrectos}"
    )

    if resultados_incorrectos > 0:
        errores.append(
            "Existen resultados que no coinciden con los goles."
        )

    # 4. Verificar goles negativos
    goles_negativos = (
        (df["FTHG"] < 0) |
        (df["FTAG"] < 0)
    ).sum()

    print(f"Goles negativos encontrados: {goles_negativos}")

    if goles_negativos > 0:
        errores.append(
            "Existen partidos con goles negativos."
        )

    # 5. Verificar encuentros duplicados
    partidos_duplicados = df.duplicated(
        subset=["Date", "HomeTeam", "AwayTeam"]
    ).sum()

    print(f"Encuentros duplicados: {partidos_duplicados}")

    if partidos_duplicados > 0:
        errores.append(
            "Existen encuentros repetidos."
        )

    # Resultado final
    if errores:
        print("\n=== ERRORES DETECTADOS ===")

        for error in errores:
            print(f"- {error}")

        raise ValueError(
            "El dataset no superó todas las validaciones."
        )

    print("\n=== VALIDACIÓN COMPLETADA ===")
    print("Todas las comprobaciones fueron superadas.")