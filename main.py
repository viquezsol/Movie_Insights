from src.helpers.carga_datos import CargadorDatos

def main():
    cargador = CargadorDatos("tmdb_2020_to_2025.csv")
    df = cargador.cargar()
    if df is not None:
        print("\nPrimeras 5 filas:")
        print(df.head())
        print("\nInformación de carga:")
        print(cargador.obtener_info_carga())

if __name__ == "__main__":
    main()