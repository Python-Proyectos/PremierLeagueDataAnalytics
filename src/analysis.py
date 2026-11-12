import pandas as pd


def calcular_clasificacion(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula la clasificación de la Premier League a partir
    de los resultados de los partidos.

    Parámetros:
        df: DataFrame con los partidos de la temporada.

    Retorna:
        DataFrame con la clasificación de los equipos.
    """

    columnas_requeridas = {
        "HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR"
    }

    faltantes = columnas_requeridas - set(df.columns)

    if faltantes:
        raise ValueError(
            f"Faltan columnas necesarias: {sorted(faltantes)}"
        )

    equipos = sorted(
        set(df["HomeTeam"]) | set(df["AwayTeam"])
    )

    estadisticas = {
        equipo: {
            "Equipo": equipo,
            "PJ": 0,
            "PG": 0,
            "PE": 0,
            "PP": 0,
            "GF": 0,
            "GC": 0,
            "DG": 0,
            "PTS": 0
        }
        for equipo in equipos
    }

    for partido in df.itertuples(index=False):
        local = partido.HomeTeam
        visitante = partido.AwayTeam

        goles_local = int(partido.FTHG)
        goles_visitante = int(partido.FTAG)

        estadisticas[local]["PJ"] += 1
        estadisticas[visitante]["PJ"] += 1

        estadisticas[local]["GF"] += goles_local
        estadisticas[local]["GC"] += goles_visitante

        estadisticas[visitante]["GF"] += goles_visitante
        estadisticas[visitante]["GC"] += goles_local

        if goles_local > goles_visitante:
            estadisticas[local]["PG"] += 1
            estadisticas[local]["PTS"] += 3
            estadisticas[visitante]["PP"] += 1

        elif goles_local < goles_visitante:
            estadisticas[visitante]["PG"] += 1
            estadisticas[visitante]["PTS"] += 3
            estadisticas[local]["PP"] += 1

        else:
            estadisticas[local]["PE"] += 1
            estadisticas[visitante]["PE"] += 1

            estadisticas[local]["PTS"] += 1
            estadisticas[visitante]["PTS"] += 1

    for equipo in equipos:
        estadisticas[equipo]["DG"] = (
            estadisticas[equipo]["GF"]
            - estadisticas[equipo]["GC"]
        )

    clasificacion = pd.DataFrame(
        estadisticas.values()
    )

    clasificacion = clasificacion.sort_values(
        by=["PTS", "DG", "GF", "Equipo"],
        ascending=[False, False, False, True]
    ).reset_index(drop=True)

    clasificacion.insert(
        0,
        "Posicion",
        range(1, len(clasificacion) + 1)
    )

    return clasificacion