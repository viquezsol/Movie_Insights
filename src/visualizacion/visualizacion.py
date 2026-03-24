from src.helpers.carga_datos import CargadorDatos
from src.eda.EDA import ProcesadorEDA

cargador = CargadorDatos("../../data/raw/tmdb_2020_to_2025.csv")
df = cargador.cargar()

eda = ProcesadorEDA(df)
df_limpio = eda.limpiar_datos()