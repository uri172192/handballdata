import streamlit as st
import pandas as pd

st.set_page_config(page_title="HTA", layout="wide")

# Función para manejar las acciones y actualizar el DataFrame
def handle_action(team_name, rival_team, campo, phasegame, start, def_type, player, action_type, player2, sub_action_type, space):
    new_row = {'Team Name': team_name, 'Rival Team Name': rival_team, 'Lineup': campo, 'Phase Game': phasegame, 'Inici': start,
               'Def Type': def_type, 'Player': player, 'Action Type': action_type, 'Feeder': player2,'Sub Action': sub_action_type, 'Espai': space}
    global df
    df = df.append(new_row, ignore_index=True)

df = pd.DataFrame()

col1, col2, col3, col4 = st.columns(4)
 
with col1:

    # Interfaz de usuario con Streamlit
        st.markdown('**HANDBALL TEAM ANALYSIS**')

    # Pedir información inicial
        team_name = st.text_input('Equipo')
        rival_team = st.text_input('Rival')
        campo = st.text_input('Jugadores a Pista')

with col2:

    #Fase Joc
    phasegame = st.selectbox(':green[Fase Juego]', ['Ataque','Defensa'])

    #Inici:
    start = st.selectbox(':green[Situación Juego]', ['Posicional','Golpe', 'Contraataque','2na oleada', 'Contragol','Repliegue'])
    # Desglosar tipos de acción y zonas en botones
    def_type = st.selectbox('**Tipo Defensa**', ('6:0','5:1','3:3','3:2:1', '4:2','Individual'))


with col3:

    player = st.text_input('**Nº Jugador**')
    action_type = st.selectbox (':red[**Acción**]', ('Gol','Falta','Parada', 'Palo/Fuera', 'Passos', 'Dobles', 'Ataque', 'Area', 'Mal pase', 'Mala recepción', '2 min', 'Penalti', 'Pasivo'))
    player2 = st.text_input('**Nº Feeder**')
    sub_action_type = st.selectbox (':red[**Sub Acción**]', ('NA','Fijación','Asistencia','Desmarque sin balón'))
    
with col4:

    # Selectbox para seleccionar la opción de asistencia

     # Espais Atacats
    space = st.selectbox(
        ':orange[Selecciona Espacio Atacado/Defendido]',
        ('0-1', '1-2', '2-3', '3-3', '3-2', '2-1', '1-0', '7m', '9mIzquierda', '9mCentro', '9mDerecha', 'Otros'))
    

    if st.button('**Registrar Acción**'):
        # Agregar las acciones registradas al DataFrame
        handle_action(team_name, rival_team, campo, phasegame, start, def_type, player, action_type, player2, sub_action_type, space)
        st.success('Acción registrada con éxito!')

    if st.button(':green[**Guardar en Excel**]'):
        df.to_excel("acciones_balonmano.xlsx", index=False)
        st.success('Datos guardados en acciones_balonmano.xlsx')
