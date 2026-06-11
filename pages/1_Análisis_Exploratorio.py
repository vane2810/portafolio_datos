# PÁGINA DE ANÁLISIS EXPLORATORIO :C

#importación de librerías
import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="Análisis Exploratorio",
    layout="wide"
)

#carga archivo css
def cargar_css():
    with open("assets/styles/analisis.css", "r", encoding="utf-8") as archivo:
        st.markdown(f"<style>{archivo.read()}</style>", unsafe_allow_html=True)
cargar_css()

# aislar estilos personalizados 
st.markdown("""<div class='site-root'>""", unsafe_allow_html=True)

#header de la pagina - info principal
st.markdown("""
<section class="module-hero">
<div class="module-left">
<h1>Análisis Exploratorio</h1>
<p class="subtitle">
    Exploración, descripción y visualización de datos para descubrir patrones, tendencias y relaciones en el dataset.
</p>
</div>
<div class="module-icon">
<i class="fa-solid fa-magnifying-glass-chart"></i>
</div>
</section>
""", unsafe_allow_html=True)


# submenu 
submenu = st.tabs([
    "Descripción del dataset",
    "Descripción de campos",
    "Navegador del dataset",
    "Buscador de registros",
    "Graficador exploratorio",
    "Hipótesis"
])

df = pd.read_csv("data/dataset.csv")

if "Unnamed: 0" in df.columns:
    df = df.drop(columns=["Unnamed: 0"])

# tab 1 - descripción del dataset
with submenu[0]:

    st.markdown("""
<div class="section-box">
<h2>Descripción del dataset</h2>
<p>
El dataset contiene información de canciones de Spotify, incluyendo artistas,
álbumes, géneros musicales, popularidad y características de audio.
</p>
</div>
""", unsafe_allow_html=True)

    total_filas = df.shape[0]
    total_columnas = df.shape[1]
    total_nulos = df.isnull().sum().sum()
    total_duplicados = df.duplicated().sum()

    columnas_numericas = df.select_dtypes(include=["int64", "float64"]).columns
    columnas_categoricas = df.select_dtypes(include=["object", "bool"]).columns

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Filas", total_filas)
    col2.metric("Columnas", total_columnas)
    col3.metric("Valores nulos", total_nulos)
    col4.metric("Duplicados", total_duplicados)

    col5, col6, col7 = st.columns(3)

    col5.metric("Campos numéricos", len(columnas_numericas))
    col6.metric("Campos categóricos", len(columnas_categoricas))
    col7.metric("Géneros musicales", df["track_genre"].nunique())

    st.markdown("### Vista previa del dataset")
    st.dataframe(df.head(10), use_container_width=True)

    st.markdown("### Resumen de columnas")

    resumen_columnas = pd.DataFrame({
        "Campo": df.columns,
        "Tipo de dato": df.dtypes.astype(str),
        "Valores nulos": df.isnull().sum().values,
        "Valores únicos": df.nunique().values
    })

    st.dataframe(resumen_columnas, use_container_width=True)

# tab 2 - descripción de campos
with submenu[1]:

    st.markdown("""
<div class="section-box">
<h2>Descripción de campos</h2>
</div>
""", unsafe_allow_html=True)

    campo = st.selectbox(
        "Selecciona un campo para conocer su tipo de dato, cantidad de valores, valores nulos y su comportamiento general",
        df.columns
    )

    tipo_dato = str(df[campo].dtype)
    valores_unicos = df[campo].nunique()
    valores_nulos = df[campo].isnull().sum()

    col1, col2, col3 = st.columns(3)

    col1.metric("Tipo de dato", tipo_dato)
    col2.metric("Valores únicos", valores_unicos)
    col3.metric("Valores nulos", valores_nulos)

    st.markdown(f"### Descripción del campo: `{campo}`")

    if pd.api.types.is_numeric_dtype(df[campo]):

        st.markdown("""
        Este campo es <strong>CUANTITATIVO</strong>, por lo tanto se muestran sus principales
        medidas estadísticas.
        """, unsafe_allow_html=True)

        descripcion = df[campo].describe().reset_index()
        descripcion.columns = ["Medida", "Valor"]

        st.dataframe(
            descripcion,
            use_container_width=True
        )

    else:

        st.markdown("""
        Este campo es <strong>CATEGÓRICO</strong>, por lo tanto se muestran los valores posibles
        encontrados en el dataset.
        """, unsafe_allow_html=True)

        valores = df[campo].value_counts().reset_index()
        valores.columns = ["Valor", "Frecuencia"]

        st.dataframe(
            valores,
            use_container_width=True
        )

# tab 3 - navegador del dataset completo
with submenu[2]:

    st.markdown("""
<div class="section-box">
<h2>Navegador del dataset completo</h2>
</div>
""", unsafe_allow_html=True)

    columnas_seleccionadas = st.multiselect(
        "Selecciona las columnas que deseas visualizar",
        df.columns.tolist(),
        default=df.columns.tolist()
    )

    opciones_filas = {
        "10 filas": 10,
        "25 filas": 25,
        "50 filas": 50,
        "100 filas": 100,
        "500 filas": 500,
        "1000 filas": 1000,
        "10000 filas": 10000,
        "Todo el dataset": len(df)
    }

    seleccion_filas = st.selectbox(
        "Cantidad de registros a visualizar",
        list(opciones_filas.keys()),
        index=2
    )

    cantidad_filas = opciones_filas[seleccion_filas]

    if columnas_seleccionadas:

        st.markdown(f"""
<div class="field-title">
<h3>Vista del dataset</h3>
<p>
Mostrando <strong>{cantidad_filas}</strong> registros y
<strong>{len(columnas_seleccionadas)}</strong> columnas seleccionadas
</p>
</div>
""", unsafe_allow_html=True)

        st.dataframe(
            df[columnas_seleccionadas].head(cantidad_filas),
            use_container_width=True,
            height=500
        )

    else:

        st.warning(
            "Selecciona al menos una columna para visualizar el dataset."
        )


# tab 4 - buscador de registros por código
with submenu[3]:

    st.markdown("""
<div class="section-box">
<h2>Buscador de registros</h2>
</div>
""", unsafe_allow_html=True)

    codigo = st.text_input(
        "Busca una canción dentro del dataset utilizando su código único del campo track_id",
        placeholder="Ejemplo: 5SuOikwiRyPMVoIQDJUgSV"
    )

    if codigo:

        resultado = df[
            df["track_id"].astype(str).str.contains(
                codigo,
                case=False,
                na=False
            )
        ]

        if not resultado.empty:

            st.success(f"Registros encontrados: {len(resultado)}")

            st.dataframe(
                resultado,
                use_container_width=True
            )

        else:

            st.warning("No se encontraron registros con ese código.")

    else:

        st.info("Escribe un código para realizar la búsqueda.")

# tab 5 - graficador exploratorio
with submenu[4]:

    st.markdown("""
<div class="section-box">
<h2>Graficador exploratorio</h2>
</div>
""", unsafe_allow_html=True)

    campo_grafico = st.selectbox(
        "Selecciona un campo del dataset y la aplicación generará automáticamente el gráfico más adecuado según el tipo de dato",
        df.columns,
        key="campo_grafico"
    )

    st.markdown(f"""
<div class="field-title">
<h3>Gráfico generado para: <span>{campo_grafico}</span></h3>
</div>
""", unsafe_allow_html=True)

    # Campos numéricos
    if pd.api.types.is_numeric_dtype(df[campo_grafico]) and not pd.api.types.is_bool_dtype(df[campo_grafico]):

        fig = px.histogram(
            df,
            x=campo_grafico,
            nbins=40,
            title=f"Distribución de {campo_grafico}",
            template="plotly_dark",
            marginal="box"
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15,23,42,0.65)",
            font=dict(color="#f8fafc"),
            title_font=dict(size=22),
            bargap=0.05
        )

        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""
<div class="final-conclusion">
<strong>Interpretación:</strong> Este gráfico permite observar la distribución
del campo seleccionado, identificar concentraciones de datos, valores frecuentes
y posibles valores atípicos.
</div>
""", unsafe_allow_html=True)

    # Campos categóricos o booleanos
    else:

        conteo = (
            df[campo_grafico]
            .value_counts()
            .head(15)
            .reset_index()
        )

        conteo.columns = [campo_grafico, "Frecuencia"]

        fig = px.bar(
            conteo,
            x="Frecuencia",
            y=campo_grafico,
            orientation="h",
            title=f"Valores más frecuentes de {campo_grafico}",
            template="plotly_dark",
            text="Frecuencia"
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15,23,42,0.65)",
            font=dict(color="#f8fafc"),
            title_font=dict(size=22),
            yaxis=dict(categoryorder="total ascending")
        )

        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""
<div class="final-conclusion">
<strong>Interpretación:</strong> Este gráfico muestra los valores más repetidos
del campo seleccionado, permitiendo identificar categorías predominantes dentro
del dataset
</div>
""", unsafe_allow_html=True)

# tab 6 - hipótesis
with submenu[5]:

    st.markdown("""
<div class="section-box">
<h2>Hipótesis</h2>
<p>
Validación de hipótesis mediante variables del dataset, proceso de análisis,
visualización gráfica y conclusión final
</p>
</div>
""", unsafe_allow_html=True)

    hipotesis_menu = st.tabs([
        "Hipótesis 1",
        "Hipótesis 2"
    ])

    # HIPÓTESIS 1
    with hipotesis_menu[0]:

        st.markdown("""
<div class="hypothesis-card">
<div class="hypothesis-card-header">
<div class="hypothesis-number">1</div>
<div>
<h3>Las canciones con mayor energía tienden a tener mayor popularidad</h3>
<p>
Se analiza si el nivel de energía de una canción tiene relación con su popularidad promedio
</p>
</div>
</div>
</div>
""", unsafe_allow_html=True)

        st.markdown("""
<div class="analysis-grid">

<div class="analysis-card">
<h4>Variables utilizadas</h4>
<ul>
<li><strong>energy:</strong> nivel de energía de la canción, representado entre 0 y 1</li>
<li><strong>popularity:</strong> nivel de popularidad de la canción en Spotify</li>
</ul>
</div>

<div class="analysis-card">
<h4>Proceso realizado</h4>
<ol>
<li>Seleccionar las variables <strong>energy</strong> y <strong>popularity</strong></li>
<li>Eliminar registros con valores vacíos en esas variables</li>
<li>Clasificar las canciones en energía baja, media y alta</li>
<li>Calcular la popularidad promedio de cada grupo</li>
<li>Comparar los resultados para validar la hipótesis</li>
</ol>
</div>

</div>
""", unsafe_allow_html=True)

        datos_h1 = df[["energy", "popularity"]].dropna().copy()

        datos_h1["grupo_energia"] = pd.cut(
            datos_h1["energy"],
            bins=[0, 0.33, 0.66, 1],
            labels=["Energía baja", "Energía media", "Energía alta"],
            include_lowest=True
        )

        resumen_h1 = (
            datos_h1
            .groupby("grupo_energia", observed=False)["popularity"]
            .mean()
            .reset_index()
        )

        st.markdown("""
<div class="chart-title">
<h4>Visualización del análisis</h4>
<p>
Comparación de la popularidad promedio según el nivel de energía de las canciones
</p>
</div>
""", unsafe_allow_html=True)

        fig = px.bar(
            resumen_h1,
            x="grupo_energia",
            y="popularity",
            title="Popularidad promedio según nivel de energía",
            template="plotly_dark",
            text_auto=".2f"
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15,23,42,0.65)",
            font=dict(color="#f8fafc"),
            title_font=dict(size=22),
            xaxis_title="Grupo de energía",
            yaxis_title="Popularidad promedio"
        )

        st.plotly_chart(fig, use_container_width=True)

        baja = resumen_h1.loc[
            resumen_h1["grupo_energia"] == "Energía baja",
            "popularity"
        ].values[0]

        media = resumen_h1.loc[
            resumen_h1["grupo_energia"] == "Energía media",
            "popularity"
        ].values[0]

        alta = resumen_h1.loc[
            resumen_h1["grupo_energia"] == "Energía alta",
            "popularity"
        ].values[0]

        col1, col2, col3 = st.columns(3)

        col1.metric("Energía baja", round(baja, 2))
        col2.metric("Energía media", round(media, 2))
        col3.metric("Energía alta", round(alta, 2))

        if alta > media > baja:
            conclusion = """
La hipótesis se valida, ya que los resultados muestran una tendencia creciente:
a mayor nivel de energía, mayor promedio de popularidad
"""
        elif alta > baja:
            conclusion = """
La hipótesis se valida parcialmente, porque las canciones con energía alta
presentan mayor popularidad promedio que las canciones con energía baja,
aunque la tendencia no es completamente uniforme
"""
        else:
            conclusion = """
La hipótesis no se valida, debido a que las canciones con mayor energía
no presentan un promedio de popularidad superior de forma clara
"""

        st.markdown(f"""
<div class="final-conclusion">
<h4>Conclusión del análisis</h4>
<p>{conclusion}</p>
</div>
""", unsafe_allow_html=True)

    # HIPÓTESIS 2
    with hipotesis_menu[1]:

        st.markdown("""
<div class="hypothesis-card">
<div class="hypothesis-card-header">
<div class="hypothesis-number">2</div>
<div>
<h3>Los géneros musicales presentan diferentes niveles promedio de popularidad</h3>
<p>
Se analiza si el género musical influye en el promedio de popularidad de las canciones
</p>
</div>
</div>
</div>
""", unsafe_allow_html=True)

        st.markdown("""
<div class="analysis-grid">

<div class="analysis-card">
<h4>Variables utilizadas</h4>
<ul>
<li><strong>track_genre:</strong> género musical al que pertenece la canción</li>
<li><strong>popularity:</strong> nivel de popularidad de la canción en Spotify</li>
</ul>
</div>

<div class="analysis-card">
<h4>Proceso realizado</h4>
<ol>
<li>Seleccionar las variables <strong>track_genre</strong> y <strong>popularity</strong></li>
<li>Eliminar registros con valores vacíos en esas variables</li>
<li>Agrupar las canciones por género musical</li>
<li>Calcular la popularidad promedio por género</li>
<li>Ordenar los géneros y comparar las diferencias obtenidas</li>
</ol>
</div>

</div>
""", unsafe_allow_html=True)

        datos_h2_limpios = df[["track_genre", "popularity"]].dropna().copy()

        datos_h2 = (
            datos_h2_limpios
            .groupby("track_genre")["popularity"]
            .mean()
            .sort_values(ascending=False)
            .head(15)
            .reset_index()
        )

        st.markdown("""
<div class="chart-title">
<h4>Visualización del análisis</h4>
<p>
Comparación de los 15 géneros musicales con mayor popularidad promedio
</p>
</div>
""", unsafe_allow_html=True)

        fig = px.bar(
            datos_h2,
            x="popularity",
            y="track_genre",
            orientation="h",
            title="Popularidad promedio por género musical",
            template="plotly_dark",
            text_auto=".2f"
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15,23,42,0.65)",
            font=dict(color="#f8fafc"),
            title_font=dict(size=22),
            xaxis_title="Popularidad promedio",
            yaxis_title="Género musical",
            yaxis=dict(categoryorder="total ascending")
        )

        st.plotly_chart(fig, use_container_width=True)

        mayor_promedio = datos_h2["popularity"].max()
        menor_promedio = datos_h2["popularity"].min()
        diferencia = mayor_promedio - menor_promedio
        genero_mayor = datos_h2.loc[
            datos_h2["popularity"].idxmax(),
            "track_genre"
        ]

        col1, col2, col3 = st.columns(3)

        col1.metric("Género con mayor promedio", genero_mayor)
        col2.metric("Mayor popularidad promedio", round(mayor_promedio, 2))
        col3.metric("Diferencia", round(diferencia, 2))

        if diferencia >= 10:
            conclusion = """
La hipótesis se valida, ya que existen diferencias claras entre los géneros
musicales analizados. Esto indica que el género puede influir en el nivel
promedio de popularidad
"""
        elif diferencia >= 5:
            conclusion = """
La hipótesis se valida parcialmente, porque existen diferencias moderadas
entre los géneros musicales, aunque no son extremadamente amplias
"""
        else:
            conclusion = """
La hipótesis no se valida con fuerza, ya que las diferencias entre los géneros
musicales son pequeñas
"""

        st.markdown(f"""
<div class="final-conclusion">
<h4>Conclusión del análisis</h4>
<p>{conclusion}</p>
</div>
""", unsafe_allow_html=True)
        
#footer
st.markdown("""
<footer class="footer">
    <span>© 2026 Olga Vanessa Sorto Fuentes — Todos los derechos reservados</span>
</footer>
""", unsafe_allow_html=True)