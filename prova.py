import streamlit as st

def home():
    st.title("Página de Inicio")
    st.write("¡Bienvenido a mi aplicación multipágina!")
    st.write("Seleccione una página en el menú de la izquierda.")
    import streamlit as st
    import pandas as pd
    import numpy as np

    st.set_page_config(layout="wide")
    st.title('HDA🤾‍♂️📊')

    st.divider()

    st.subheader('📌Descripción HDA')
    st.write('📢**Handball Data Analytics** se presenta como una aplicación destinada al desarrollo y democratización del análisis de datos en balonmano. La finalidad es ayudar a los usarios a **disfrutar, comprender y compartir los datos sobre el balonmano**.')

    st.divider()

    st.subheader("📌Contenidos HDA")
    st.write("🏐**Scorers**: visualiza los goleadores según equipo y posición")
    st.write("🏹**Shooting Distances**: explora los máximos anotadores según la distancia del lanzamiento")
    st.write("📋**Efficiency Snapshot Asobal**: conoce como han rendido los equipos durante la temporada")
    st.write("🕵️**Shooting Similiraty**: descubre los jugadores similares entre si según su eficacia en el lanzamiento")
    st.write("🗂️**Data Consulting**: consulta los datos de los que disponemos sobre cada equipo en materia de lanzamientos")

    st.divider()

def about():
    st.title("Acerca de")
    st.write("Esta es la página de información.")
    st.write("Aquí puedes encontrar detalles sobre la aplicación.")

# Configurar la barra lateral para navegar entre las páginas
# Utilizamos un diccionario para asignar el nombre de la página a su función correspondiente
pages = {
    "Página de Inicio": home,
    "Acerca de": about
}

# Configurar la barra lateral
st.sidebar.title("Navegación")
selection = st.sidebar.radio("Ir a:", list(pages.keys()))

# Ejecutar la función de la página seleccionada
page = pages[selection]
page()
