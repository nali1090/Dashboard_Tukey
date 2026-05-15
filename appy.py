#Inicie cargando streamlit desde la terminal de vs (no sabia que tenia una) y ahora la importo
import streamlit as st
from PIL import Image

#Inicio mi prueba añadiendo un titulo 

#st.title("Mi Dashboard Interactivo") lo decorere mas, fuente http://medium.com/@verinamk/streamlit-for-beginners-build-your-first-dashboard-58b764a62a2d
# Para correrlo : streamlit run app.py lo guardo
# streamlit page config
st.set_page_config(
    page_title="Dashboard Interactivo",  # the page title shown in the browser tab
    page_icon=":bar_chart: ", # Para el iconito escoji mejor una bombilla y uno de un coso de tiro en el centro
    layout="wide",  # page layout : use the entire screen
)
# add page title
st.title(":dart: My Dashboard Interactivo :bar_chart:")

#Aca va un encabezado y el contexto del dataset 
st.header("About the Dataset")
st.write(""" Este dataset (https://www.kaggle.com/datasets/guriya79/how-ai-is-changing-student-life) 
        explora cómo la inteligencia artificial está transformando la vida estudiantil, enfocándose en 
        hábitos de estudio, rendimiento académico y satisfacción general. Muestra cómo los estudiantes 
        interactúan con herramientas de IA en su rutina diaria de aprendizaje y cómo estas herramientas 
        influyen en sus resultados.
        El dataset destaca patrones de uso del mundo real y revela tanto los beneficios como los posibles 
        efectos negativos de adoptar IA en la educación. """)
#Para añadir una imagen
N_image = Image.open("imagen_N.png")
#esto es para centrarlo, pedimos que divida el dashboard en columnas
col1, col2, col3 = st.columns([1, 2, 1])
#y que en la 2da añada mi imagen, alo mejor uso lo de las columnas mas tarde
with col2:
    st.image(N_image)



