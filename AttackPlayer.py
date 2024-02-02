from cProfile import label
import streamlit as st
import pandas as pd
from PIL import Image
import streamlit_antd_components as sac

st.set_page_config(page_title="HPAA", layout="wide")

# Función para manejar las acciones y actualizar el DataFrame
def handle_action(player_name, position, rival_team, phasegame, start, action_type, sub_action_type, space, shoot_action_type, shoot_action_distance, howshoot, ast_action_typeast, result, df):
    new_row = {'Player Name': player_name, 'Position': position, 'Rival Team Name': rival_team, 'Phase Game': phasegame, 'Inici': start,
               'Action Type': action_type, 'Sub Action Type': sub_action_type, 'Espai': space, 'Xut': shoot_action_type, 'Shoot Distance': shoot_action_distance, 'How Shoot': howshoot, 'Assist': ast_action_typeast, 'Result': result}
    df = df.append(new_row, ignore_index=True)
    return df

# Variable global para almacenar el estado del DataFrame
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame()

st.markdown('**HANDBALL PLAYER ATTACK ANALYSIS**')
col1, col2, col3 = st.columns(3)

with col1:
        player_name = st.text_input('Nom Jugador')
with col2:
        position = st.text_input('Posició')
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
                              [
                               sac.SegmentedItem(label='0-1'),
                               sac.SegmentedItem(label='7 metros'),
                               sac.SegmentedItem(label='1-0'),
                               sac.SegmentedItem(label='1-2'),
                               sac.SegmentedItem(label='2-3'),
                               sac.SegmentedItem(label='3-3'),
                               sac.SegmentedItem(label='3-2'),
                               sac.SegmentedItem(label='2-1'),
                               sac.SegmentedItem(label='9m Izq'),
                               sac.SegmentedItem(label='9m Centro'),
                               sac.SegmentedItem(label='Medio Campo'),
                               sac.SegmentedItem(label='Propio Campo')
                               ],
                               label='**Espacio Atacado/Defendido**', size='md', direction='horizontal')
    
    # Botones para seleccionar la zona
    result = sac.segmented(items=[sac.SegmentedItem(label='Gol'),
                                     sac.SegmentedItem(label='No Gol'), 
                                     sac.SegmentedItem(label='Falta'),
                                     sac.SegmentedItem(label='Fijacion'),
                                     sac.SegmentedItem(label='7m')],label='**Resultado**', align='left', size='sm', color='green')


    # Botón para registrar la acción
    if st.button('**Registrar Acción**'):
        st.session_state.df = handle_action(player_name, position, rival_team, phasegame, start, action_type, sub_action_type, space, shoot_action_type, shoot_action_distance, howshoot, ast_action_typeast, result, st.session_state.df)
        st.success('Acción registrada con éxito!')

    # Mostrar el DataFrame actualizado
    st.write('Acciones Registradas:')
    st.write(st.session_state.df)

    # Guardar el DataFrame en un archivo Excel al finalizar la sesión
    if st.button(':green[**Guardar en Excel**]'):
        st.session_state.df.to_excel('acciones_balonmano.xlsx', index=False)
        st.success('Datos guardados en acciones_balonmano.xlsx')
