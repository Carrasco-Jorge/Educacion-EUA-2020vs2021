import pandas as pd
import streamlit as st

def extraer_y_transformar_datos_educacion():
    datos = pd.read_csv("datos\\Educationv.csv")

    # Renombrar columnas a español
    datos.rename(columns={
        "Year": "anio",
        "cd": "dist_congresual",
        "Bachelors_degree_or_higher": "edu_superior",
        "high_school_or_some_degree": "edu_media_superior",
        "Less_than_high_school_graduate": "menos_de_edu_media_superior"
    }, inplace=True)
    # Cambiar tipo de dato de "dist_congresual" a string
    datos["dist_congresual"] = datos["dist_congresual"].astype("string")
    # Crear columna para codigo de estado
    datos["estado"] = datos["dist_congresual"].str.split("_",expand=True).rename(columns={1:"estado"})["estado"]

    # Quitar Puerto Rico del conjunto de datos
    datos = datos[datos["estado"]!="PR"]

    return datos

def calcular_porcentajes(columna, datos):
    # Calcula el porcentaje del nivel educativo indicado en 'columna'
    return round(100 * datos[columna]/(datos["edu_superior"] + datos["edu_media_superior"] + datos["menos_de_edu_media_superior"]), 2)

def agregar_datos_por_estado(datos):
    # Crear tabla agregada por estados y con columnas:
    # # ["estado","anio","edu_superior","edu_media_superior","menos_de_edu_media_superior"]
    datos_por_estado = datos.groupby(by=["estado","anio"]).sum()[["edu_superior","edu_media_superior","menos_de_edu_media_superior"]].reset_index()
    # Calcular proporciones de nivel educativo por estado por año
    datos_por_estado["edu_superior_%"] = calcular_porcentajes("edu_superior", datos_por_estado)
    datos_por_estado["edu_media_superior_%"] = calcular_porcentajes("edu_media_superior", datos_por_estado)
    datos_por_estado["menos_de_edu_media_superior_%"] = calcular_porcentajes("menos_de_edu_media_superior", datos_por_estado)
    # Crear columna con nombre de estado
    nombres_estados = pd.read_csv("datos\\Nombres_estados.csv",index_col="codigo")
    datos_por_estado["nombre_estado"] = datos_por_estado["estado"].map(lambda estado: nombres_estados.loc[estado]["nombre"])

    return datos_por_estado

@st.cache_data
def etl_datos():
    # Extraer, transformar y cargar datos para dashboard
    datos = extraer_y_transformar_datos_educacion()
    datos_por_estado = agregar_datos_por_estado(datos)

    return datos_por_estado