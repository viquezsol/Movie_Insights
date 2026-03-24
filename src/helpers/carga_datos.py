import pandas as pd
import os
from pathlib import Path

class CargadorDatos:
    def __init__(self, ruta):
        self.ruta = ruta
        self.df = None

    def cargar(self):
        import pandas as pd
        self.df = pd.read_csv(self.ruta)
        return self.df

    def obtener_info_carga(self):
        if self.df is not None:
            return {
                "filas": self.df.shape[0],
                "nulos (%)": (self.df.isnull().sum() / len(self.df) * 100).to_dict()
            }
