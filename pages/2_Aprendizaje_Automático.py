#PAGINA DE APRENDIZAJE AUTOMATICO :V

import streamlit as st
import pandas as pd
import plotly.express as px

from sklearn.tree import plot_tree
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error


st.set_page_config(
    page_title="Aprendizaje Automático",
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

<h1>Aprendizaje Automático</h1>

<p class="subtitle">
Entrenamiento de modelos predictivos utilizando variables del dataset,
algoritmos supervisados y división de datos de entrenamiento y prueba
</p>

</div>

<div class="module-icon">
<i class="fa-solid fa-brain"></i>
</div>

</section>
""", unsafe_allow_html=True)


st.markdown("""
<div class="section-box">
<h2>Configuración del modelo</h2>
<p>
Selecciona el algoritmo, la variable que deseas predecir, la variable independiente
y el porcentaje de datos que se utilizará para entrenamiento y prueba
</p>
</div>
""", unsafe_allow_html=True)


columnas_numericas = df.select_dtypes(include=["int64", "float64"]).columns.tolist()

variables_objetivo = [
    "popularity",
    "energy",
    "danceability",
    "valence",
    "tempo"
]

variables_objetivo = [col for col in variables_objetivo if col in columnas_numericas]

variables_independientes = [
    "energy",
    "danceability",
    "valence",
    "tempo",
    "loudness",
    "acousticness",
    "speechiness",
    "instrumentalness",
    "liveness",
    "duration_ms"
]

variables_independientes = [col for col in variables_independientes if col in columnas_numericas]


col1, col2 = st.columns(2)

with col1:
    algoritmo = st.selectbox(
        "Selecciona el algoritmo",
        [
            "Regresión Lineal",
            "Árbol de Decisión"
        ]
    )

with col2:
    porcentaje_entrenamiento = st.slider(
        "Porcentaje de datos para entrenamiento",
        min_value=50,
        max_value=90,
        value=80,
        step=5
    )


col3, col4 = st.columns(2)

with col3:
    variable_objetivo = st.selectbox(
        "Selecciona la variable a analizar",
        variables_objetivo
    )

with col4:
    variable_independiente = st.selectbox(
        "Selecciona la variable independiente",
        [col for col in variables_independientes if col != variable_objetivo]
    )


porcentaje_prueba = 100 - porcentaje_entrenamiento

st.markdown(f"""
<div class="analysis-grid">

<div class="analysis-card">
<h4>Datos de entrenamiento</h4>
<p>Se utilizará el <strong>{porcentaje_entrenamiento}%</strong> del dataset para entrenar el modelo</p>
</div>

<div class="analysis-card">
<h4>Datos de prueba</h4>
<p>Se utilizará el <strong>{porcentaje_prueba}%</strong> restante para evaluar las predicciones</p>
</div>

</div>
""", unsafe_allow_html=True)


datos_modelo = df[[variable_independiente, variable_objetivo]].dropna().copy()

X = datos_modelo[[variable_independiente]]
y = datos_modelo[variable_objetivo]

test_size = porcentaje_prueba / 100

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=test_size,
    random_state=42
)


if algoritmo == "Regresión Lineal":
    modelo = LinearRegression()
else:
    modelo = DecisionTreeRegressor(
        max_depth=5,
        random_state=42
    )


modelo.fit(X_train, y_train)

predicciones = modelo.predict(X_test)
predicciones_entrenamiento = modelo.predict(X_train)


r2 = r2_score(y_test, predicciones)
mae = mean_absolute_error(y_test, predicciones)
mse = mean_squared_error(y_test, predicciones)


st.markdown("""
<div class="section-box">
<h2>Resultados del entrenamiento</h2>
<p>
A continuación se muestran las métricas principales del modelo entrenado
</p>
</div>
""", unsafe_allow_html=True)


m1, m2, m3, m4 = st.columns(4)

m1.metric("Algoritmo", algoritmo)
m2.metric("R²", round(r2, 3))
m3.metric("MAE", round(mae, 3))
m4.metric("MSE", round(mse, 3))


if algoritmo == "Regresión Lineal":
    coeficiente = modelo.coef_[0]
    intercepto = modelo.intercept_

    c1, c2 = st.columns(2)
    c1.metric("Coeficiente", round(coeficiente, 4))
    c2.metric("Intercepto", round(intercepto, 4))

else:
    st.metric("Profundidad del árbol", modelo.get_depth())


df_train = X_train.copy()
df_train[variable_objetivo] = y_train
df_train["Tipo"] = "Entrenamiento"
df_train["Predicción"] = predicciones_entrenamiento

df_test = X_test.copy()
df_test[variable_objetivo] = y_test
df_test["Tipo"] = "Prueba"
df_test["Predicción"] = predicciones


df_grafico = pd.concat([df_train, df_test])

if len(df_grafico) > 6000:
    df_grafico = df_grafico.sample(6000, random_state=42)


st.markdown("""
<div class="chart-title">
<h4>Visualización del modelo</h4>
<p>
La gráfica muestra los datos de entrenamiento, los datos de prueba
y las predicciones generadas por el modelo
</p>
</div>
""", unsafe_allow_html=True)


if algoritmo == "Regresión Lineal":

    fig = px.scatter(
        df_grafico,
        x=variable_independiente,
        y=variable_objetivo,
        color="Tipo",
        opacity=0.55,
        title=f"{variable_objetivo} según {variable_independiente}",
        template="plotly_dark",
        trendline="ols"
    )


else:

    fig = px.scatter(
        df_grafico,
        x=variable_independiente,
        y=variable_objetivo,
        color="Tipo",
        opacity=0.55,
        title=f"{variable_objetivo} según {variable_independiente}",
        template="plotly_dark"
    )

fig.add_scatter(
    x=df_test[variable_independiente],
    y=df_test["Predicción"],
    mode="markers",
    name="Predicciones",
    marker=dict(size=6, symbol="x")
)

fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(15,23,42,0.65)",
    font=dict(color="#f8fafc"),
    title_font=dict(size=22),
    xaxis_title=variable_independiente,
    yaxis_title=variable_objetivo
)

st.plotly_chart(fig, use_container_width=True)


st.markdown(f"""
<div class="final-conclusion">
<h4>Interpretación del modelo</h4>
<p>
El modelo intenta predecir la variable <strong>{variable_objetivo}</strong>
a partir de la variable <strong>{variable_independiente}</strong>
El valor R² indica qué tan bien el modelo explica el comportamiento de los datos.
Un valor cercano a 1 representa mejor ajuste, mientras que un valor cercano a 0
indica bajo poder predictivo
</p>
</div>
""", unsafe_allow_html=True)

#footer
st.markdown("""
<footer class="footer">
    <span>© 2026 Olga Vanessa Sorto Fuentes — Todos los derechos reservados</span>
</footer>
""", unsafe_allow_html=True)