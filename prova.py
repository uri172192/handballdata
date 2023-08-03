import streamlit as st

def home():
    st.title("Página de Inicio")
    st.write("¡Bienvenido a mi aplicación multipágina!")
    st.write("Seleccione una página en el menú de la izquierda.")

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
