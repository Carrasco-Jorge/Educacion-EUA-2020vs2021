import pandas as pd

def obtener_lista_nombres_estados():
    nombres_estados = pd.read_csv("datos\\Nombres_estados.csv",index_col="codigo").drop("PR")
    return list(nombres_estados["nombre"])

def obtener_nombre_estado(estado):
    nombres_estados = pd.read_csv("datos\\Nombres_estados.csv",index_col="codigo").drop("PR")
    return nombres_estados.loc[estado]["nombre"]

def obtener_codigo_estado(nombre):
    codigo = nombre

    if nombre != "EUA":
        nombres_estados = pd.read_csv("datos\\Nombres_estados.csv")
        nombres_estados = nombres_estados[nombres_estados["codigo"]!="PR"]
        codigo = (nombres_estados[nombres_estados["nombre"]==nombre])["codigo"].iloc[0]

    return codigo

def agregar_datos_2020vs2021(datos, estadistica):
    # Crear tabla con columnas:
    # ["nombre_estado","2020","2021","2021 vs 2020"]
    # con valores porcentuales de la estadístca indicada
    tabla = pd.pivot_table(
        datos, values=estadistica, index="nombre_estado",
        columns=["anio"], aggfunc="sum"
    )
    tabla["2021 vs 2020"] = tabla[2021]-tabla[2020]
    return tabla

def obtener_cambio_porcentual_estado(datos, region, estadistica):
    # Caso EUA
    if region=="EUA":
        valores = []

        for anio in [2020,2021]:
            # Agregar datos de todos los estados por año
            # y calcular porcentajes de estadistica indicada
            datos_anio = datos[datos["anio"]==anio]
            valores.append(100*datos_anio[
                estadistica[:-2]
            ].sum()/datos_anio.iloc[:,2:5].sum().sum())
        
        return round(valores[1] - valores[0],2)
    # Caso Estado
    tabla = agregar_datos_2020vs2021(datos, estadistica)
    region = obtener_nombre_estado(region)

    cambio_porcentual = round(tabla["2021 vs 2020"], 2).loc[region]
    return cambio_porcentual