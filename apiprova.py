import streamlit as st
import pandas as pd
import numpy as np

st.title('Welcome to my new API')
st.header("This is my header")
st.subheader('My subheader')
st.write('My name is Oriol and Im a **handbll coach**') #message
st.caption('Small caption text') #peu foto
st.code('a = 1234') #Codi per copiar de python
st.text('Hello world') #Texto simple
st.latex('\int a x') #Formulas matematicas
st.divider() #Barra separadora
df = pd.DataFrame(
   np.random.randn(50, 20),
   columns=('col %d' % i for i in range(20))) #pujar o crear df

st.dataframe(df)  #invocar df pujar
st.dataframe(df.style.highlight_max(axis=0)) #invoca df amb valors maxims marcats
#Hi ha més info sobre com editar les columnes
#EXEMPLE EDIT COLUMNA (barra progress)

data_df = pd.DataFrame(
    {
        "sales": [200, 550, 1000, 80],
    }
)

st.data_editor(
    data_df,
    column_config={
        "sales": st.column_config.ProgressColumn(
            "Sales volume",
            help="The sales volume in USD",
            format="$%f",
            min_value=0,
            max_value=1000,
        ),
    },
    hide_index=True,
)

st.metric(label="Temperature", value="70 °F", delta="1.2 °F") #Dades bàsiques (com una icona del Power BI)
col1, col2, col3 = st.columns(3) #El mateix posant varies seguides
col1.metric("Time", "70 °F", "1.2 °F")
col2.metric("Gols", "9 mph", "8%")
col3.metric("Saves", "86%", "4%")

# CONCEPTES BÀSICS FI

