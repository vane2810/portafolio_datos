#PÁGINA DE INICIO :D

import streamlit as st
import base64

st.set_page_config(
    page_title="Inicio ",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def cargar_css():
    with open("assets/styles/inicio.css", "r", encoding="utf-8") as archivo:
        st.markdown(f"<style>{archivo.read()}</style>", unsafe_allow_html=True)
cargar_css()

def imagen_base64(ruta):
    with open(ruta, "rb") as img:
        return base64.b64encode(img.read()).decode()

foto = imagen_base64("assets/img/foto.png")

# aislar estilos personalizados 
st.markdown("""<div class='site-root'>""", unsafe_allow_html=True)

# contenido de la página de inicio
st.markdown(f"""
<section class="hero">

<div class="hero-text">
<p class="label">Portafolio Digital Profesional</p>
<h1>Olga Vanessa Sorto Fuentes</h1>

<p class="subtitle">
Estudiante de Ingeniería en Sistemas y Redes Informáticas, con interés en la Ciencia de Datos, el análisis exploratorio, el aprendizaje automático y el desarrollo de aplicaciones inteligentes.
<br><br>
Me apasiona transformar datos en información útil mediante visualizaciones, análisis y herramientas tecnológicas innovadoras.
</p>

<div class="personal-info">
    <span><i class="fa-solid fa-graduation-cap"></i> Universidad Gerardo Barrios</span>
    <span><i class="fa-solid fa-database"></i> Ciencia de Datos</span>
</div>
<div class="skills-badges">
    <span class="badge-skill">Python</span>
    <span class="badge-skill">Pandas</span>
    <span class="badge-skill">Scikit-learn</span>
    <span class="badge-skill">Streamlit </span>
    <span class="badge-skill">Scraping</span>
    <span class="badge-skill">Analytics</span>
    <span class="badge-skill">Machine Learning</span>
</div>
</div>

<div class="profile-card">
    <img src="data:image/png;base64,{foto}" class="profile-img">
    <p class="profile-quote">"Convirtiendo datos en decisiones inteligentes"</p>
</div>

</section>
""", unsafe_allow_html=True)

st.markdown("""
<section class="video-section">
    <h2>Data Storytelling</h2>
    <p>
    En este video se presenta una demostración del análisis realizado a partir del dataset utilizado,
    explicando los datos, las visualizaciones principales y los hallazgos obtenidos durante el proceso.
    </p>

<div class="video-container">
<iframe 
src="https://www.youtube.com/embed/pX9CMIW9Je4"
title="Demo Data Storytelling"
frameborder="0"
allowfullscreen>
</iframe>
</div>
</section>

<section class="video-section">

<h2>Contenido del Portafolio</h2>

<p class="section-description">
El portafolio integra diferentes módulos orientados al análisis de datos,
automatización inteligente y exploración
</p>

<div class="features-grid">

<div class="feature-card">
<i class="fa-solid fa-chart-line"></i>
<h3>Análisis Exploratorio</h3>
<p>
Exploración de campos, visualización de datos,
navegación del dataset e hipótesis.
</p>
</div>

<div class="feature-card">
<i class="fa-solid fa-brain"></i>
<h3>Aprendizaje Automático</h3>
<p>
Modelos predictivos con selección de variables,
algoritmos y datos de entrenamiento.
</p>
</div>

<div class="feature-card">
<i class="fa-solid fa-headphones"></i>
<h3>Recomendaciones</h3>
<p>
Sistema inteligente para sugerir canciones
según características musicales.
</p>
</div>

<div class="feature-card">
<i class="fa-solid fa-file-arrow-up"></i>
<h3>Carga de Archivos</h3>
<p>
Análisis de archivos CSV o Excel cargados
desde la computadora del usuario.
</p>
</div>

<div class="feature-card">
<i class="fa-solid fa-comments"></i>
<h3>Análisis de Sentimientos</h3>
<p>
Clasificación de opiniones musicales en
positivas, negativas o neutrales.
</p>
</div>

<div class="feature-card">
<i class="fa-solid fa-wand-magic-sparkles"></i>
<h3>Prompts IA</h3>
<p>
Consultas inteligentes sobre datasets
mediante lenguaje natural.
</p>
</div>

</div>

</section>

<footer class="footer">
<div class="footer-content">
<p class="contact-text">
Información de contacto y perfiles profesionales
</p>
<div class="footer-links">

<a href="mailto:olgavanessasf@gmail.com" target="_blank">
<i class="fa-solid fa-envelope"></i>
    olgavanessasf@gmail.com
</a>
<a href="https://github.com/vane2810" target="_blank">
<i class="fa-brands fa-github"></i>
    GitHub
</a>
<a href="https://www.linkedin.com/in/vanessa-sorto-989bb1239/" target="_blank">
<i class="fa-brands fa-linkedin"></i>
    LinkedIn
</a>
</div>
<small>
© 2026 Olga Vanessa Sorto Fuentes — Todos los derechos reservados
</small>
</div>
</footer>
""", unsafe_allow_html=True)

# Cierre del wrapper
st.markdown("""</div>""", unsafe_allow_html=True)