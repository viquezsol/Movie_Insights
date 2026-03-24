import pandas as pd
import ast
import os

class ProcesadorEDA:
    def __init__(self, df):
        self.df = df

    def limpiar_datos(self):


        columnas_irrelevantes = ['Unnamed: 0', 'backdrop_path', 'poster_path']
        self.df = self.df.drop(columns=columnas_irrelevantes, errors='ignore')


        self.df['release_date'] = pd.to_datetime(self.df['release_date'], errors='coerce')


        self.df['year'] = self.df['release_date'].dt.year


        self.df['overview'] = self.df['overview'].fillna('Sin descripción')


        columnas_numericas = ['popularity', 'vote_average', 'vote_count']
        for col in columnas_numericas:
            if col in self.df.columns:
                self.df[col] = self.df[col].fillna(0)


        self.df = self.df.dropna(subset=['release_date'])


        if 'genre_ids' in self.df.columns:
            self.df['genre_ids'] = self.df['genre_ids'].apply(
                lambda x: ast.literal_eval(x) if isinstance(x, str) else x
            )


        self.df = self.df.drop_duplicates(subset='id')


        if 'popularity' in self.df.columns:
            limite = self.df['popularity'].quantile(0.99)
            self.df = self.df[self.df['popularity'] < limite]

        return self.df

    def resumen_descriptivo(self):
        return self.df.describe()

    def matriz_correlacion(self):
        columnas = ['popularity', 'vote_average', 'vote_count']
        return self.df[columnas].corr()

    def guardar_csv(self, ruta="data/processed/tmdb_movies_clean.csv"):
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        self.df.to_csv(ruta, index=False)