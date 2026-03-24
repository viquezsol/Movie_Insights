import pandas as pd
import os
from pathlib import Path


class CargadorDatos:
    def __init__(self, nombre_archivo, directorio_base=None):
        """
        nombre_archivo: nombre del archivo (ej. 'tmdb_2020_to_2025.csv')
        directorio_base: ruta base donde buscar. Si es None, se usa el directorio del proyecto.
        """
        self.nombre_archivo = nombre_archivo
        self.directorio_base = Path(directorio_base) if directorio_base else Path(__file__).parent.parent.parent
        self.df = None
        self.info_carga = {}

    def _buscar_archivo(self):
        """Busca el archivo en subcarpetas comunes y retorna la ruta completa o None."""
        posibles_rutas = [
            self.directorio_base / "data" / "raw" / self.nombre_archivo,
            self.directorio_base / "data raw" / self.nombre_archivo,
            self.directorio_base / "dataraw" / self.nombre_archivo,
            self.directorio_base / self.nombre_archivo,
        ]
        for ruta in posibles_rutas:
            if ruta.exists():
                return ruta
        return None

    def cargar(self):
        try:
            ruta = self._buscar_archivo()
            if not ruta:
                raise FileNotFoundError(f"No encuentro el archivo '{self.nombre_archivo}' en las rutas esperadas.")

            self.df = pd.read_csv(ruta)
            self.info_carga["num_filas"] = self.df.shape[0]
            self.info_carga["num_columnas"] = self.df.shape[1]
            null_pct = self.df.isnull().mean() * 100
            self.info_carga["porcentaje_nulos"] = null_pct.to_dict()

            print("Archivo cargado correctamente.")
            print(f"   Filas: {self.info_carga['num_filas']}")
            print(f"   Columnas: {self.info_carga['num_columnas']}")
            return self.df
        except Exception as e:
            print(f"Error: {e}")
            return None

    def obtener_info_carga(self):
        return self.info_carga