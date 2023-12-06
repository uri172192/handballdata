import streamlit as st
import pandas as pd
from PIL import Image

st.set_page_config(page_title="HPAA", layout="wide")

# Función para manejar las acciones y actualizar el DataFrame
def handle_action(player_name, position, team_name, rival_team, phasegame, start, action_type, sub_action_type, space, shoot_action_type, shoot_action_distance, howshoot, ast_action_typeast, result, df):
    new_row = ['Player Name': player_name, 'Position': position, 'Team Name': team_name, 'Rival Team Name': rival_team, 'Phase Game': phasegame, 'Inici': start,
               'Action Type': action_type, 'Sub Action Type': sub_action_type, 'Espai': space, 'Xut': shoot_action_type, 'Shoot Distance': shoot_action_distance, 'How Shoot': howshoot, 'Assist': ast_action_typeast, 'Result': result]
    df = df.append(new_row, ignore_index=True)
    return df

# Variable global para almacenar el estado del DataFrame
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame()

col1, col2, col3, col4 = st.columns(4)
 
with col1:

    # Interfaz de usuario con Streamlit
        st.markdown('**HANDBALL PLAYER ATTACK ANALYSIS**')

    # Pedir información inicial
        player_name = st.text_input('Nom Jugador')
        position = st.text_input('Posició')
        team_name = st.text_input('Equip')
        rival_team = st.text_input('Rival')

with col2:

    #Fase Joc
    phasegame = st.selectbox(':green[Fase Joc]', ['Atac','Defensa','Contraatac', 'Replegament'])

    #Inici:
    start = st.selectbox(':green[Inici Joc]', ['Parat','Carrera','Bot', 'T Fort', 'T Feble'])
    # Desglosar tipos de acción y zonas en botones
    action_type = st.selectbox('**Select Action Type**', ('NA','Xut','Passe','Finta Fort', 'Finta Dèbil', 'Mala recepció', 'Passos', 'Dobles', 'Atac'))
    sub_action_type = st.selectbox ('**Sub Action Type**', ('NA','Xut','Assist', 'Pèrdua'))


with col3:

    # Selectbox para seleccionar la opción de tiro
    shoot_action_type = st.selectbox(':red[Shoot Location]', ['NA','Curt', 'Llarg', 'Creuat', 'Paralel'], key='shootactiontype')

    # Select distancia del lanzamiento
    shoot_action_distance = st.radio(':red[Shoot Distance]', ['NA','6m', '7m', '9m'], key='shootactiondistance')
     
     #Selecciona como se produce el lanzamiento
    howshoot = st.selectbox(':red[How Shoot]', ['NA','Salt', 'Peu parat'], key='howshoot')
   
with col4:

    # Selectbox para seleccionar la opción de asistencia
    ast_action_typeast = st.selectbox(':blue[Assist Type]', ['NA','PI', 'CE', 'LD', 'LE', 'ED', 'EE'])

     # Espais Atacats
    space = st.selectbox(
        ':orange[Selecciona Espai Atacat]',
        ('0-1', '1-2', '2-3', '3-3', '3-2', '2-1', '1-0', '7m', '9me', '9mc', '9md', 'Altres'))
    
    # Botones para seleccionar la zona
    result = st.radio('**RESULT**',['Gol','No Gol','Falta', 'Fixació','7m'])

    # Botón para registrar la acción
    if st.button('**Registrar Acción**'):
        st.session_state.df = handle_action(player_name, position, team_name, rival_team, phasegame, start, action_type, sub_action_type, space, shoot_action_type, shoot_action_distance, howshoot, ast_action_typeast, result, df)
        st.success('Acción registrada con éxito!')

    # Mostrar el DataFrame actualizado
    st.write('Acciones Registradas:')
    st.write(st.session_state.df)

    # Guardar el DataFrame en un archivo Excel al finalizar la sesión
    if st.button(':green[**Guardar en Excel**]'):
        st.session_state.df.to_excel('acciones_balonmano.xlsx', index=False)
        st.success('Datos guardados en acciones_balonmano.xlsx')
