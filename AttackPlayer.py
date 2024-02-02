from cProfile import label
import streamlit as st
import pandas as pd
from PIL import Image
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import streamlit_antd_components as sac

# Configura las credenciales para acceder a la API de Google Sheets
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('my-project-uri-409012-2928f7e18a5a.json', scope)
client = gspread.authorize(creds)

# Abre la hoja de cálculo usando el enlace público
spreadsheet_url = "https://docs.google.com/spreadsheets/d/1HHScRuSrhk0n1cTGNKDkW2P-yuMsNUXMNLocZJ43oeA/edit?usp=sharing"
sh = client.open_by_url(spreadsheet_url)
worksheet = sh.get_worksheet(0)  # Elige la hoja de trabajo (worksheet) adecuada

st.set_page_config(page_title="HPAA", layout="wide")

# Función para manejar las acciones y actualizar el DataFrame
def handle_action(player_name, position, rival_team, phasegame, start, action_type, sub_action_type, space, shoot_action_type, shoot_action_distance, howshoot, ast_action_typeast, result):
    new_row = {'Player Name': player_name, 'Position': position, 'Rival Team Name': rival_team, 'Phase Game': phasegame, 'Inici': start,
               'Action Type': action_type, 'Sub Action Type': sub_action_type, 'Espai': space, 'Xut': shoot_action_type, 'Shoot Distance': shoot_action_distance, 'How Shoot': howshoot, 'Assist': ast_action_typeast, 'Result': result}
    # Obtener el DataFrame almacenado en la variable de estado
    df_copy = st.session_state.df.copy()

    # Agregar una nueva fila al DataFrame
    df_copy = pd.concat([df_copy, pd.DataFrame([new_row])], ignore_index=True)
    
    # Actualizar la variable de estado con el DataFrame actualizado
    st.session_state.df = df_copy
    
    return df_copy
         
# Variable global para almacenar el estado del DataFrame
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame()

st.markdown('**HANDBALL PLAYER ATTACK ANALYSIS**')
col1, col2, col3 = st.columns(3)

with col1:
        player_name = st.text_input('Nombre Jugador')
with col2:
        position = st.text_input('Posición')
with col3:
        rival_team = st.text_input('Rival')

col1, col2, col3 = st.columns(3)

with col1:

    phasegame = sac.segmented(items=[sac.SegmentedItem(label='Ataque'),
                                     sac.SegmentedItem(label='Defensa'), 
                                     sac.SegmentedItem(label='Contraataque')],label='**Fase Juego**', align='left', size='sm')

    #Inici:
    start = sac.segmented(items=[sac.SegmentedItem(label='Parat'),
                                     sac.SegmentedItem(label='Carrera'), 
                                     sac.SegmentedItem(label='Bot'),
                                     sac.SegmentedItem(label='T Fort'),
                                     sac.SegmentedItem(label='T Feble')],label='**Inicio Juego**', align='left', size='sm')
    
    # Desglosar tipos de acción y zonas en botones
    action_type = sac.segmented(items=[sac.SegmentedItem(label='Xut'),
                                     sac.SegmentedItem(label='Pase'), 
                                     sac.SegmentedItem(label='Finta Fuerte'),
                                     sac.SegmentedItem(label='Finta Debil'),
                                     sac.SegmentedItem(label='Mala recepcion'),
                                     sac.SegmentedItem(label='Mal pase'),
                                     sac.SegmentedItem(label='Pasos'),
                                     sac.SegmentedItem(label='Dobles'),
                                     sac.SegmentedItem(label='Ataque')],label='**Inicio Juego**', align='left', size='sm')
    
    sub_action_type = sac.segmented(items=[sac.SegmentedItem(label='NA'),
                                     sac.SegmentedItem(label='Xut'),
                                     sac.SegmentedItem(label='Asistencia'), 
                                     sac.SegmentedItem(label='Pérdida')],label='**Sub Action Type**', align='left', size='sm')

with col2:

    # Selectbox para seleccionar la opción de tiro
    shoot_action_type = sac.segmented(items=[sac.SegmentedItem(label='Corto'),
                                     sac.SegmentedItem(label='Largo'), 
                                     sac.SegmentedItem(label='Cruzado'),
                                     sac.SegmentedItem(label='Paralelo')],label='**Shoot Action Type**', align='left', size='sm')

    # Select distancia del lanzamiento
    shoot_action_distance = sac.segmented(items=[sac.SegmentedItem(label='NA'),
                                     sac.SegmentedItem(label='6m'), 
                                     sac.SegmentedItem(label='7m'),
                                     sac.SegmentedItem(label='9m')],label='**Shoot Action Distance**', align='left', size='sm')
     
    #Selecciona como se produce el lanzamiento
    howshoot = sac.segmented(items=[sac.SegmentedItem(label='NA'),
                                     sac.SegmentedItem(label='Salto'), 
                                     sac.SegmentedItem(label='Pie parado')],label='**Shoot Action Type**', align='left', size='sm')

with col3:

    # Selectbox para seleccionar la opción de asistencia
    ast_action_typeast = sac.segmented(items=[sac.SegmentedItem(label='NA'),
                                     sac.SegmentedItem(label='PI'), 
                                     sac.SegmentedItem(label='CE'),
                                     sac.SegmentedItem(label='LD'),
                                     sac.SegmentedItem(label='LI'),
                                     sac.SegmentedItem(label='ED'),
                                     sac.SegmentedItem(label='EI')],label='**Asistencia Action Type**', align='left', size='sm')


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
 
    result = sac.segmented(items=[sac.SegmentedItem(label='Gol'),
                                         sac.SegmentedItem(label='No Gol'), 
                                         sac.SegmentedItem(label='Falta'),
                                         sac.SegmentedItem(label='Fijacion'),
                                         sac.SegmentedItem(label='7m')],label='**Resultado**', align='left', size='sm', color='green')
        
    # Botón para agregar información a Google Sheets
    if st.button('**REGISTRAR ACCIÓN**'):
            # Obtener los valores de los campos
            player_name_value = player_name
            position_value = position
            rival_team_value = rival_team
            phasegame_value = phasegame
            start_value = start
            action_type_value = action_type
            sub_action_type_value = sub_action_type
            space_value = space
            shoot_action_type_value = shoot_action_type
            shoot_action_distance_value = shoot_action_distance, 
            howshoot_value =  howshoot 
            ast_action_typeast_value = ast_action_typeast
            result_value = result
            
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
               '9m Der': '9mDerecha',
               '-   Medio Campo   -':'Medio Campo',
               '-   Propio Campo   -': 'Propio Campo'
             }
    
            # Obtener el valor mapeado para el espacio seleccionado en la aplicación
            space_value_mapped = espacio_mapping.get(space_value, space_value)
    
            # Llamar a la función handle_action con los valores obtenidos
            action_data = handle_action(player_name, position_value, rival_team_value, phasegame_value, start_value, action_type_value, sub_action_type_value, space_value_mapped, shoot_action_type_value, shoot_action_distance_value, howshoot_value, ast_action_typeast_value, result_value)
        
            # Agrega nueva fila a la hoja de cálculo
            worksheet.append_row(action_data.iloc[-1].values.tolist())
            st.success('Información agregada correctamente a Google Sheets')
