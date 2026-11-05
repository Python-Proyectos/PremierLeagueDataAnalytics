from src.data_loader import cargar_datos
from src.data_cleaning import limpiar_datos
from src.data_validation import validar_datos

def main():

    print("=" * 50)
    print(" PREMIER LEAGUE DATA ANALYTICS")
    print(" Temporada 2018-2019")
    print("=" * 50)

    # Cargar el dataset
    df = cargar_datos()

    print("\nDataset cargado correctamente.")

    # Mostrar dimensiones
    print("\n=== DIMENSIONES DEL DATASET ===")
    print(f"Partidos: {df.shape[0]}")
    print(f"Columnas: {df.shape[1]}")

    # Mostrar primeros registros
    print("\n=== PRIMEROS 5 PARTIDOS ===")
    print(df.head().to_string(index=False))

    # Mostrar nombres de columnas
    print("\n=== COLUMNAS DISPONIBLES ===")
    print(df.columns.tolist())

    # Mostrar información general
    print("\n=== INFORMACIÓN GENERAL ===")
    df.info()

    # Mostrar valores faltantes
    print("\n=== VALORES NULOS ===")
    print(df.isnull().sum())

    # Limpiar y preparar el dataset
    df_limpio = limpiar_datos(df)

    print("\n=== PRIMEROS PARTIDOS LIMPIOS ===")

    print(
        df_limpio[
            ["Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR"]
        ].head().to_string(index=False)
    )

    # Validar integridad de los datos
    validar_datos(df_limpio)

if __name__ == "__main__":
    main()

