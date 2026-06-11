#PÁGINA DE SISTEMA DE RECOMENDACIÓN :P
import streamlit as st
import pandas as pd
import plotly.express as px

from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity


st.set_page_config(
    page_title="Sistema de Recomendación",
    layout="wide"
)


def cargar_css():
    with open("assets/styles/analisis.css", "r", encoding="utf-8") as archivo:
        st.markdown(f"<style>{archivo.read()}</style>", unsafe_allow_html=True)


cargar_css()


df = pd.read_csv("data/dataset.csv")

if "Unnamed: 0" in df.columns:
    df = df.drop(columns=["Unnamed: 0"])


st.markdown("""
<section class="module-hero">

<div class="module-left">

<h1>Sistema de Recomendación</h1>

<p class="subtitle">
Sistema inteligente que recomienda canciones similares a partir de características
musicales como energía, ritmo, acústica, tempo y popularidad
</p>

</div>

<div class="module-icon">
<i class="fa-solid fa-headphones"></i>
</div>

</section>
""", unsafe_allow_html=True)


st.markdown("""
<div class="section-box">
<h2>Recomendador musical</h2>

</div>
""", unsafe_allow_html=True)


columnas_necesarias = [
    "track_name",
    "artists",
    "track_genre",
    "popularity",
    "danceability",
    "energy",
    "valence",
    "tempo",
    "acousticness",
    "instrumentalness",
    "liveness",
    "speechiness"
]

df_rec = df[columnas_necesarias].dropna().copy()

df_rec["cancion_artista"] = (
    df_rec["track_name"].astype(str)
    + " - "
    + df_rec["artists"].astype(str)
)

df_rec = df_rec.drop_duplicates(subset=["cancion_artista"]).reset_index(drop=True)


features = [
    "popularity",
    "danceability",
    "energy",
    "valence",
    "tempo",
    "acousticness",
    "instrumentalness",
    "liveness",
    "speechiness"
]


col1, col2 = st.columns(2)

with col1:
    cancion_seleccionada = st.selectbox(
        "Selecciona una canción",
        df_rec["cancion_artista"].sort_values().tolist()
    )

with col2:
    cantidad = st.slider(
        "Cantidad de recomendaciones",
        min_value=3,
        max_value=15,
        value=5
    )


st.markdown("""
<div class="analysis-grid">

<div class="analysis-card">
<h4>Variables utilizadas</h4>
<ul>
<li><strong>popularidad:</strong> nivel de aceptación de la canción</li>
<li><strong>danceability:</strong> facilidad para bailar la canción</li>
<li><strong>energy:</strong> intensidad y actividad percibida</li>
<li><strong>valence:</strong> positividad musical</li>
<li><strong>tempo:</strong> velocidad de la canción</li>
</ul>
</div>

<div class="analysis-card">
<h4>Proceso realizado</h4>
<ol>
<li>Seleccionar una canción base</li>
<li>Tomar sus características musicales</li>
<li>Normalizar los valores numéricos</li>
<li>Calcular similitud del coseno</li>
<li>Mostrar las canciones más parecidas</li>
</ol>
</div>

</div>
""", unsafe_allow_html=True)


if st.button("Generar recomendaciones"):

    indice = df_rec[df_rec["cancion_artista"] == cancion_seleccionada].index[0]

    scaler = StandardScaler()
    matriz_features = scaler.fit_transform(df_rec[features])

    similitudes = cosine_similarity(
        [matriz_features[indice]],
        matriz_features
    )[0]

    df_rec["similitud"] = similitudes

    recomendaciones = (
        df_rec
        .drop(index=indice)
        .sort_values(by="similitud", ascending=False)
        .head(cantidad)
    )

    cancion_base = df_rec.loc[indice]

    st.markdown(f"""
<div class="hypothesis-card">
<div class="hypothesis-card-header">
<div class="hypothesis-number">R</div>
<div>
<h3>Canción seleccionada</h3>
<p>
<strong>{cancion_base["track_name"]}</strong> — {cancion_base["artists"]}<br>
Género: {cancion_base["track_genre"]} | Popularidad: {cancion_base["popularity"]}
</p>
</div>
</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="chart-title">
<h4>Canciones recomendadas</h4>
<p>
Estas canciones presentan mayor similitud con la canción seleccionada
</p>
</div>
""", unsafe_allow_html=True)

    tabla = recomendaciones[
        [
            "track_name",
            "artists",
            "track_genre",
            "popularity",
            "danceability",
            "energy",
            "valence",
            "tempo",
            "similitud"
        ]
    ].copy()

    tabla.columns = [
        "Canción",
        "Artista",
        "Género",
        "Popularidad",
        "Danceability",
        "Energy",
        "Valence",
        "Tempo",
        "Similitud"
    ]

    tabla["Similitud"] = tabla["Similitud"].round(3)

    st.dataframe(
        tabla,
        use_container_width=True
    )

    fig = px.bar(
        tabla,
        x="Similitud",
        y="Canción",
        orientation="h",
        title="Nivel de similitud de canciones recomendadas",
        template="plotly_dark",
        text="Similitud"
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15,23,42,0.65)",
        font=dict(color="#f8fafc"),
        title_font=dict(size=22),
        xaxis_title="Similitud",
        yaxis_title="Canción",
        yaxis=dict(categoryorder="total ascending")
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
<div class="final-conclusion">
<h4>Conclusión del sistema</h4>
<p>
El sistema recomienda canciones similares comparando características musicales
numéricas. Mientras más alto sea el valor de similitud, mayor parecido existe
entre la canción seleccionada y la recomendación generada
</p>
</div>
""", unsafe_allow_html=True)
    
#footer
st.markdown("""
<footer class="footer">
    <span>© 2026 Olga Vanessa Sorto Fuentes — Todos los derechos reservados</span>
</footer>
""", unsafe_allow_html=True)