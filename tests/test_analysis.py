import pandas as pd
import pytest

from src.analysis import calcular_clasificacion


def test_victoria_otorga_tres_puntos():
    """
    Verifica que una victoria otorgue tres puntos
    y una derrota no otorgue ninguno.
    """

    partidos = pd.DataFrame([
        {
            "HomeTeam": "Equipo A",
            "AwayTeam": "Equipo B",
            "FTHG": 2,
            "FTAG": 1,
            "FTR": "H"
        }
    ])

    clasificacion = calcular_clasificacion(partidos)

    ganador = clasificacion[
        clasificacion["Equipo"] == "Equipo A"
    ].iloc[0]

    perdedor = clasificacion[
        clasificacion["Equipo"] == "Equipo B"
    ].iloc[0]

    assert ganador["PTS"] == 3
    assert ganador["PG"] == 1
    assert ganador["GF"] == 2
    assert ganador["GC"] == 1

    assert perdedor["PTS"] == 0
    assert perdedor["PP"] == 1



"""Test Empate otorga un punto"""
def test_empate_otorga_un_punto():
    """
    Comprueba que ambos equipos reciben un punto
    cuando el partido termina empatado.
    """

    partidos = pd.DataFrame([
        {
            "HomeTeam": "Equipo A",
            "AwayTeam": "Equipo B",
            "FTHG": 2,
            "FTAG": 2,
            "FTR": "D"
        }
    ])

    clasificacion = calcular_clasificacion(partidos)

    equipo_a = clasificacion[
        clasificacion["Equipo"] == "Equipo A"
    ].iloc[0]

    equipo_b = clasificacion[
        clasificacion["Equipo"] == "Equipo B"
    ].iloc[0]

    assert equipo_a["PTS"] == 1
    assert equipo_b["PTS"] == 1

    assert equipo_a["PE"] == 1
    assert equipo_b["PE"] == 1

    assert equipo_a["DG"] == 0
    assert equipo_b["DG"] == 0


def test_diferencia_de_goles():
    """
    Verifica que la diferencia de goles se calcule
    correctamente para ambos equipos.
    """

    partidos = pd.DataFrame([
        {
            "HomeTeam": "Equipo A",
            "AwayTeam": "Equipo B",
            "FTHG": 4,
            "FTAG": 1,
            "FTR": "H"
        }
    ])

    clasificacion = calcular_clasificacion(partidos)

    equipo_a = clasificacion[
        clasificacion["Equipo"] == "Equipo A"
    ].iloc[0]

    equipo_b = clasificacion[
        clasificacion["Equipo"] == "Equipo B"
    ].iloc[0]

    assert equipo_a["DG"] == 3
    assert equipo_b["DG"] == -3

    assert equipo_a["GF"] == 4
    assert equipo_a["GC"] == 1

    assert equipo_b["GF"] == 1
    assert equipo_b["GC"] == 4


def test_columnas_faltantes():
    """
    Comprueba que la función lance una excepción
    cuando faltan columnas obligatorias.
    """

    partidos = pd.DataFrame([
        {
            "HomeTeam": "Equipo A",
            "AwayTeam": "Equipo B"
        }
    ])

    with pytest.raises(ValueError, match="Faltan columnas necesarias"):
        calcular_clasificacion(partidos)



"""Test clasificacion con multiples partidos"""
def test_clasificacion_con_multiples_partidos():
    """
    Verifica la acumulación de puntos y estadísticas
    cuando se disputan varios encuentros.
    """

    partidos = pd.DataFrame([
        {
            "HomeTeam": "Equipo A",
            "AwayTeam": "Equipo B",
            "FTHG": 3,
            "FTAG": 1,
            "FTR": "H"
        },
        {
            "HomeTeam": "Equipo B",
            "AwayTeam": "Equipo C",
            "FTHG": 2,
            "FTAG": 2,
            "FTR": "D"
        },
        {
            "HomeTeam": "Equipo C",
            "AwayTeam": "Equipo A",
            "FTHG": 0,
            "FTAG": 2,
            "FTR": "A"
        }
    ])

    clasificacion = calcular_clasificacion(partidos)

    assert clasificacion["Equipo"].tolist() == [
        "Equipo A",
        "Equipo B",
        "Equipo C"
    ]

    equipo_a = clasificacion.iloc[0]
    equipo_b = clasificacion.iloc[1]
    equipo_c = clasificacion.iloc[2]

    assert equipo_a["PJ"] == 2
    assert equipo_a["PG"] == 2
    assert equipo_a["PTS"] == 6
    assert equipo_a["DG"] == 4

    assert equipo_b["PJ"] == 2
    assert equipo_b["PE"] == 1
    assert equipo_b["PP"] == 1
    assert equipo_b["PTS"] == 1

    assert equipo_c["PJ"] == 2
    assert equipo_c["PE"] == 1
    assert equipo_c["PP"] == 1
    assert equipo_c["PTS"] == 1