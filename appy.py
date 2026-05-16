#Inicie cargando streamlit desde la terminal de vs (no sabia que tenia una) y ahora la importo
import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

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
#Aca hice un commit

#Iniciamos con lo primero
#cargamos el df
#esto es pa cargarlo
df = pd.read_csv(r"AI_Student_Life_Pakistan_2026.csv")

#Aqui es pa ocultarlo si es q no lo queremos ver
with st.expander('Dataset'):
    df

col11 , col12 = st.columns([1,2])

with col11 :
    st.header("Análisis de Impacto")
    #Inicio a fragmentar el ds, esto es para el boton de seleccion solicitado, tomamos las columnas Impact_on_Grades y AI_Tool_Used
    #Aca estan las opciones, le pedimos que añada una general para poder ver todas las ciudades , que tambien necesitaremos su columna
    ciudades = ["Todas las ciudades"] + list(df["City"].unique())
                                        #Aca le pido que haga una lista unicamente de la columna City tomando solo los valores unicos
    #Ahora el seleccionador, este lo declaramos con selectbox y le ponemos como la instruccion de que debe
    #Seleccionar el usuario y le damos las variables
    ciudad_sel = st.selectbox("Selecciona una ciudad:", ciudades)
    #Aca es para que en caso de seleccionar todas tome todas las ciudades muestre la grafica general
    if ciudad_sel == "Todas las ciudades":
        df_1 = df
    else: #Sino hara un filtrado por ciudad, en base a la opcion elegida
        df_1 = df[df["City"] == ciudad_sel]

    # Filtramos el df pidiendo que nos agrupe en grupos las columnas de tool used y impact on grades y que nos de sus tamaños
    anli_IAC = df_1.groupby(["AI_Tool_Used", "Impact_on_Grades"]).size()

    # Las convertimos en columnas para la grafica
    anli_IAC = anli_IAC.unstack()

    # Graficamos
    #Esto es para pedirle que ponga las graficas apiladas y no por separado
    anli_IAC.plot(kind="bar", stacked=True)
    plt.xlabel("Herramienta")
    plt.ylabel("Cantidad de estudiantes") 

    st.pyplot(plt) #Para que muestre la grafica, si no solo existe, pero no aparece

#Listo ahora va 2do commit (o primer commit de modificaciones al code)
    



    



