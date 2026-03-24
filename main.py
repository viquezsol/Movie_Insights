from src.helpers.carga_datos import CargadorDatos

def main():
    cargador = CargadorDatos("data/raw/tmdb_2020_to_2025.csv")
    df = cargador.cargar()

    if df is not None:
        print("\nPrimeras 5 filas:")
        print(df.head())

        print("\nInformación de carga:")
        print(cargador.obtener_info_carga())

if __name__ == "__main__":
    main()

    from src.helpers.carga_datos import CargadorDatos
    from src.eda.EDA import ProcesadorEDA


    def main():
        cargador = CargadorDatos("data/raw/tmdb_2020_to_2025.csv")
        df = cargador.cargar()

        eda = ProcesadorEDA(df)
        df_limpio = eda.limpiar_datos()

        eda.guardar_csv()

        print("Dataset limpio guardado correctamente")


    if __name__ == "__main__":
        main()