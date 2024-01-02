import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Configura las credenciales para acceder a la API de Google Sheets
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('my-project-uri-409012-2928f7e18a5a.json', scope)
client = gspread.authorize(creds)

# Abre la hoja de cálculo usando el enlace público
spreadsheet_url = "https://docs.google.com/spreadsheets/d/1Iwv9GfbNPm-UtI85kz1Qc3Ng2wVS9BfnfU0qJwfmPiQ/edit?usp=sharing"
sh = client.open_by_url(spreadsheet_url)
worksheet = sh.get_worksheet(0)  # Elige la hoja de trabajo (worksheet) adecuada

st.set_page_config(page_title="HTA", layout="wide")

# Variable global para almacenar el estado del DataFrame
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=['Team Name', 'Rival Team Name', 'Lineup', 'Phase Game', 'Inici',
                                                'Def Type', 'Player', 'Action Type', 'Feeder', 'Sub Action', 'Espai'])

# Función para manejar las acciones y actualizar el DataFrame
def handle_action(team_name, rival_team, campo, phasegame, start, def_type, player, action_type, player2, sub_action_type, space):
    new_row = {'Team Name': team_name, 'Rival Team Name': rival_team, 'Lineup': campo, 'Phase Game': phasegame, 'Inici': start,
               'Def Type': def_type, 'Player': player, 'Action Type': action_type, 'Feeder': player2, 'Sub Action': sub_action_type, 'Espai': space}
    
    # Obtener el DataFrame almacenado en la variable de estado
    df_copy = st.session_state.df.copy()
    
    # Agregar una nueva fila al DataFrame
    df_copy = pd.concat([df_copy, pd.DataFrame([new_row])], ignore_index=True)
    
    # Actualizar la variable de estado con el DataFrame actualizado
    st.session_state.df = df_copy
    
    return df_copy

col1, col2, col3, col4 = st.columns(4)
 
with col1:
    # Interfaz de usuario con Streamlit
    st.markdown('**HANDBALL TEAM ANALYSIS**')
    # Pedir información inicial
    team_name = st.text_input('Equipo')
    rival_team = st.text_input('Rival')
    campo = st.text_input('Jugadores a Pista')
    st.checkbox("Activate Mode Horitzontal", key="horizontal")

with col2:
    #Fase Joc
    phasegame = st.radio(':green[**FASE JUEGO**]', ['Ataque','Defensa'], horizontal=st.session_state.horizontal)
    #Inici:
    start = st.radio(':green[**SITUACIÓN JUEGO**]', ['Posicional','Falta', 'Contraataque','2da oleada', 'Contragol','Repliegue', 'Inferioridad', 'Superioridad'], horizontal=st.session_state.horizontal)
    # Desglosar tipos de acción y zonas en botones
    def_type = st.radio('**TIPO DEFENSA**', ('6:0','5:1','3:3','3:2:1', '4:2','5:0','4:0','Individual'), horizontal=st.session_state.horizontal)

with col3:
    player = st.text_input('**Nº JUGADOR**')
    action_type = st.radio(':red[**ACCIÓN**]', ('Gol','Falta','Parada', 'Palo/Fuera', 'Passos', 'Dobles', 'Ataque', 'Area', 'Recuperación','Mal pase', 'Mala recepción', '2 min', 'Penalti', 'Pasivo'), horizontal=st.session_state.horizontal)
    player2 = st.text_input('**Nº FEEDER**')
    sub_action_type = st.radio(':red[**SUB ACCIÓN**]', ('NA','Asistencia','Desmarque sin balón'), horizontal=st.session_state.horizontal)
    
with col4:
    # Espais Atacats
    space = st.radio(':orange[**SELECCIONA ESPACIO ATACADO/DEFENDIDO**]',
                         ('6m 0-1', '6m 1-2', '6m 2-3', '6m 3-3', '6m 3-2', '6m 2-1', '6m 1-0', '7m', '9mIzquierda', '9mCentro', '9mDerecha', 'Otros'), horizontal=st.session_state.horizontal)
    # Botón para agregar información a Google Sheets
    if st.button('**REGISTRAR ACCIÓN**'):
        # Obtener los valores de los campos
        team_name_value = team_name
        rival_team_value = rival_team
        campo_value = campo
        phasegame_value = phasegame
        start_value = start
        def_type_value = def_type
        player_value = player
        action_type_value = action_type
        player2_value = player2
        sub_action_type_value = sub_action_type
        space_value = space
    
        # Llamar a la función handle_action con los valores obtenidos
        action_data = handle_action(team_name_value, rival_team_value, campo_value, phasegame_value, start_value, def_type_value, player_value, action_type_value, player2_value, sub_action_type_value, space_value)
    
        # Agrega nueva fila a la hoja de cálculo
        worksheet.append_row(action_data.iloc[-1].values.tolist())
        st.success('Información agregada correctamente a Google Sheets')
