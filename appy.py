#Inicie cargando streamlit desde la terminal de vs (no sabia que tenia una) y ahora la importo
import streamlit as st
import plotly.express as px
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

col11 , col12 = st.columns(2)

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

    # Filtramos el df pidiendo que nos agrupe en grupos las columnas de tool used y impact on grades pido que cuente los valores y que normalice que es lo que me falto
    anli_IAC = df_1.groupby("AI_Tool_Used")["Impact_on_Grades"].value_counts(normalize=True)

    # Las convertimos en columnas para la grafica
    anli_IAC = anli_IAC.unstack()

    #Falto normalizar
    #Listo, solo cambie de 
    #ali_IAC = df_1.groupby(["AI_Tool_Used", "Impact_on_Grades"]).size() a anli_IAC = df_1.groupby("AI_Tool_Used")["Impact_on_Grades"].value_counts(normalize=True) eso

    # Graficamos
    #Cambie las graficas a estas, 
    #Aca le decimos cual es la info que graficara y cual tipo sera
    fig = px.bar(anli_IAC, 
             #Aca le pedimos que apile las graficas   
             barmode="stack",
             #Su titulo 
             title="Impacto en Notas por Herramienta",
             #Le pone nombres a los ejes
             labels={"value": "Cantidad de estudiantes", "AI_Tool_Used": "Herramienta"})

    st.plotly_chart(fig, use_container_width=True)

#Listo ahora va 2do commit (o primer commit de modificaciones al code)
#parte 2
with col12 :
    st.header("Comparativa de Propositos")
     #Igual hacemos lo mismo, pero ahora nos pide st.radio que nos ayudara a seleccionar los usos que les dan que queremos ver para poder compara entre estos
    #Le pido que de la instruccion y que me de las opciones para las compatarivas
    prop_opc = st.radio("Selecciona un propósito:", ["Coding", "Writing", "Research", "Learning", "Homework"])
    #Fragmentamos el df para que solo nos de la col de proposito y que unicamente tome los valores de la opcion que seleccionemos
    df_2 = df[df["Purpose"] == prop_opc]
    #Aca hacemos un conteo, de el impacto en las notas (+, - o nada) en base al df fragmentadi
    conteo_prop = df_2["Impact_on_Grades"].value_counts()

    #Y eso lo graficamos
    
    fig = px.bar(conteo_prop,
             title=f"Impacto en Notas — {prop_opc}",
             labels={"value": "Cantidad de estudiantes", "index": "Impacto"})

    st.plotly_chart(fig, use_container_width=True)
#Ahora va el 2do commit Nota, accidentalmente a la hora de subirlo a mi tukey le di enter con la misma descripcion al comit :,c asi q saldra lo mismo


#Parte 3
#Nota cambie mis graficas a la libreria de streamlit por q son mas dinamicas

st.header("Analisis de Anomalias")
#Esto es para el deslizador , le ponemos el titulo o mas bien indicacion 
#La variable es para usarla en el filtro de mas tarde
horas = st.slider("Filtra por horas de uso diario:",
                  #El minimo para el deslizador tomamos flotantes (por q algunas horas las toma en decimales) 
                  min_value=float(df["Daily_Usage_Hours"].min()), 
                                    #Tomamos del df la columna de Daily_Usage_Hours sacandole el minimo para que ese sea nuestro minimo del deslizador
                  max_value=float(df["Daily_Usage_Hours"].max()),
                            #Igual con este pero este sera para el maximo 
                  value=float(df["Daily_Usage_Hours"].mean()))
                    #Este es para el primer valor que veremos al iniciar el programa, que en este caso lo quise poner en medio

#esro lo recicle para obtener el df en la parte que nos intereza que es que el nivel de satisfaccion sea alto y que el impacto en las notas sea bajo
Pareducir3 = (df['Satisfaction_Level'] == 'High') & (df['Impact_on_Grades'] == 'Slight Decline') & (df['Daily_Usage_Hours'] <= horas)
dfsat_dec = df[Pareducir3]   #Gruardamos eso en una variable                                      #Ese es para el filtro que añaciremos ya que debe contar solo los que tengan horas menores o iguales a las que determinara nuestro deslizador

#Esto es para que escriba en el dashboard cuantos estudiantes son los que cumplen con los filtros
st.write(f"Total de estudiantes: {len(dfsat_dec)}")#el f va por que dentro de nuestro texto va a llevar una funcion o codigo a ejecutar
                                #Y le pedimos que cuente desde nuestro df de satisfaccion que estara ya filtrado
#esto es para que muestre el data frame, pero solo mostrara nivel de satisfaccion, imacto e ia usada ya que los demas datos sobran para lo solicitado
st.dataframe(dfsat_dec[['Satisfaction_Level', 'Impact_on_Grades', 'AI_Tool_Used', 'Daily_Usage_Hours']], use_container_width=True)

#Listo va otro commit

#Parte 4
col41 , col52 = st.columns(2)
with col41 :
    st.header("Demografia y Uso")

    #Estos son los checkbox, en estos decimos que marcara al darle click
    por_genero = st.checkbox("Desglosar por Género")
    por_nivel = st.checkbox("Desglosar por Nivel Educativo")
    #Hacemos variables de los checkbox para luego usarlas en la particion del df

    #esto es para que se vea la grafica unicamente si se eligio una opc
    if por_genero or por_nivel:
    # Decides el groupby según los checkboxes
        if por_genero and por_nivel:
            #si se escojen las 2 a la vex entondes se toman las 2 columnas
            grupo = ["Gender", "Education_Level"]
        elif por_genero:
            #Si solo es por genero solo tomamos esa columna
            grupo = ["Gender"]
        elif por_nivel:
            #Si es por nivel ed, solo tomamos esa
            grupo = ["Education_Level"]
        #Aca hacemos otro df que agrupe las variables de grupo (que estan en el if para guardar lo que de eligio)
        df_4 = df.groupby(grupo)["Daily_Usage_Hours"].mean().reset_index()
                                #De ese grupo toma la col de horas de uso, calcula su promedio con .mean y asi mismo convierte el resultado en col con reset_index ya que al hacerlos sin eso nos marca error por manejar un indice para graficar
        #Graficamos
        fig = px.bar(df_4, 
            #Aqui es para cambiarle los colores por grupo ya que si no no se notan en la grafica
             x=grupo[0], #Toma el 1er grupo de lo solicitado
             y="Daily_Usage_Hours",#en el eje y tenemos uso de horas
             color=grupo[-1],#Para cambiar el color en caso de que sean genero y nivel ed, tambien lo cambia en genero y nivel
             title="Promedio de Horas de Uso",
             labels={"Daily_Usage_Hours": "Horas promedio"})
        st.plotly_chart(fig, use_container_width=True)

    #esto es para que si no tenemos seleccionado nada no muestre grafica 
    else:
        st.write("Seleccione al menos una opcion para ver la grafica ")
    
#Listo va nuestro penultimo commit

#listo la ultima parte
with col52 :
    st.header("Rendimiento Regional ")
    #de aca sacamos las op de ciudad aplicando un unique para las ciudades unicas y hago una lista con tolist ya que el multiselect solo funciona con listas
    ciudades_ops = df["City"].unique().tolist()
    #Aca aplicamos el multiselect y le ponemos una variable para poder determinar que poner en cada opc
    ciudades_sel = st.multiselect("Selecciona ciudades para comparar:", 
                                ciudades_ops, 
                                default=ciudades_ops)

    if ciudades_sel:
        #Aca si hay algo seleccionado en nuestra variable del multiseclect
        #hacemos un df filtrando la columna ciudad que sea la del selector
        df_5 = df[df["City"].isin(ciudades_sel)]
        
        #para el total de estudiantes tomando en cuenta las col de ciudad e impacto en notas
        total_ciudad = df_5.groupby("City")["Impact_on_Grades"].count()
        #Aca compara nuestro df para contar las notas mejoradas, si si estan mejoradas aplica un groupby y cuentasolo los que mejoraron
        mejora_ciudad = df_5[df_5["Impact_on_Grades"] == "Improved"].groupby("City")["Impact_on_Grades"].count()
        #Para sacar el porcentaje de mejora
        porCity = (mejora_ciudad / total_ciudad * 100).round(2).reset_index()#Igual para graficar hacemos unreset para hacerlo columna

        #Le ponemos nombres a las graficas para qye se vean bonitas
        porCity.columns = ["City", "% Notas Mejoradas"]
        #graficamos
        fig = px.bar(porCity, x="City", y="% Notas Mejoradas",
                    title="% de Notas Mejoradas por Ciudad",
                    labels={"City": "Ciudad"},
                    range_y=[0, 100])

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.write("Selecciona al menos una ciudad para ver la gráfica")

#Listooooooo el ultimo commit






