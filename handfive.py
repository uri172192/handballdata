import streamlit as st

def home():
    st.title("Home")
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
    st.title("Scorers")
    st.write("Esta es la página de información.")
    st.write("Aquí puedes encontrar detalles sobre la aplicación.")
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import altair as alt
from vega_datasets import data
import matplotlib.colors as mcolors

st.set_page_config(layout="wide")
st.title('🏐Scorers')
st.header('🎯Goleadores Asobal')
st.subheader('📌Consulta todos los goleadores según **equipo**:')

df = pd.read_excel(r"C:\Users\Lenovo\Downloads\datapps\pages\DatasetJugadoresAsobal.xlsx")

## Conseguir lista de equipos
Equipos = df['Equipo'].unique()

## Create the select box
selected_team = st.selectbox('Escoge equipo:', Equipos)

## Filter the data
filtered_data = df[df['Equipo'] == selected_team]

## Generate unique colors for each team (combining multiple color scales)
team_colors1 = dict(zip(Equipos[:8], mcolors.TABLEAU_COLORS.values()))
team_colors2 = dict(zip(Equipos[8:16], mcolors.XKCD_COLORS.values()))
team_colors = {**team_colors1, **team_colors2}

## Graph
graph = alt.Chart(filtered_data).encode(
    x='ToG',
    y=alt.Y("Jugador").sort('-x'),
    text='ToG',
    tooltip=['Jugador', 'Equipo', 'ToG', 'ToS', 'To%'],
    color=alt.Color("Equipo", scale=alt.Scale(domain=list(team_colors.keys()), range=list(team_colors.values())))
)
plotfinal = graph.mark_bar() + graph.mark_text(align='left', dx=2)
st.altair_chart(plotfinal, use_container_width=True)

st.caption("🔎Fuente: Asobal")
expander = st.expander(" ➕ **LEGEND**")
expander.write("**ToG** = Total Goles Marcados")
expander.write("**ToS** = Total Lanzamientos Intentados")
expander.write("**To%** = Porcentaje de acierto en el lanzamiento")

st.divider()

st.subheader('📌Consulta todos los goleadores según **posición**:')
## Conseguir lista de posiciones
Pos = df['Posicion'].unique()

## Create the select box (filter)
selected_pos = st.selectbox('Selecciona posición:', Pos)

## Filter the data
filtered_data = df[df['Posicion'] == selected_pos]

## Graph
graph = alt.Chart(filtered_data).encode(
    x='ToG',
    y=alt.Y("Jugador").sort('-x'),
    text='ToG',
    tooltip=['Jugador', 'Posicion', 'Equipo', 'ToG', 'ToS', 'To%'],
    color=alt.Color("Equipo", scale=alt.Scale(domain=list(team_colors.keys()), range=list(team_colors.values())))
)
plotfinalpos = graph.mark_bar() + graph.mark_text(align='left', dx=2)
st.altair_chart(plotfinalpos, use_container_width=True)

st.caption("🔎Fuente: Asobal")
expander = st.expander(" ➕ **LEGEND**")
expander.write("**ToG** = Total Goles Marcados")
expander.write("**ToS** = Total Lanzamientos Intentados")
expander.write("**To%** = Porcentaje de acierto en el lanzamiento")

# Configurar la barra lateral para navegar entre las páginas
# Utilizamos un diccionario para asignar el nombre de la página a su función correspondiente
pages = {
    "Home": home,
    "Scorers": about
}

# Configurar la barra lateral
st.sidebar.title("HDA")
selection = st.sidebar.radio(list(pages.keys()))

# Ejecutar la función de la página seleccionada
page = pages[selection]
page()
