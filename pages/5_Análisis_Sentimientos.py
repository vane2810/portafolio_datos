#PAGINA DE ANALISIS DE SENTIMIENTOS :Z
import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


st.set_page_config(
    page_title="Análisis de Sentimientos",
    layout="wide",
    initial_sidebar_state="collapsed"
)


def cargar_css():
    with open("assets/styles/analisis.css", "r", encoding="utf-8") as archivo:
        st.markdown(f"<style>{archivo.read()}</style>", unsafe_allow_html=True)


cargar_css()


st.markdown("""
<section class="module-hero">

<div class="module-left">

<h1>Análisis de Sentimientos</h1>

<p class="subtitle">
Lectura de opiniones desde un sitio web y clasificación automática
del sentimiento expresado en los textos obtenidos
</p>

</div>

<div class="module-icon">
<i class="fa-solid fa-comments"></i>
</div>

</section>
""", unsafe_allow_html=True)


st.markdown("""
<div class="section-box">
<h2>Análisis de sentimientos y scraping</h2>
</div>
""", unsafe_allow_html=True)


palabras_positivas = [
    "bueno", "excelente", "genial", "increíble", "agradable", "positivo",
    "feliz", "recomendado", "maravilloso", "perfecto", "bonito", "útil",
    "satisfecho", "encanta", "mejor", "calidad", "rápido", "eficiente",
    "fácil", "interesante", "importante", "exitoso"
]

palabras_negativas = [
    "malo", "terrible", "horrible", "negativo", "triste", "problema",
    "lento", "difícil", "deficiente", "peor", "molesto", "error",
    "fallo", "aburrido", "caro", "pésimo", "desagradable", "inútil",
    "complicado", "mal", "fracaso"
]


def analizar_sentimiento(texto):
    texto_limpio = texto.lower()

    positivos = sum(1 for palabra in palabras_positivas if palabra in texto_limpio)
    negativos = sum(1 for palabra in palabras_negativas if palabra in texto_limpio)

    puntaje = positivos - negativos

    if puntaje > 0:
        return "Positivo"
    elif puntaje < 0:
        return "Negativo"
    else:
        return "Neutral"


def validar_url(url):
    url = url.strip()

    if url == "":
        return False, "Ingresa una URL para iniciar el análisis."

    if not url.startswith(("http://", "https://")):
        return False, "La URL debe iniciar con http:// o https://"

    partes_url = urlparse(url)

    if partes_url.netloc == "":
        return False, "Ingresa una URL válida. Ejemplo: https://ejemplo.com"

    return True, url


def obtener_textos_desde_url(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    respuesta = requests.get(url, headers=headers, timeout=10)
    respuesta.raise_for_status()

    soup = BeautifulSoup(respuesta.text, "html.parser")

    elementos = soup.find_all(["p", "h2", "h3"])

    textos = []

    for elemento in elementos:
        texto = elemento.get_text(strip=True)

        if len(texto) >= 40:
            textos.append(texto)

    return textos


url = st.text_input(
    "Ingresa la URL del sitio a analizar",
    placeholder="https://ejemplo.com/opiniones"
)
st.caption("💡 Puedes usar este foro de ejemplo: https://soporte.miarroba.com/7/13018141-general-20-anos-juntos/")



if st.button("Analizar sentimientos"):

    url_valida, resultado_url = validar_url(url)

    if not url_valida:
        st.warning(resultado_url)

    else:

        try:
            textos = obtener_textos_desde_url(resultado_url)

            if len(textos) == 0:
                st.warning("No se encontraron textos suficientes para analizar.")

            else:
                df_sentimientos = pd.DataFrame({
                    "Opinión": textos
                })

                df_sentimientos["Sentimiento"] = df_sentimientos["Opinión"].apply(
                    analizar_sentimiento
                )

                st.markdown("""
<div class="chart-title">
<h4>Scrapping de opiniones</h4>
<p>
Se muestran los textos encontrados en el sitio web ingresado.
</p>
</div>
""", unsafe_allow_html=True)

                st.dataframe(
                    df_sentimientos,
                    use_container_width=True,
                    height=450
                )
                st.markdown("""
<h4>Resumen de sentimientos encontrados</h4>
</div>
""", unsafe_allow_html=True)

                conteo = (
                    df_sentimientos["Sentimiento"]
                    .value_counts()
                    .reset_index()
                )
                

                conteo.columns = ["Sentimiento", "Cantidad"]

                col1, col2, col3 = st.columns(3)

                positivos = conteo.loc[
                    conteo["Sentimiento"] == "Positivo",
                    "Cantidad"
                ].sum()

                negativos = conteo.loc[
                    conteo["Sentimiento"] == "Negativo",
                    "Cantidad"
                ].sum()

                neutrales = conteo.loc[
                    conteo["Sentimiento"] == "Neutral",
                    "Cantidad"
                ].sum()

                col1.metric("Positivos", int(positivos))
                col2.metric("Negativos", int(negativos))
                col3.metric("Neutrales", int(neutrales))

                st.markdown("""
<div class="chart-title">
<h4>Resultado del análisis</h4>
<p>
Distribución de sentimientos encontrados en las opiniones leídas.
</p>
</div>
""", unsafe_allow_html=True)

                fig = px.bar(
                    conteo,
                    x="Sentimiento",
                    y="Cantidad",
                    title="Distribución de sentimientos",
                    template="plotly_dark",
                    text="Cantidad"
                )

                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(15,23,42,0.65)",
                    font=dict(color="#f8fafc"),
                    title_font=dict(size=22),
                    xaxis_title="Sentimiento",
                    yaxis_title="Cantidad"
                )

                st.plotly_chart(fig, use_container_width=True)

                sentimiento_dominante = conteo.loc[
                    conteo["Cantidad"].idxmax(),
                    "Sentimiento"
                ]

                if sentimiento_dominante == "Positivo":
                    conclusion = """
La mayoría de opiniones analizadas presentan un sentimiento positivo.
Esto indica que el contenido leído refleja aceptación, satisfacción
o comentarios favorables por parte de los usuarios.
"""
                elif sentimiento_dominante == "Negativo":
                    conclusion = """
La mayoría de opiniones analizadas presentan un sentimiento negativo.
Esto indica que existen críticas, inconformidades o experiencias
desfavorables relacionadas con el contenido analizado.
"""
                else:
                    conclusion = """
La mayoría de opiniones analizadas presentan un sentimiento neutral.
Esto indica que gran parte de los textos encontrados son informativos
o no expresan emociones claramente positivas o negativas.
"""

                st.markdown(f"""
<div class="chart-title">
<h4>Conclusión del análisis</h4>
<p>{conclusion}</p>
</div>
""", unsafe_allow_html=True)

        except requests.exceptions.ConnectionError:
            st.error("No se pudo conectar con el sitio web. Verifica que la URL exista o que tengas conexión a internet.")

        except requests.exceptions.Timeout:
            st.error("El sitio web tardó demasiado en responder. Intenta con otra URL.")

        except requests.exceptions.HTTPError as e:
            st.error("El sitio web respondió con un error HTTP. Puede que la página no exista o esté bloqueada.")
            

        except requests.exceptions.InvalidURL:
            st.error("La URL ingresada no es válida. Revisa que esté escrita correctamente.")

        except Exception as e:
            st.error("Ocurrió un error inesperado al analizar el sitio web.")


#footer
st.markdown("""
<footer class="footer">
    <span>© 2026 Olga Vanessa Sorto Fuentes — Todos los derechos reservados</span>
</footer>
""", unsafe_allow_html=True)