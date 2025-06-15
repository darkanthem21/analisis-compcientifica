# dashboard_modules/layouts/tab1_monitoring_stations.py

from dash import dcc, html
import dash_bootstrap_components as dbc

def create_layout_tab1(lista_regiones, lista_años):
    """
    Crea el layout (la estructura visual) para la Pestaña 1.

    Args:
        lista_regiones (list): Una lista de las regiones para el filtro dropdown.
        lista_años (list): Una lista de los años para los filtros de fecha.

    Returns:
        dbc.Container: El layout de la pestaña.
    """
    return dbc.Container(
        [
            # Fila de Filtros Principales
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H5("Filtros Principales", className="mt-4"),
                            html.Label("Región:"),
                            dcc.Dropdown(
                                id='filtro-region-tab1',
                                options=[{'label': region, 'value': region} for region in lista_regiones],
                                value=lista_regiones[0] if lista_regiones else None, # Valor inicial
                                clearable=False
                            ),
                        ],
                        md=4 # Ocupa 4 de 12 columnas en pantallas medianas o más grandes
                    ),
                    dbc.Col(
                        [
                            html.Label("Desde (Año):"),
                            dcc.Dropdown(
                                id='filtro-año-desde-tab1',
                                options=[{'label': año, 'value': año} for año in lista_años],
                                value=lista_años[0] if lista_años else None,
                                clearable=False
                            ),
                        ],
                        md=2
                    ),
                    dbc.Col(
                        [
                            html.Label("Hasta (Año):"),
                            dcc.Dropdown(
                                id='filtro-año-hasta-tab1',
                                options=[{'label': año, 'value': año} for año in lista_años],
                                value=lista_años[-1] if lista_años else None,
                                clearable=False
                            ),
                        ],
                        md=2
                    ),
                ],
                className="mb-4" # Margin bottom
            ),

            html.Hr(), # Línea divisoria

            # Fila de Contenido Principal (KPIs y Gráfico)
            dbc.Row(
                [
                    # --- Panel Izquierdo: KPIs y Conclusión ---
                    dbc.Col(
                        [
                            html.H4("Datos de la Región Seleccionada", className="text-center"),
                            # Tarjetas de KPI
                            dbc.CardGroup(
                                [
                                    dbc.Card(
                                        dbc.CardBody([
                                            html.H6("Estaciones", className="card-title"),
                                            html.H3(id="kpi-cantidad-estaciones", className="card-text")
                                        ]), className="text-center"
                                    ),
                                    dbc.Card(
                                        dbc.CardBody([
                                            html.H6("% Población", className="card-title"),
                                            html.H3(id="kpi-poblacion-pct", className="card-text")
                                        ]), className="text-center"
                                    ),
                                    dbc.Card(
                                        dbc.CardBody([
                                            html.H6("% Permisos Circ.", className="card-title"),
                                            html.H3("N/A", id="kpi-permisos-pct", className="card-text") # Placeholder
                                        ]), className="text-center"
                                    ),
                                ]
                            ),
                            # Conclusión Regional
                            dbc.Card(
                                dbc.CardBody([
                                    html.H5("Conclusión Regional", className="card-title"),
                                    html.P(
                                        id="texto-conclusion-regional",
                                        children="Seleccione una región para ver la conclusión."
                                    )
                                ]), className="mt-4"
                            )
                        ],
                        md=4 # Ocupa 4 de 12 columnas
                    ),

                    # --- Panel Derecho: Gráfico por Estación ---
                    dbc.Col(
                        [
                            html.H4("Análisis por Estación de Monitoreo", className="text-center"),
                            # Filtros secundarios para estación y contaminante
                            dbc.Row([
                                dbc.Col([
                                    html.Label("Estación (Antena):"),
                                    dcc.Dropdown(id='filtro-estacion-tab1', disabled=True) # Se habilita con un callback
                                ], md=6),
                                dbc.Col([
                                    html.Label("Contaminante:"),
                                    dcc.Dropdown(
                                        id='filtro-contaminante-tab1',
                                        options=[
                                            {'label': 'MP2.5', 'value': 'pm25'},
                                            {'label': 'MP10', 'value': 'pm10'},
                                            {'label': 'CO', 'value': 'co'},
                                            {'label': 'NO2', 'value': 'no2'},
                                            {'label': 'SO2', 'value': 'so2'},
                                            {'label': 'O3', 'value': 'o3'},
                                        ],
                                        value='pm25' # Valor por defecto
                                    )
                                ], md=6)
                            ]),
                            # El Gráfico
                            dcc.Graph(
                                id='grafico-series-tiempo-estacion',
                                config={'displayModeBar': True} # Muestra la barra de herramientas de plotly
                            ),
                            # Espacio para el tooltip
                            html.P(
                                [
                                    "¿Cómo se mide esto? ",
                                    html.I(className="bi bi-info-circle-fill", id="tooltip-aqi-target", style={"cursor": "pointer"})
                                ],
                                className="text-end"
                            ),
                            dbc.Tooltip(
                                "Aquí se mostrará información sobre la tabla AQI y los riesgos de cada contaminante.",
                                target="tooltip-aqi-target",
                            )
                        ],
                        md=8 # Ocupa 8 de 12 columnas
                    )
                ]
            )
        ],
        fluid=True,
        className="dbc" # Clase para aplicar estilos de bootstrap si es necesario
    )
