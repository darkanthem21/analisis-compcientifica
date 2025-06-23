import dash_bootstrap_components as dbc
from dash import html, dcc

def create_header():
    """Crea el header del dashboard con diseño mejorado y colores accesibles"""
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                # Título principal con gradiente y mejor contraste
                html.Div([
                    html.H1([
                        html.I(className="fas fa-wind me-3", style={'color': '#27AE60'}),
                        "Dashboard Interactivo Calidad del Aire en Chile"
                    ], className="text-center mb-4", style={'color': '#fff', 'fontWeight': 700, 'textShadow': '1px 2px 8px #2C3E50'}),
                    html.P(
                        "Análisis integral de contaminación atmosférica, fuentes de emisión y correlaciones ambientales",
                        className="text-center lead mb-4",
                        style={'color': '#e0e0e0'}
                    )
                ], style={
                    'background': 'linear-gradient(135deg, #2C3E50 0%, #3498DB 100%)',
                    'padding': '40px 20px',
                    'borderRadius': '15px',
                    'marginBottom': '20px',
                    'boxShadow': '0 10px 30px rgba(44,62,80,0.25)'
                }),

                # Navegación mejorada con efectos y colores accesibles
                dbc.Row([
                    dbc.Col([
                        dbc.ButtonGroup([
                            dbc.Button([
                                html.I(className="fas fa-map-marked-alt me-2"),
                                "Estaciones de Monitoreo"
                            ], id="btn-stations", color="primary",
                               className="btn-nav me-2", n_clicks=1, active=True,
                               style={'borderRadius': '25px', 'padding': '12px 24px', 'fontWeight': 500, 'fontSize': '1.1rem'}),

                            dbc.Button([
                                html.I(className="fas fa-industry me-2"),
                                "Fuentes de Contaminación"
                            ], id="btn-sources", color="secondary",
                               className="btn-nav me-2", n_clicks=0,
                               style={'borderRadius': '25px', 'padding': '12px 24px', 'fontWeight': 500, 'fontSize': '1.1rem'}),

                            dbc.Button([
                                html.I(className="fas fa-chart-line me-2"),
                                "Análisis de Correlación"
                            ], id="btn-correlation", color="success",
                               className="btn-nav", n_clicks=0,
                               style={'borderRadius': '25px', 'padding': '12px 24px', 'fontWeight': 500, 'fontSize': '1.1rem'})
                        ], size="lg", className="d-flex justify-content-center")
                    ], className="text-center mb-4")
                ])
            ])
        ])
    ], fluid=True, className="mb-4")

def create_date_filters():
    """Crea filtros de fecha mejorados y con mejor contraste"""
    return dbc.Card([
        dbc.CardHeader([
            html.H5([
                html.I(className="fas fa-calendar-alt me-2"),
                "Filtros Temporales"
            ], className="mb-0", style={'color': '#2C3E50'})
        ], style={'backgroundColor': '#F8F9FA'}),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Label("📅 Desde:", className="fw-bold", style={'color': '#2C3E50'}),
                    dcc.Input(
                        id="date-from",
                        type="number",
                        placeholder="Año inicial",
                        value=2019,
                        min=2019,
                        max=2023,
                        className="form-control",
                        style={'backgroundColor': '#fff', 'borderColor': '#3498DB', 'color': '#2C3E50'}
                    )
                ], width=6),
                dbc.Col([
                    dbc.Label("📅 Hasta:", className="fw-bold", style={'color': '#2C3E50'}),
                    dcc.Input(
                        id="date-to",
                        type="number",
                        placeholder="Año final",
                        value=2023,
                        min=2019,
                        max=2023,
                        className="form-control",
                        style={'backgroundColor': '#fff', 'borderColor': '#3498DB', 'color': '#2C3E50'}
                    )
                ], width=6)
            ])
        ])
    ], className="mb-4", color="light", outline=True, style={'boxShadow': '0 2px 8px rgba(44,62,80,0.08)', 'borderRadius': '10px'})

def create_region_info_cards():
    """Crea tarjetas de información regional mejoradas y accesibles"""
    return dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.I(className="fas fa-users me-2", style={'color': '#fff'}),
                    html.Strong("Población Regional")
                ], className="text-center", style={'backgroundColor': '#3498DB', 'color': '#fff', 'fontWeight': 600, 'fontSize': '1.1rem', 'borderTopLeftRadius': '10px', 'borderTopRightRadius': '10px'}),
                dbc.CardBody([
                    html.H3(id="population-percentage", className="text-center mb-2", children="--", style={'color': '#3498DB', 'fontWeight': 700}),
                    html.P("% respecto al total nacional", className="text-center text-muted small mb-0")
                ])
            ], style={'border': '2px solid #3498DB', 'boxShadow': '0 2px 8px rgba(44,62,80,0.08)', 'borderRadius': '10px'})
        ], width=4),

        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.I(className="fas fa-smog me-2", style={'color': '#fff'}),
                    html.Strong("Emisiones Totales")
                ], className="text-center", style={'backgroundColor': '#F39C12', 'color': '#fff', 'fontWeight': 600, 'fontSize': '1.1rem', 'borderTopLeftRadius': '10px', 'borderTopRightRadius': '10px'}),
                dbc.CardBody([
                    html.H3(id="emissions-percentage", className="text-center mb-2", children="--", style={'color': '#F39C12', 'fontWeight': 700}),
                    html.P("% respecto al total nacional", className="text-center text-muted small mb-0")
                ])
            ], style={'border': '2px solid #F39C12', 'boxShadow': '0 2px 8px rgba(44,62,80,0.08)', 'borderRadius': '10px'})
        ], width=4),

        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.I(className="fas fa-lightbulb me-2", style={'color': '#fff'}),
                    html.Strong("Evaluación")
                ], className="text-center", style={'backgroundColor': '#27AE60', 'color': '#fff', 'fontWeight': 600, 'fontSize': '1.1rem', 'borderTopLeftRadius': '10px', 'borderTopRightRadius': '10px'}),
                dbc.CardBody([
                    html.Div(id="regional-conclusion", className="text-center",
                            style={'minHeight': '60px', 'color': '#27AE60', 'fontWeight': 700})
                ])
            ], style={'border': '2px solid #27AE60', 'boxShadow': '0 2px 8px rgba(44,62,80,0.08)', 'borderRadius': '10px'})
        ], width=4)
    ], className="mb-4", style={'marginTop': '0'})

def create_enhanced_aqi_legend():
    """Crea leyenda AQI compacta y minimalista"""
    return dbc.Card([
        dbc.CardBody([
            html.H6([
                html.I(className="fas fa-wind me-2"),
                "ICA"
            ], className="text-center mb-3", style={'color': '#2C3E50', 'fontWeight': '600'}),

            # Escala visual compacta
            html.Div([
                # Barra de color gradiente
                html.Div(style={
                    'height': '20px',
                    'background': 'linear-gradient(to right, #00E400 0%, #FFFF00 20%, #FF7E00 40%, #FF0000 60%, #8F3F97 80%, #7E0023 100%)',
                    'borderRadius': '10px',
                    'marginBottom': '15px',
                    'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
                }),

                # Indicadores compactos
                html.Div([
                    html.Div([
                        html.Div(style={
                            'width': '12px',
                            'height': '12px',
                            'backgroundColor': '#00E400',
                            'borderRadius': '50%',
                            'display': 'inline-block',
                            'marginRight': '8px'
                        }),
                        html.Span("Excelente", style={'fontSize': '12px', 'color': '#2C3E50'}),
                        html.Div("0-12", className="text-muted", style={'fontSize': '10px', 'marginLeft': '20px'})
                    ], className="mb-2"),

                    html.Div([
                        html.Div(style={
                            'width': '12px',
                            'height': '12px',
                            'backgroundColor': '#FFFF00',
                            'borderRadius': '50%',
                            'display': 'inline-block',
                            'marginRight': '8px'
                        }),
                        html.Span("Bueno", style={'fontSize': '12px', 'color': '#2C3E50'}),
                        html.Div("12-35", className="text-muted", style={'fontSize': '10px', 'marginLeft': '20px'})
                    ], className="mb-2"),

                    html.Div([
                        html.Div(style={
                            'width': '12px',
                            'height': '12px',
                            'backgroundColor': '#FF7E00',
                            'borderRadius': '50%',
                            'display': 'inline-block',
                            'marginRight': '8px'
                        }),
                        html.Span("Moderado", style={'fontSize': '12px', 'color': '#2C3E50'}),
                        html.Div("35-55", className="text-muted", style={'fontSize': '10px', 'marginLeft': '20px'})
                    ], className="mb-2"),

                    html.Div([
                        html.Div(style={
                            'width': '12px',
                            'height': '12px',
                            'backgroundColor': '#FF0000',
                            'borderRadius': '50%',
                            'display': 'inline-block',
                            'marginRight': '8px'
                        }),
                        html.Span("Insalubre", style={'fontSize': '12px', 'color': '#2C3E50'}),
                        html.Div("55-150", className="text-muted", style={'fontSize': '10px', 'marginLeft': '20px'})
                    ], className="mb-2"),

                    html.Div([
                        html.Div(style={
                            'width': '12px',
                            'height': '12px',
                            'backgroundColor': '#8F3F97',
                            'borderRadius': '50%',
                            'display': 'inline-block',
                            'marginRight': '8px'
                        }),
                        html.Span("Muy insalubre", style={'fontSize': '12px', 'color': '#2C3E50'}),
                        html.Div("150-250", className="text-muted", style={'fontSize': '10px', 'marginLeft': '20px'})
                    ], className="mb-2"),

                    html.Div([
                        html.Div(style={
                            'width': '12px',
                            'height': '12px',
                            'backgroundColor': '#7E0023',
                            'borderRadius': '50%',
                            'display': 'inline-block',
                            'marginRight': '8px'
                        }),
                        html.Span("Peligroso", style={'fontSize': '12px', 'color': '#2C3E50'}),
                        html.Div("250+", className="text-muted", style={'fontSize': '10px', 'marginLeft': '20px'})
                    ])
                ])
            ]),

            html.Hr(className="my-3"),
            html.P("μg/m³", className="text-center text-muted", style={'fontSize': '11px', 'marginBottom': '0'})
        ], className="p-3")
    ], style={
        'boxShadow': '0 2px 8px rgba(0,0,0,0.08)',
        'borderRadius': '12px',
        'border': '1px solid #e1e5ed',
        'backgroundColor': '#ffffff'
    })

def create_aqi_legend():
    """Versión simplificada de la leyenda AQI para compatibilidad"""
    return create_enhanced_aqi_legend()

def create_stations_tab():
    """Crea el contenido de la pestaña de estaciones con diseño mejorado y colores accesibles"""
    return [
        # Banner informativo
        dbc.Alert([
            html.H4([
                html.I(className="fas fa-info-circle me-2", style={'color': '#3498DB'}),
                "Análisis de Estaciones de Monitoreo"
            ], className="alert-heading"),
            html.P("Explore la calidad del aire a través de Chile mediante estaciones de monitoreo. "
                   "Seleccione una región en el mapa para ver datos detallados y análisis temporal.",
                   className="mb-0")
        ], color="info", className="mb-4", style={'backgroundColor': '#eaf6fb', 'color': '#2C3E50', 'borderColor': '#3498DB'}),

        create_date_filters(),

        # Contenido principal
        dbc.Row([
            # Panel izquierdo - Mapa
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5([
                            html.I(className="fas fa-map me-2", style={'color': '#2C3E50'}),
                            "Mapa Interactivo de Chile"
                        ], className="mb-0", style={'color': '#2C3E50'})
                    ], style={'backgroundColor': '#F8F9FA'}),
                    dbc.CardBody([
                        dcc.Graph(id="chile-map", style={'height': '650px'})
                    ], className="p-0")
                ], style={'boxShadow': '0 4px 12px rgba(44,62,80,0.10)', 'borderRadius': '12px'})
            ], width=5),

            # Panel derecho - Información y análisis
            dbc.Col([
                # Información de la región seleccionada
                dbc.Card([
                    dbc.CardHeader([
                        html.H5([
                            html.I(className="fas fa-chart-area me-2", style={'color': '#3498DB'}),
                            "Datos Región Seleccionada"
                        ], className="mb-0", style={'color': '#2C3E50'})
                    ], style={'backgroundColor': '#F8F9FA'}),
                    dbc.CardBody([
                        create_region_info_cards(),
                        html.Div(id="info-text", children=[
                            dbc.Alert([
                                html.I(className="fas fa-mouse-pointer me-2", style={'color': '#F39C12'}),
                                "Haga clic en una región del mapa para ver información detallada."
                            ], color="light", className="text-center", style={'backgroundColor': '#fffbe6', 'color': '#2C3E50', 'borderColor': '#F39C12'})
                        ])
                    ])
                ], className="mb-4", style={'boxShadow': '0 4px 12px rgba(44,62,80,0.10)', 'borderRadius': '12px'}),

                # Análisis temporal
                dbc.Card([
                    dbc.CardHeader([
                        html.H5([
                            html.I(className="fas fa-chart-line me-2", style={'color': '#27AE60'}),
                            "Análisis Temporal por Estación"
                        ], className="mb-0", style={'color': '#2C3E50'})
                    ], style={'backgroundColor': '#F8F9FA'}),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Seleccionar Estación:", className="fw-bold", style={'color': '#2C3E50'}),
                                dcc.Dropdown(
                                    id="station-dropdown",
                                    placeholder="Seleccione una estación de monitoreo",
                                    className="mb-3"
                                )
                            ])
                        ]),
                        dcc.Graph(id="temporal-chart", style={'height': '400px'})
                    ])
                ], style={'boxShadow': '0 4px 8px rgba(0,0,0,0.1)'})
            ], width=7)
        ])
    ]

def create_sources_tab():
    """Crea el contenido de la pestaña de fuentes con diseño mejorado y colores accesibles"""
    return [
        # Banner informativo
        dbc.Alert([
            html.H4([
                html.I(className="fas fa-industry me-2", style={'color': '#F39C12'}),
                "Análisis de Fuentes de Contaminación"
            ], className="alert-heading"),
            html.P("Explore las diferentes fuentes de emisiones contaminantes: Difusas (agricultura, erosión), "
                   "Puntuales (industrias, plantas) y En Ruta (transporte, vehículos).",
                   className="mb-0")
        ], color="warning", className="mb-4", style={'backgroundColor': '#fffbe6', 'color': '#2C3E50', 'borderColor': '#F39C12'}),

        # Controles mejorados
        dbc.Card([
            dbc.CardHeader([
                html.H5([
                    html.I(className="fas fa-sliders-h me-2", style={'color': '#2C3E50'}),
                    "Controles de Análisis"
                ], className="mb-0", style={'color': '#2C3E50'})
            ], style={'backgroundColor': '#F8F9FA'}),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Tipo de Análisis:", className="fw-bold", style={'color': '#2C3E50'}),
                        dcc.Dropdown(
                            id="sources-chart-type",
                            options=[
                                {'label': '📊 Análisis por Región', 'value': 'region'},
                                {'label': '🔄 Distribución por Tipo de Fuente', 'value': 'source_type'},
                                {'label': '📈 Evolución Temporal', 'value': 'temporal'}
                            ],
                            value='region',
                            className="mb-3"
                        )
                    ], width=6),
                    dbc.Col([
                        dbc.Label("Filtrar por Región:", className="fw-bold", style={'color': '#2C3E50'}),
                        dcc.Dropdown(
                            id="sources-region-filter",
                            placeholder="Todas las regiones",
                            className="mb-3"
                        )
                    ], width=6)
                ])
            ])
        ], className="mb-4", color="light", outline=True, style={'boxShadow': '0 2px 8px rgba(44,62,80,0.08)', 'borderRadius': '10px'}),

        # Área de análisis
        dbc.Row([
            # Gráfico principal
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5([
                            html.I(className="fas fa-chart-bar me-2", style={'color': '#3498DB'}),
                            "Visualización de Emisiones"
                        ], className="mb-0", style={'color': '#2C3E50'})
                    ], style={'backgroundColor': '#F8F9FA'}),
                    dbc.CardBody([
                        dcc.Graph(id="emissions-chart", style={'height': '500px'})
                    ], className="p-0")
                ], style={'boxShadow': '0 4px 12px rgba(44,62,80,0.10)', 'borderRadius': '12px'})
            ], width=8),

            # Panel de información
            dbc.Col([
                # Información sobre tipos de fuente
                dbc.Card([
                    dbc.CardHeader([
                        html.H6([
                            html.I(className="fas fa-info-circle me-2", style={'color': '#3498DB'}),
                            "Tipos de Fuentes"
                        ], className="mb-0", style={'color': '#2C3E50'})
                    ], style={'backgroundColor': '#F8F9FA'}),
                    dbc.CardBody([
                        html.Div([
                            html.H6([
                                html.I(className="fas fa-seedling me-2", style={'color': '#27AE60'}),
                                "Fuentes Difusas"
                            ], className="mb-2"),
                            html.P("Emisiones distribuidas en un área amplia. Incluyen agricultura, "
                                   "erosión del suelo, y emisiones vehiculares urbanas.",
                                   className="small mb-3"),

                            html.H6([
                                html.I(className="fas fa-industry me-2", style={'color': '#3498DB'}),
                                "Fuentes Puntuales (EFP)"
                            ], className="mb-2"),
                            html.P("Emisiones de establecimientos fijos. Incluyen industrias, "
                                   "plantas de energía y refinerías.",
                                   className="small mb-3"),

                            html.H6([
                                html.I(className="fas fa-truck me-2", style={'color': '#F39C12'}),
                                "Fuentes En Ruta (TR)"
                            ], className="mb-2"),
                            html.P("Emisiones del transporte en movimiento. Incluyen vehículos, "
                                   "transporte público y camiones.",
                                   className="small")
                        ])
                    ])
                ], className="mb-3", color="light", outline=True, style={'boxShadow': '0 2px 8px rgba(44,62,80,0.08)', 'borderRadius': '10px'}),

                # Estadísticas de emisiones
                dbc.Card([
                    dbc.CardHeader([
                        html.H6([
                            html.I(className="fas fa-chart-pie me-2", style={'color': '#27AE60'}),
                            "Estadísticas"
                        ], className="mb-0", style={'color': '#2C3E50'})
                    ], style={'backgroundColor': '#F8F9FA'}),
                    dbc.CardBody([
                        html.Div(id="emissions-stats", children=[
                            dbc.Alert([
                                html.I(className="fas fa-chart-bar me-2", style={'color': '#3498DB'}),
                                "Seleccione un análisis para ver estadísticas detalladas."
                            ], color="light", className="text-center small", style={'backgroundColor': '#eaf6fb', 'color': '#2C3E50', 'borderColor': '#3498DB'})
                        ])
                    ])
                ], color="info", outline=True, style={'boxShadow': '0 2px 8px rgba(44,62,80,0.08)', 'borderRadius': '10px'})
            ], width=4)
        ])
    ]

def create_correlation_tab():
    """Crea el contenido de la pestaña de correlación con diseño mejorado y colores accesibles"""
    return [
        # Banner informativo
        dbc.Alert([
            html.H4([
                html.I(className="fas fa-project-diagram me-2", style={'color': '#27AE60'}),
                "Análisis de Correlación"
            ], className="alert-heading"),
            html.P("Analice las correlaciones entre contaminación atmosférica, población, "
                   "emisiones industriales y variables ambientales para identificar patrones y relaciones.",
                   className="mb-0")
        ], color="success", className="mb-4", style={'backgroundColor': '#eafbf3', 'color': '#2C3E50', 'borderColor': '#27AE60'}),

        # Controles de análisis mejorados
        dbc.Card([
            dbc.CardHeader([
                html.H5([
                    html.I(className="fas fa-cogs me-2", style={'color': '#2C3E50'}),
                    "Configuración del Análisis"
                ], className="mb-0", style={'color': '#2C3E50'})
            ], style={'backgroundColor': '#F8F9FA'}),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Tipo de Análisis:", className="fw-bold", style={'color': '#2C3E50'}),
                        dcc.Dropdown(
                            id="correlation-analysis-type",
                            options=[
                                {'label': '🔥 Matriz de Correlación General', 'value': 'heatmap'},
                                {'label': '👥 Población vs Contaminación', 'value': 'population_pollution'},
                                {'label': '🏭 Emisiones vs Calidad del Aire', 'value': 'emissions_air_quality'},
                                {'label': '📈 Análisis Temporal', 'value': 'temporal_correlation'}
                            ],
                            value='heatmap',
                            className="mb-3"
                        )
                    ], width=6),
                    dbc.Col([
                        dbc.Label("Variables a Incluir:", className="fw-bold", style={'color': '#2C3E50'}),
                        dcc.Dropdown(
                            id="correlation-variables",
                            options=[
                                {'label': 'PM2.5', 'value': 'pm25'},
                                {'label': 'PM10', 'value': 'pm10'},
                                {'label': 'O3', 'value': 'o3'},
                                {'label': 'NO2', 'value': 'no2'},
                                {'label': 'CO', 'value': 'co'},
                                {'label': 'SO2', 'value': 'so2'},
                                {'label': 'Población', 'value': 'poblacion'},
                                {'label': 'Emisiones', 'value': 'emisiones'}
                            ],
                            value=['pm25', 'pm10', 'poblacion', 'emisiones'],
                            multi=True,
                            className="mb-3"
                        )
                    ], width=6)
                ])
            ])
        ], className="mb-4", color="light", outline=True, style={'boxShadow': '0 2px 8px rgba(44,62,80,0.08)', 'borderRadius': '10px'}),

        # Área de gráficos de correlación
        dbc.Row([
            # Gráfico principal
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5([
                            html.I(className="fas fa-chart-area me-2", style={'color': '#3498DB'}),
                            "Visualización de Correlaciones"
                        ], className="mb-0", style={'color': '#2C3E50'})
                    ], style={'backgroundColor': '#F8F9FA'}),
                    dbc.CardBody([
                        dcc.Graph(id="correlation-chart", style={'height': '600px'})
                    ], className="p-0")
                ], style={'boxShadow': '0 4px 12px rgba(44,62,80,0.10)', 'borderRadius': '12px'})
            ], width=8),

            # Panel de información
            dbc.Col([
                # Interpretación de correlaciones
                dbc.Card([
                    dbc.CardHeader([
                        html.H6([
                            html.I(className="fas fa-lightbulb me-2", style={'color': '#27AE60'}),
                            "Interpretación"
                        ], className="mb-0", style={'color': '#2C3E50'})
                    ], style={'backgroundColor': '#F8F9FA'}),
                    dbc.CardBody([
                        html.Div([
                            html.P([
                                html.I(className="fas fa-arrow-up me-2", style={'color': '#27AE60'}),
                                html.Strong("Correlación > 0.7:"),
                                " Fuerte correlación positiva"
                            ], className="small mb-2"),
                            html.P([
                                html.I(className="fas fa-minus me-2", style={'color': '#F39C12'}),
                                html.Strong("Correlación 0.3-0.7:"),
                                " Correlación moderada"
                            ], className="small mb-2"),
                            html.P([
                                html.I(className="fas fa-arrow-down me-2", style={'color': '#3498DB'}),
                                html.Strong("Correlación < 0.3:"),
                                " Correlación débil"
                            ], className="small mb-2"),
                            html.P([
                                html.I(className="fas fa-exchange-alt me-2", style={'color': '#E74C3C'}),
                                html.Strong("Correlación negativa:"),
                                " Relación inversa"
                            ], className="small mb-3"),
                            html.Hr(),
                            html.H6("📊 Estadísticas del Análisis", className="mb-2", style={'color': '#2C3E50'}),
                            html.Div(id="correlation-stats", children=[
                                dbc.Alert([
                                    html.I(className="fas fa-chart-line me-2", style={'color': '#3498DB'}),
                                    "Seleccione un tipo de análisis para ver estadísticas."
                                ], color="light", className="text-center small", style={'backgroundColor': '#eaf6fb', 'color': '#2C3E50', 'borderColor': '#3498DB'})
                            ])
                        ])
                    ])
                ], className="mb-3", color="light", outline=True, style={'boxShadow': '0 2px 8px rgba(44,62,80,0.08)', 'borderRadius': '10px'}),

                # Insights y conclusiones
                dbc.Card([
                    dbc.CardHeader([
                        html.H6([
                            html.I(className="fas fa-brain me-2", style={'color': '#27AE60'}),
                            "Insights Principales"
                        ], className="mb-0", style={'color': '#2C3E50'})
                    ], style={'backgroundColor': '#F8F9FA'}),
                    dbc.CardBody([
                        html.Div(id="correlation-insights", children=[
                            dbc.Alert([
                                html.I(className="fas fa-magic me-2", style={'color': '#F39C12'}),
                                "Los insights aparecerán aquí basados en el análisis seleccionado."
                            ], color="light", className="text-center small", style={'backgroundColor': '#fffbe6', 'color': '#2C3E50', 'borderColor': '#F39C12'})
                        ])
                    ])
                ], color="success", outline=True, style={'boxShadow': '0 2px 8px rgba(44,62,80,0.08)', 'borderRadius': '10px'})
            ], width=4)
        ])
    ]
