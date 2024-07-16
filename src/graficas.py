import plotly.graph_objects as go
import plotly.express as px
from .query import obtener_nombre_estado

def grafica_pastel_niveles_educacion(datos, region:str, anio:int):
    # Obtener lista con nombres de estados incluidos
    # en "region"
    estado = region
    if region == "EUA":
        region = list(datos["estado"].unique())
        estado = "EUA"
    else:
        estado = obtener_nombre_estado(estado)
    region = region if isinstance(region,list) else [region]

    # Filtrar datos por region indicada
    datos_filtrados = datos[
        (datos["anio"]==anio) & (datos["estado"].isin(region))
    ]

    # Obtener proporciones de niveles educativos
    # en region indicada
    proporciones = datos_filtrados[[
        "edu_superior",
        "edu_media_superior",
        "menos_de_edu_media_superior"
    ]].sum()
    
    # Definir nombres para etiquetas de gráfica
    nombres = [
        "Educación superior",
        "Educación media superior",
        "Menos de edu. media superior"
    ]

    # Crear gráfica de pastel
    fig = go.Figure(data=[go.Pie(labels=nombres, values=proporciones, hole=.6)])

    # Configurar gráfica
    fig.update_layout(
        height=90,
        margin=go.layout.Margin(
        l=0, # margen izq
        r=0, # margen der
        b=0, # margen inf
        t=0  # margen sup
        ),
        annotations=[dict(text=anio, x=0.5, y=0.5, font_size=20, showarrow=False, font_color="black")]
    )

    return fig, proporciones, datos_filtrados

def mapa(datos, columna, anio):
    # Filtrar datos por año
    datos = datos[datos["anio"]==anio]

    # Crear gráfico de mapa EUA
    fig = go.Figure(data=go.Choropleth(
        locations=datos['estado'], # Seleccionar todos los estados de EUA
        z = datos[columna].astype(float), # Datos que indicarán el color
        locationmode = 'USA-states', # Seleccionar estados de EUA para mapear "locations"
        colorscale = 'rdylbu', # Definir paleta de colores
        colorbar_title = "% de población", # Título de barra de colores
        marker_line_color="white", # Color de bordes del mapa
        hovertext=datos["nombre_estado"] + "<br>" + round(datos[columna],2).astype(str) + "%", # Datos en "hover"
        hoverinfo="text" # Solo mostrar la info indicada en "hover"
    ))

    # Configurar gráfica
    fig.update_layout(
        geo_scope='usa', # limitar mapa a EUA
        margin=go.layout.Margin(
        l=0, # margen izq
        r=0, # margen der
        b=0, # margen inf
        t=0  # margen sup
        ),
        height=250
    )

    return fig

def grafica_barras_top10(datos, columna, anio, titulo):
    # Ordenar y filtrar datos por columna seleccionada
    ordenar = False
    if "Bottom 10" in titulo:
        ordenar = True
    valor_max = datos[columna].max()
    datos = datos[datos["anio"]==anio].sort_values(by=columna,ascending=ordenar)\
        .head(10).sort_values(by=columna,ascending=not ordenar)

    # Crear gráfica de barras
    fig = go.Figure(data=go.Bar(
        x=datos[columna],
        y=datos["nombre_estado"],
        orientation='h'
    ))
    
    # Configurar gráfica
    fig.update_layout(
        title=titulo,
        margin=go.layout.Margin(
        l=0, # margen izq
        r=0, # margen der
        b=0, # margen inf
        t=65  # margen sup
        ),
        height=260,
        xaxis_range=[0,valor_max],
        xaxis = dict(
            dtick=valor_max//6,
            tickfont=dict(color="#5c5c5c"),
            showline=True
        ),
        yaxis=dict(
            tickfont=dict(color="#5c5c5c")
        )
    )

    return fig