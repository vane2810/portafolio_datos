# PÁGINA DE CARGA DE ARCHIVOS
import io
import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="Carga de Archivos",
    layout="wide"
)


def cargar_css():
    with open("assets/styles/analisis.css", "r", encoding="utf-8") as archivo:
        st.markdown(f"<style>{archivo.read()}</style>", unsafe_allow_html=True)


def cargar_csv_con_progreso(archivo, progress_bar, status_text):
    archivo.seek(0)
    total_bytes = getattr(archivo, "size", None)

    if total_bytes is None:
        contenido = archivo.read()
        total_bytes = len(contenido)
        archivo_bytes = io.BytesIO(contenido)
    else:
        archivo_bytes = archivo

    dfs = []
    bytes_leidos = 0

    for chunk in pd.read_csv(
        archivo_bytes,
        chunksize=10000,
        encoding="utf-8",
        on_bad_lines="skip"
    ):
        dfs.append(chunk)
        bytes_leidos = archivo_bytes.tell()
        if total_bytes:
            progreso = min(int(bytes_leidos / total_bytes * 100), 99)
            progress_bar.progress(progreso)
            status_text.text(f"Leyendo CSV... {progreso}%")

    if dfs:
        df = pd.concat(dfs, ignore_index=True)
    else:
        df = pd.DataFrame()

    progress_bar.progress(100)
    status_text.text("Lectura de CSV completada")
    archivo.seek(0)
    return df


def cargar_excel_con_progreso(archivo, progress_bar, status_text):
    status_text.text("Leyendo archivo Excel...")
    progress_bar.progress(25)
    archivo.seek(0)

    if archivo.name.endswith(".xls"):
        df = pd.read_excel(archivo, engine="xlrd")
    else:
        df = pd.read_excel(archivo, engine="openpyxl")

    progress_bar.progress(80)
    status_text.text("Procesando datos de Excel...")
    progress_bar.progress(100)
    status_text.text("Lectura de Excel completada")
    archivo.seek(0)
    return df


cargar_css()


st.markdown("""
<section class="module-hero">

<div class="module-left">

<h1>Carga de Archivos</h1>

<p class="subtitle">
Carga archivos desde la computadora, visualiza sus datos
y genera gráficos exploratorios de forma automática
</p>

</div>

<div class="module-icon">
<i class="fa-solid fa-file-arrow-up"></i>
</div>

</section>
""", unsafe_allow_html=True)


st.markdown("""
<div class="section-box">
<h2>Análisis de datos por carga de archivos</h2>
</div>
""", unsafe_allow_html=True)


archivo = st.file_uploader(
    "Selecciona un archivo CSV o Excel",
    type=["csv", "xlsx", "xls"],
    accept_multiple_files=False
)


if archivo is not None:

    try:
        progress_bar = st.progress(0)
        status_text = st.empty()
        status_text.text("Iniciando carga del archivo...")

        if archivo.name.endswith(".csv"):
            df_cargado = cargar_csv_con_progreso(archivo, progress_bar, status_text)
        else:
            df_cargado = cargar_excel_con_progreso(archivo, progress_bar, status_text)

        st.success("Archivo cargado correctamente")
        status_text.empty()
        progress_bar.empty()
        st.markdown(f"""
<div class="chart-title">
<h4>Resumen del archivo cargado</h4>
<p>
El archivo <strong>{archivo.name}</strong> fue cargado correctamente y está listo
para el análisis exploratorio
</p>

</div>
""", unsafe_allow_html=True)

        filas = df_cargado.shape[0]
        columnas = df_cargado.shape[1]
        nulos = int(df_cargado.isnull().sum().sum())
        duplicados = int(df_cargado.duplicated().sum())

        columnas_numericas = df_cargado.select_dtypes(
            include=["int64", "float64"]
        ).columns.tolist()

        columnas_categoricas = df_cargado.select_dtypes(
            include=["object", "category", "bool"]
        ).columns.tolist()

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Filas", filas)
        col2.metric("Columnas", columnas)
        col3.metric("Valores nulos", nulos)
        col4.metric("Duplicados", duplicados)

        col5, col6 = st.columns(2)

        col5.metric("Campos numéricos", len(columnas_numericas))
        col6.metric("Campos categóricos", len(columnas_categoricas))

        st.markdown("""
<div class="chart-title">
<h4>Vista previa del archivo</h4>
<p>
Se muestran los primeros registros del archivo cargado
</p>
</div>
""", unsafe_allow_html=True)

        filas_max = max(min(len(df_cargado), 100), 1)
        cantidad = st.slider(
            "Cantidad de filas a visualizar",
            min_value=1,
            max_value=filas_max,
            value=min(50, filas_max),
            step=1
        )
        
        st.dataframe(
            df_cargado.head(cantidad),
            use_container_width=True
        )

        st.markdown("""
<div class="chart-title">
<h4>Resumen de columnas</h4>
<p>
Se muestra el tipo de dato, cantidad de valores nulos y valores únicos por columna
</p>
</div>
""", unsafe_allow_html=True)

        resumen_columnas = pd.DataFrame({
            "Campo": df_cargado.columns,
            "Tipo de dato": df_cargado.dtypes.astype(str),
            "Valores nulos": df_cargado.isnull().sum().values,
            "Valores únicos": df_cargado.nunique().values
        })

        st.dataframe(
            resumen_columnas,
            use_container_width=True
        )

        columnas_con_nulos = resumen_columnas[
            resumen_columnas["Valores nulos"] > 0
        ]

        if len(columnas_con_nulos) > 0:

            st.markdown("""

<div class="chart-title">
<h4>Generador de gráfico</h4>
<p>
Selecciona un campo para generar un gráfico exploratorio automático
</div>
""", unsafe_allow_html=True)

        campo = st.selectbox(
            "Selecciona el campo a graficar",
            df_cargado.columns
        )

        if campo in columnas_numericas:

            fig = px.histogram(
                df_cargado,
                x=campo,
                nbins=35,
                title=f"Distribución de {campo}",
                template="plotly_dark",
                marginal="box"
            )

            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(15,23,42,0.65)",
                font=dict(color="#f8fafc"),
                title_font=dict(size=22),
                xaxis_title=campo,
                yaxis_title="Frecuencia"
            )

            st.plotly_chart(fig, use_container_width=True)
            st.markdown(f"""
<div class="final-conclusion">
<h4>Análisis del gráfico</h4>
<p>
El gráfico se construyó utilizando la variable <strong>{campo}</strong>.
Al ser una variable numérica, se representa mediante un histograma para observar
la distribución de los datos, la frecuencia de los valores y posibles valores atípicos.
</p>
</div>
""", unsafe_allow_html=True)

        else:

            conteo = (
                df_cargado[campo]
                .value_counts()
                .head(15)
                .reset_index()
            )

            conteo.columns = [campo, "Frecuencia"]

            fig = px.bar(
                conteo,
                x="Frecuencia",
                y=campo,
                orientation="h",
                title=f"Valores más frecuentes de {campo}",
                template="plotly_dark",
                text="Frecuencia"
            )

            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(15,23,42,0.65)",
                font=dict(color="#f8fafc"),
                title_font=dict(size=22),
                xaxis_title="Frecuencia",
                yaxis_title=campo,
                yaxis=dict(categoryorder="total ascending")
            )

            st.plotly_chart(fig, use_container_width=True)
            st.markdown(f"""
<div class="final-conclusion">
<h4>Análisis del gráfico</h4>
<p>
El gráfico se construyó utilizando la variable <strong>{campo}</strong> y la
variable calculada <strong>Frecuencia</strong>. Al ser un campo categórico, se
muestran las categorías más repetidas dentro del archivo cargado.
</p>
</div>
""", unsafe_allow_html=True)

    except Exception as e:
        st.error("No se pudo leer el archivo cargado")
        st.write(e)

else:
    st.info("Carga un archivo para iniciar el análisis")

#footer
st.markdown("""
<footer class="footer">
    <span>© 2026 Olga Vanessa Sorto Fuentes — Todos los derechos reservados</span>
</footer>
""", unsafe_allow_html=True)