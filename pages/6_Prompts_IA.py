# PAGINA DE PROMPTS IA :l

#importaciónd e librerías
from typing import Optional
import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="Prompts IA", layout="wide",initial_sidebar_state="collapsed")

def cargar_css():
    with open("assets/styles/analisis.css", "r", encoding="utf-8") as archivo:
        st.markdown(f"<style>{archivo.read()}</style>", unsafe_allow_html=True)

cargar_css()

df = pd.read_csv("data/dataset.csv")

if "Unnamed: 0" in df.columns:
    df = df.drop(columns=["Unnamed: 0"])

def limpiar_texto(texto: str) -> str:
    texto = texto.lower().strip()
    reemplazos = {"á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u", "ñ": "n"}
    for original, reemplazo in reemplazos.items():
        texto = texto.replace(original, reemplazo)
    return texto

def encontrar_columna(texto: str, columnas: list) -> Optional[str]:
    texto = limpiar_texto(texto)

    for columna in columnas:
        nombre = limpiar_texto(columna)
        if nombre in texto:
            return columna

    return None

def responder_prompt(pregunta: str) -> str:
    pregunta_limpia = limpiar_texto(pregunta)
    columnas = df.columns.tolist()
    columnas_numericas = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
    columnas_categoricas = df.select_dtypes(include=["object", "category", "bool"]).columns.tolist()

    if "dataset cargado" in pregunta_limpia or "que dataset" in pregunta_limpia:
        return (
            "El dataset cargado corresponde a información musical de canciones. "
            "Incluye variables como nombre de la canción, artista, género, popularidad, energía, "
            "bailabilidad, tempo, duración y otras características de audio."
        )

    if "descripcion" in pregunta_limpia or "describe" in pregunta_limpia:
        return (
            f"El dataset contiene {df.shape[0]} filas y {df.shape[1]} columnas. "
            f"Posee {len(columnas_numericas)} campos numéricos y {len(columnas_categoricas)} campos categóricos. "
            "Permite realizar análisis exploratorio, visualización de datos, predicciones y recomendaciones musicales."
        )

    if "problematica" in pregunta_limpia or "predecir" in pregunta_limpia:
        return (
            "Con este dataset se pueden analizar o predecir problemáticas como: "
            "qué características influyen en la popularidad de una canción, "
            "qué géneros musicales tienen mejor aceptación, "
            "qué canciones podrían recomendarse según su energía o bailabilidad, "
            "y cómo variables como tempo, duración o valencia se relacionan con la popularidad."
        )

    if "columna" in pregunta_limpia:
        return f"El dataset tiene {df.shape[1]} columnas."

    if any(pal in pregunta_limpia for pal in ["fila", "filas", "registro", "registros"]):
        return f"El dataset tiene {df.shape[0]} filas."

    if "campos numericos" in pregunta_limpia or "variables numericas" in pregunta_limpia:
        return f"El dataset tiene {len(columnas_numericas)} campos numéricos: {', '.join(columnas_numericas[:10])}."

    if "campos categoricos" in pregunta_limpia or "variables categoricas" in pregunta_limpia:
        return f"El dataset tiene {len(columnas_categoricas)} campos categóricos: {', '.join(columnas_categoricas[:10])}."

    if any(pal in pregunta_limpia for pal in ["nulo", "nulos", "vacio", "vacios"]):
        return f"El dataset tiene {int(df.isnull().sum().sum())} valores nulos."

    if any(pal in pregunta_limpia for pal in ["duplicado", "duplicados"]):
        return f"El dataset tiene {int(df.duplicated().sum())} registros duplicados."

    if "popularidad promedio" in pregunta_limpia:
        if "popularity" in columnas:
            return f"La popularidad promedio de las canciones es {round(df['popularity'].mean(), 3)}."
        return "No encontré la columna popularity en el dataset."

    if "duracion promedio" in pregunta_limpia:
        if "duration_ms" in columnas:
            minutos = df["duration_ms"].mean() / 60000
            return f"La duración promedio de las canciones es de aproximadamente {round(minutos, 2)} minutos."
        return "No encontré la columna duration_ms en el dataset."

    if "genero mas frecuente" in pregunta_limpia or "genero mas comun" in pregunta_limpia:
        if "track_genre" in columnas:
            genero = df["track_genre"].mode()
            if not genero.empty:
                return f"El género musical más frecuente en el dataset es {genero.iloc[0]}."
        return "No encontré la columna track_genre en el dataset."

    if "cancion mas popular" in pregunta_limpia:
        if "track_name" in columnas and "popularity" in columnas:
            fila = df.loc[df["popularity"].idxmax()]
            return f"La canción más popular es {fila['track_name']} con una popularidad de {fila['popularity']}."
        return "No encontré las columnas necesarias para identificar la canción más popular."

    if "artista mas frecuente" in pregunta_limpia or "artista mas comun" in pregunta_limpia:
        if "artists" in columnas:
            artista = df["artists"].mode()
            if not artista.empty:
                return f"El artista más frecuente en el dataset es {artista.iloc[0]}."
        return "No encontré la columna artists en el dataset."

    if any(pal in pregunta_limpia for pal in ["media", "promedio"]):
        columna = encontrar_columna(pregunta_limpia, columnas)
        if columna and pd.api.types.is_numeric_dtype(df[columna]):
            return f"La media del campo {columna} es {round(df[columna].mean(), 3)}."
        return "No encontré un campo numérico válido para calcular la media."

    if any(pal in pregunta_limpia for pal in ["mayor", "maximo", "maxima"]):
        columna = encontrar_columna(pregunta_limpia, columnas)
        if columna and pd.api.types.is_numeric_dtype(df[columna]):
            return f"El mayor valor del campo {columna} es {round(df[columna].max(), 3)}."
        return "No encontré un campo numérico válido para calcular el mayor valor."

    if any(pal in pregunta_limpia for pal in ["menor", "minimo", "minima"]):
        columna = encontrar_columna(pregunta_limpia, columnas)
        if columna and pd.api.types.is_numeric_dtype(df[columna]):
            return f"El menor valor del campo {columna} es {round(df[columna].min(), 3)}."
        return "No encontré un campo numérico válido para calcular el menor valor."

    if any(pal in pregunta_limpia for pal in ["frecuente", "comun", "moda"]):
        columna = encontrar_columna(pregunta_limpia, columnas)
        if columna:
            moda = df[columna].mode()
            if not moda.empty:
                return f"El valor más frecuente del campo {columna} es {moda.iloc[0]}."
        return "No pude identificar el campo para calcular la frecuencia."

    return """No entendí bien la pregunta. Puedes probar con:
- ¿Qué dataset tiene cargado?
- Dame una descripción del dataset
- ¿Qué problemáticas podría predecir este dataset?
- ¿Cuántas filas tiene el dataset?
- ¿Cuántas columnas tiene el dataset?
- ¿Cuántos valores nulos tiene el dataset?
- ¿Cuáles son los campos numéricos?
- ¿Cuáles son los campos categóricos?
- ¿Cuál es la canción más popular?
- ¿Cuál es el género más frecuente?
- ¿Quién es el artista más común?
"""

st.markdown("""
<section class="module-hero">
    <div class="module-left">
        <h1>Prompts IA</h1>
        <p class="subtitle">
            Escribe preguntas sobre el dataset como si estuvieras conversando con una IA
        </p>
    </div>
    <div class="module-icon">
        <i class="fa-solid fa-robot"></i>
    </div>
</section>
""", unsafe_allow_html=True)


with st.container():
    st.markdown('<div class="main-chat">', unsafe_allow_html=True)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {
                "role": "assistant",
                "content": "Hola, soy tu asistente IA. Pregúntame algo sobre el dataset :D"
            }
        ]

    st.markdown('<p class="suggested-title">Sugerencias rápidas</p>', unsafe_allow_html=True)

    pregunta_sugerida = None

    if st.button("¿Qué dataset tienes cargado?"):
     pregunta_sugerida = "¿Qué dataset tienes cargado?"

    if st.button("¿Qué problemáticas podría predecir este dataset?"):
        pregunta_sugerida = "¿Qué problemáticas podría predecir este dataset?"
    
    if st.button("¿Quién es el artista más común?"):
        pregunta_sugerida = "¿Quién es el artista más común?"


    for mensaje in st.session_state.chat_history:
        with st.chat_message(mensaje["role"]):
            st.markdown(mensaje["content"])

    pregunta = st.chat_input("Escribe tu pregunta...")

    if pregunta_sugerida:
        pregunta = pregunta_sugerida

    if pregunta:
        st.session_state.chat_history.append({"role": "user", "content": pregunta})
        respuesta = responder_prompt(pregunta)
        st.session_state.chat_history.append({"role": "assistant", "content": respuesta})
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<footer class="footer">
    <span>© 2026 Olga Vanessa Sorto Fuentes — Todos los derechos reservados</span>
</footer>
""", unsafe_allow_html=True)