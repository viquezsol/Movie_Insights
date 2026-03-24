"""
Dashboard de Películas
Ejecutar: streamlit run dashboard/app.py
"""

import streamlit as st
import sys
from pathlib import Path
import plotly.express as px

sys.path.append(str(Path(__file__).parent.parent))
from src.helpers.carga_datos import CargadorDatos
from src.eda.EDA import ProcesadorEDA


st.set_page_config(
    page_title="Movie Insights",
    page_icon="🎬",
    layout="wide"
)


st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #F0F2F6, #E6ECF5);
}

/* Títulos */
h1, h2, h3 {
    color: #111827;
    font-weight: 600;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #0F172A;
}

/* Texto del sidebar */
[data-testid="stSidebar"] * {
    color: white;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border-radius: 10px;
}

/* Botones */
.stButton > button {
    background-color: #6C63FF;
    color: white;
    border-radius: 8px;
    border: none;
    padding: 0.4rem 1rem;
}

.stButton > button:hover {
    background-color: #5548c8;
}
</style>
""", unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.title("🎬 Movie Insights")
    st.title(" Analisis de Películas")
    st.markdown("### Realizado por Marisol Víquez y Camila Jimenez")

    st.markdown("---")
    st.markdown("### 🎛️ Filtros")


@st.cache_data
def cargar_datos():
    ruta = Path(__file__).resolve().parent.parent / "data" / "raw" / "tmdb_2020_to_2025.csv"

    cargador = CargadorDatos(str(ruta))
    df = cargador.cargar()

    eda = ProcesadorEDA(df)
    df = eda.limpiar_datos()

    return df

df = cargar_datos()


if 'year' not in df.columns:
    st.error("La columna 'year' no existe en el dataset")
    st.stop()


anio = st.sidebar.slider(
    "Año",
    int(df['year'].min()),
    int(df['year'].max()),
    int(df['year'].max())
)

df_filtrado = df[df['year'] == anio]


st.title("🎬 Dashboard de Películas")
st.markdown("Análisis exploratorio interactivo del dataset")

# TABS
tab1, tab2, tab3 = st.tabs(["📊 General", "📈 Popularidad", "📊 Correlaciones"])

# TAB 1
with tab1:
    st.subheader("📊 Dataset filtrado")
    st.dataframe(df_filtrado.head(50))

    st.markdown("### 🎬 Películas por año")
    peliculas_por_anio = df.groupby('year').size().reset_index(name='count')

    fig = px.line(
        peliculas_por_anio,
        x='year',
        y='count',
        title="Cantidad de películas por año"
    )
    st.plotly_chart(fig, use_container_width=True)

# TAB 2
with tab2:
    st.subheader("🔥 Popularidad")

    if not df_filtrado.empty:
        fig = px.histogram(
            df_filtrado,
            x="popularity",
            nbins=30,
            title="Distribución de Popularidad"
        )
        st.plotly_chart(fig, use_container_width=True)

        fig2 = px.scatter(
            df_filtrado,
            x="vote_count",
            y="popularity",
            title="Relación entre votos y popularidad"
        )
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("No hay datos para el año seleccionado")

# TAB 3
with tab3:
    st.subheader("📊 Correlación")

    columnas_corr = ['popularity', 'vote_average', 'vote_count']

    if all(col in df.columns for col in columnas_corr):
        corr = df[columnas_corr].corr()

        fig = px.imshow(
            corr,
            text_auto=True,
            title="Matriz de correlación"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No hay suficientes columnas para la correlación")


st.markdown("---")
st.markdown("© 2026 Movie Insights - Proyecto Big Data")