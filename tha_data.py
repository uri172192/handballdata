from cProfile import label
import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit_antd_components as sac
import time

# Configura las credenciales para acceder a la API de Google Sheets
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('my-project-uri-409012-2928f7e18a5a.json', scope)
client = gspread.authorize(creds)

# Abre la hoja de cálculo usando el enlace público
spreadsheet_url = "https://docs.google.com/spreadsheets/d/1Iwv9GfbNPm-UtI85kz1Qc3Ng2wVS9BfnfU0qJwfmPiQ/edit?usp=sharing"
sh = client.open_by_url(spreadsheet_url)
worksheet = sh.get_worksheet(0)  # Elige la hoja de trabajo (worksheet) adecuada

st.set_page_config(page_title="HTA", page_icon="favicon-32x32.png", layout="wide")

if "page" not in st.session_state:
    st.session_state.page = "home"

if st.session_state.page == "home":
    st.write("Configura los números de los jugadores:")

# Inicializa la variable de estado show_player_input si no existe
if 'show_player_input' not in st.session_state:
    st.session_state.show_player_input = True

# Antes de la creación del botón "Crear botones de jugadores"
if 'show_create_button' not in st.session_state:
    st.session_state.show_create_button = True

# En lugar de st.text_input, usa st.text_area para ingresar múltiples números separados por comas
if st.session_state.show_player_input:
    player_numbers = st.text_area("Introduce los números de los jugadores separados por comas")

if st.session_state.show_create_button and st.button("Crear botones de jugadores"):
    st.session_state.player_numbers_list = [int(x.strip()) for x in player_numbers.split(",") if x.strip().isnumeric()]
    st.session_state.page = "player_buttons"
    st.session_state.show_player_input = False  # Oculta la sección de entrada de números de jugadores
    st.session_state.show_create_button = False  # Oculta el botón "Crear botones de jugadores"
    
# Variable global para almacenar el estado del DataFrame
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=['Team Name', 'Rival Team Name', 'Lineup', 'Phase Game', 'Inici',
                                                'Def Type', 'Player', 'Action Type', 'Feeder', 'Sub Action', 'Espai'])

# Función para manejar las acciones y actualizar el DataFrame
def handle_action(team_name, rival_team, campo, phasegame, start, def_type, player, action_type, player2, sub_action_type, space):
    new_row = {'Team Name': team_name, 'Rival Team Name': rival_team, 'Lineup': ''.join(campo), 'Phase Game': phasegame, 'Inici': start,
               'Def Type': def_type, 'Player': player, 'Action Type': action_type, 'Feeder': player2, 'Sub Action': sub_action_type, 'Espai': space}
    
    # Obtener el DataFrame almacenado en la variable de estado
    df_copy = st.session_state.df.copy()

    # Agregar una nueva fila al DataFrame
    df_copy = pd.concat([df_copy, pd.DataFrame([new_row])], ignore_index=True)
    
    # Actualizar la variable de estado con el DataFrame actualizado
    st.session_state.df = df_copy
    
    return df_copy

#Info general:
col1, col2, col3 = st.columns(3)
with col1:
         #Interfaz de usuario con Streamlit
         st.markdown('**HANDBALL TEAM ANALYSIS**')
with col2:
         team_name = st.text_input('Equipo')
with col3:
         rival_team = st.text_input('Rival')

#App Data
col1, col2, col3 = st.columns(3)
 
with col1:
    #Fase Joc
    phasegame = sac.segmented(items=[sac.SegmentedItem(label='Ataque'),sac.SegmentedItem(label='Defensa')],label='**Fase Juego**', align='left', size='sm')

    #Inici:
    start = sac.segmented(items=
                              [sac.SegmentedItem(label='Contraataque'),
                               sac.SegmentedItem(label='2da oleada'),
                               sac.SegmentedItem(label='Falta'),
                               sac.SegmentedItem(label='Repliegue'),
                               sac.SegmentedItem(label='Contragol'),
                               sac.SegmentedItem(label='Superioridad'),
                               sac.SegmentedItem(label='Inferioridad'),
                               sac.SegmentedItem(label='Posicional')],
                               label='**Situación Juego**', align='left', size='sm', divider=False)
    # Desglosar tipos de acción y zonas en botones
    def_type = sac.segmented(items=
                              [sac.SegmentedItem(label='6:0'),
                               sac.SegmentedItem(label='5:1'),
                               sac.SegmentedItem(label='3:3'),
                               sac.SegmentedItem(label='3:2:1'),
                               sac.SegmentedItem(label='4:2'),
                               sac.SegmentedItem(label='5:0'),
                               sac.SegmentedItem(label='4:0'),
                               sac.SegmentedItem(label='Indiviual')],
                               label='**Tipo Defensa**', align='left', size='sm', divider=False)
with col2:
    if "page" not in st.session_state or st.session_state.page != "player_buttons":
        col2.write('')  # Clear the previous input
    else:
        #Utiliza sac.chip para generar botones con cada número de jugador
        campo = sac.chip([
            sac.ChipItem(label=str(player_num)) for player_num in st.session_state.player_numbers_list
        ], label='**Banquillo**', align='left', radius='xs', key="player_buttons", multiple=True)

        # Utiliza sac.buttons para generar botones con cada número de jugador seleccionado
        selected_player_numbers = [x for x in st.session_state.player_numbers_list if str(x) in campo]
        player_numbers_buttons = sac.buttons([sac.ButtonsItem(label=str(player_num)) for player_num in selected_player_numbers],
                                             label='**Pista**', align='left', radius='xs')
        # Obtiene el número seleccionado del botón
        player = player_numbers_buttons

        action_type = sac.segmented(items=
                              [sac.SegmentedItem(label='Gol'),
                               sac.SegmentedItem(label='Falta'),
                               sac.SegmentedItem(label='Parada'),
                               sac.SegmentedItem(label='Palo/Fuera'),
                               sac.SegmentedItem(label='Pasos'),
                               sac.SegmentedItem(label='Dobles'),
                               sac.SegmentedItem(label='Ataque'),
                               sac.SegmentedItem(label='Area'),
                               sac.SegmentedItem(label='Recuperación'),
                               sac.SegmentedItem(label='Mal Pase'),
                               sac.SegmentedItem(label='Mala Recepción'),
                               sac.SegmentedItem(label='2 min'),
                               sac.SegmentedItem(label='Penalti'),
                               sac.SegmentedItem(label='Pasivo')],
                               label='**Acción**', align='left', size='sm', divider=False)

        st.session_state.player_buttons_switch = sac.switch(label="Activar/Desactivar Feeder", value=True)
        
        # Utiliza la variable de estado del interruptor para activar o desactivar player_numbers_buttons2
        if st.session_state.player_buttons_switch:
            player_numbers_buttons2 = sac.buttons([sac.ButtonsItem(label=str(player_num)) for player_num in selected_player_numbers],
                                                 label='**Feeder**', align='left', radius='xs')
        else:
            player_numbers_buttons2 = None

        player2 = player_numbers_buttons2

        sub_action_type = sac.segmented(items=
                              [sac.SegmentedItem(label='NA'),
                               sac.SegmentedItem(label='Asistencia'),
                               sac.SegmentedItem(label='Desmarque sin balón')],
                               label='**Sub Acción**', align='left', size='sm', divider=False)
    
with col3:
    # Espais Atacats
    space = sac.segmented(items=
                              [sac.SegmentedItem(label='0-1'),
                               sac.SegmentedItem(label='...', disabled=True),
                               sac.SegmentedItem(label='7 metros'),
                               sac.SegmentedItem(label='...', disabled=True),
                               sac.SegmentedItem(label='1-0'),
                               sac.SegmentedItem(label='1-2'),
                               sac.SegmentedItem(label='2-3'),
                               sac.SegmentedItem(label='3-3'),
                               sac.SegmentedItem(label='3-2'),
                               sac.SegmentedItem(label='2-1'),
                               sac.SegmentedItem(label='9m Izq'),
                               sac.SegmentedItem(label='9m Centro'),
                               sac.SegmentedItem(label='9m Der'),
                               sac.SegmentedItem(label='-   Medio Campo   -'),
                               sac.SegmentedItem(label='-   Propio Campo   -')
                               ],
                               label='**Espacio Atacado/Defendido**', size='md', divider=False)
    
    # Botón para agregar información a Google Sheets
    if st.button('**REGISTRAR ACCIÓN**'):
        # Obtener los valores de los campos
        team_name_value = team_name
        rival_team_value = rival_team
        campo_value = ','.join(str(x) for x in campo)
        phasegame_value = phasegame
        start_value = start
        def_type_value = def_type
        player_value = player
        action_type_value = action_type
        player2_value = player2
        sub_action_type_value = sub_action_type
        space_value = space

        # Diccionario de mapeo para los valores de Espacio Atacado/Defendido
        espacio_mapping = {
           '0-1': '6m 0-1',
           '7 metros': '7m',
           '1-0': '6m 1-0',
           '1-2': '6m 1-2',
           '2-3': '6m 2-3',
           '3-3': '6m 3-3',
           '3-2': '6m 3-2',
           '2-1': '6m 2-1',
           '9m Izq': '9mIzquierda',
           '9m Centro': '9mCentro',
           '9m Derecha': '9mDerecha'
         }

        # Obtener el valor mapeado para el espacio seleccionado en la aplicación
        space_value_mapped = espacio_mapping.get(space_value, space_value)

        # Llamar a la función handle_action con los valores obtenidos
        action_data = handle_action(team_name_value, rival_team_value, campo_value, phasegame_value, start_value, def_type_value, player_value, action_type_value, player2_value, sub_action_type_value, space_value_mapped)
    
        # Agrega nueva fila a la hoja de cálculo
        worksheet.append_row(action_data.iloc[-1].values.tolist())
        st.success('Información agregada correctamente a Google Sheets')
