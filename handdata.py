import PySimpleGUI as sg
import openpyxl
from datetime import datetime

# Variables para almacenar la acción seleccionada y el número del jugador
accion_seleccionada = None
jugador_seleccionado = None

def guardar_accion():
    # Función para guardar la acción en el archivo Excel
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    datos = [ahora, accion_seleccionada, jugador_seleccionado]

    archivo_excel = "acciones_futbol.xlsx"
    try:
        libro = openpyxl.load_workbook(archivo_excel)
        hoja = libro.active
    except FileNotFoundError:
        libro = openpyxl.Workbook()
        hoja = libro.active
        hoja.append(["Fecha y Hora", "Acción", "Jugador"])

    hoja.append(datos)
    libro.save(archivo_excel)

# Ventana para ingresar los números de los jugadores
layout_jugadores = [
    [sg.Text("Ingrese los números de los jugadores que participan en el partido:")],
    [sg.Text("Separados por coma (por ejemplo, 7, 10, 22):"), sg.Input(key="jugadores")],
    [sg.Button("Aceptar")]
]

window_jugadores = sg.Window("Números de Jugadores", layout_jugadores)

event, values = window_jugadores.read()
window_jugadores.close()

numeros_jugadores = [int(num.strip()) for num in values["jugadores"].split(",")]

# Interfaz principal con botones para jugadores y acciones
layout = [
    [sg.Text("Selecciona el jugador:"), *[sg.Button(str(num), key=f"jugador_{num}") for num in numeros_jugadores]],
    [sg.Text("Selecciona la acción:"), sg.Button("Regate", key="Regate"), sg.Button("Recuperación", key="Recuperacion"),
     sg.Button("Assist", key="Assist"), sg.Button("Xut", key="Xut")],
    [sg.Button("Registrar Acción"), sg.Button("Salir")]
]

# Crear la ventana principal
window = sg.Window("Registro de Acciones de Fútbol", layout)

# Bucle para leer eventos y cerrar la aplicación cuando sea necesario
while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED or event == "Salir":
        break
    elif event == "Registrar Acción":
        if accion_seleccionada and jugador_seleccionado:
            guardar_accion()
            sg.popup("Acción registrada con éxito!")
            # Reiniciar selección después de registrar la acción
            jugador_seleccionado = None
            accion_seleccionada = None
        else:
            sg.popup_error("Por favor, selecciona jugador y acción.")

    elif any(event.startswith(f"jugador_{num}") for num in numeros_jugadores):
        jugador_seleccionado = event.split("_")[1]
    elif event in ["Regate", "Recuperacion", "Assist", "Xut"]:
        accion_seleccionada = event

# Cerrar la ventana al salir
window.close()
