import src.etl as etl
import src.graficas as gr
import src.query as q
import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Educación EUA",
    page_icon="img\\JC.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cargar datos
datos = etl.etl_datos()

# Barra lateral
with st.sidebar:

    st.title("Panorama de educación en EUA – 2020 y 2021")
    st.write("## Configuración")

    nombre_estado = st.selectbox(
        "Selecciona un estado",
        ["EUA"]+q.obtener_lista_nombres_estados()
    )
    estado = q.obtener_codigo_estado(nombre_estado)
    
    st.divider()
    
    anio = st.selectbox(
        "Selecciona un año",
        [2020,2021]
    )

    estadistica = st.selectbox(
        "Selecciona una estadística",
        [
            "% Educación superior","% Educación media superior",
            "% Menos de edu. media superior"
        ]
    )
    dicc_columnas = {
        "% Educación superior":"edu_superior_%",
        "% Educación media superior":"edu_media_superior_%",
        "% Menos de edu. media superior":"menos_de_edu_media_superior_%"
    }
    columna = dicc_columnas[estadistica]
    

# Dashboard
izquierda, derecha = st.columns([0.4,0.6])

# Estadisticas 2020 vs 2021 por estado
with izquierda:
    # Comparación 2020 vs 2021
    st.write(f"##### Nivel educativo en {nombre_estado} - 2020 vs 2021")

    fig, x, datos_filtrados = gr.grafica_pastel_niveles_educacion(datos, estado, 2020)
    st.plotly_chart(fig, use_container_width=True)

    fig, x, datos_filtrados = gr.grafica_pastel_niveles_educacion(datos, estado, 2021)
    st.plotly_chart(fig, use_container_width=True)

    # Métricas de aumento / cambio % de 2020 a 2021
    ## Educación superior
    sub1_col1, sub1_col2 = st.columns(2)
    with sub1_col1:
        st.info("##### Educación superior")
    with sub1_col2:
        metrica = q.obtener_cambio_porcentual_estado(datos, estado, "edu_superior_%")
        st.metric(
            "Cambio en puntos %",
            f"{metrica}%",
            "-" if metrica < 0 else "+"
        )
    
    ## Educación media superior
    sub2_col1, sub2_col2 = st.columns(2)
    with sub2_col1:
        st.info("##### Educación media superior")
    with sub2_col2:
        metrica = q.obtener_cambio_porcentual_estado(datos, estado, "edu_media_superior_%")
        st.metric(
            "Cambio en puntos %",
            f"{metrica}%",
            "-" if metrica < 0 else "+"
        )

    ## Menos de Educación media superior
    sub3_col1, sub3_col2 = st.columns(2)
    with sub3_col1:
        st.info("##### Menos de edu. media superior")
    with sub3_col2:
        metrica = q.obtener_cambio_porcentual_estado(datos, estado, "menos_de_edu_media_superior_%")
        st.metric(
            "Cambio en puntos %",
            f"{metrica}%",
            "-" if metrica < 0 else "+"
        )

# Comparacion entre estados por año y estadistica
with derecha:
    st.write(f"##### {estadistica} por estado")

    # Mapa por estadística seleccionada
    fig = gr.mapa(datos, columna, anio)
    st.plotly_chart(fig, use_container_width=True)

    # Top 10 y Bottom 10 de estadística seleccionada
    sub_col1, sub_col2 = st.columns(2)
    with sub_col1:
        fig = gr.grafica_barras_top10(datos, columna, anio, f"Top 10 estados <br> {estadistica}")
        st.plotly_chart(fig, use_container_width=True)
    with sub_col2:
        fig = gr.grafica_barras_top10(datos, columna, anio, f"Bottom 10 estados <br> {estadistica}")
        st.plotly_chart(fig, use_container_width=True)