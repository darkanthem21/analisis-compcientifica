import os
import sys
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import dash
from dash import dcc, html, Input, Output, State, callback_context
import dash_bootstrap_components as dbc

# ===== TEMA Y ESTILOS PERSONALIZADOS =====

CUSTOM_THEME = {
    'primary': '#2C3E50',   # Azul oscuro para elementos principales
    'secondary': '#3498DB', # Azul claro para elementos secundarios
    'success': '#27AE60',   # Verde para elementos positivos
    'warning': '#F39C12',   # Naranja para advertencias
    'danger': '#E74C3C',    # Rojo para errores
    'background': '#F8F9FA' # Fondo claro para mejor legibilidad
}

CUSTOM_STYLES = {
    'card': {
        'box-shadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
        'border-radius': '8px',
        'margin-bottom': '20px',
        'background-color': 'white'
    },
    'header': {
        'background-color': CUSTOM_THEME['primary'],
        'color': 'white',
        'padding': '20px 0',
        'margin-bottom': '30px',
        'border-radius': '0 0 10px 10px'
    },
    'tabs': {
        'margin-bottom': '20px'
    }
}

# Importar módulos locales
from components import create_header, create_stations_tab, create_sources_tab, create_correlation_tab
from charts import create_chile_map, create_temporal_chart
from callbacks import register_callbacks

# ===== CONFIGURACIÓN =====

# Configuración de rutas
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, 'data', 'processed')

# Mapeo de nombres de regiones
REGION_NAME_MAPPING = {
    'Arica': 'Arica y Parinacota',
    'Atacama': 'Atacama',
    'Aysen': 'Aysén',
    'Biobio': 'Biobío',
    'La Araucanía': 'Araucanía',
    'Los Lagos': 'Los Lagos',
    'Los Rios': 'Los Ríos',
    'Magallanes': 'Magallanes',
    'Maule': 'Maule',
    'Metropolitana': 'Metropolitana',
    "O'Higgins": "O'Higgins",
    'Tarapaca': 'Tarapacá',
    'Valparaiso': 'Valparaíso',
    'antofagasta': 'Antofagasta',
    'coquimbo': 'Coquimbo',
    'Ñuble': 'Ñuble',
}

# ===== FUNCIONES AUXILIARES =====

def normalize_region_name(name):
    """Normaliza nombres de regiones usando el mapeo definido"""
    if pd.isna(name):
        return ""
    name = str(name).strip()
    return REGION_NAME_MAPPING.get(name, name)

def load_data():
    """Carga todos los datasets procesados"""
    print("📂 Cargando datos procesados...")

    try:
        # Cargar datos de calidad del aire
        air_quality_path = os.path.join(DATA_DIR, 'air_quality_stations_processed.pkl')
        if os.path.exists(air_quality_path):
            df_air_quality = pd.read_pickle(air_quality_path)
            print(f"✅ Datos de calidad del aire: {df_air_quality.shape}")
        else:
            print("❌ No se encontraron datos de calidad del aire")
            df_air_quality = None

        # Cargar datos de emisiones
        emissions_path = os.path.join(DATA_DIR, 'emission_sources_processed.pkl')
        if os.path.exists(emissions_path):
            df_emissions = pd.read_pickle(emissions_path)
            print(f"✅ Datos de emisiones: {df_emissions.shape}")
        else:
            print("❌ No se encontraron datos de emisiones")
            df_emissions = None

        # Cargar datos de población
        population_path = os.path.join(DATA_DIR, 'population_processed.pkl')
        if os.path.exists(population_path):
            df_population = pd.read_pickle(population_path)
            print(f"✅ Datos de población: {df_population.shape}")
        else:
            print("❌ No se encontraron datos de población")
            df_population = None

        return df_air_quality, df_emissions, df_population

    except Exception as e:
        print(f"❌ Error cargando datos: {e}")
        return None, None, None

def process_data(df_air_quality, df_emissions, df_population):
    """Normaliza y procesa los datos cargados"""
    print("🔄 Procesando y normalizando datos...")

    # Normalizar regiones en datos de calidad del aire
    if df_air_quality is not None and 'region' in df_air_quality.columns:
        print("   Normalizando regiones en calidad del aire...")
        df_air_quality['region'] = df_air_quality['region'].apply(normalize_region_name)
        print(f"   Regiones únicas: {sorted(df_air_quality['region'].unique())}")

    # Normalizar regiones en datos de emisiones
    if df_emissions is not None and 'region' in df_emissions.columns:
        print("   Normalizando regiones en emisiones...")
        df_emissions['region'] = df_emissions['region'].apply(normalize_region_name)

    # Normalizar regiones en datos de población
    if df_population is not None and 'region' in df_population.columns:
        print("   Normalizando regiones en población...")
        df_population['region'] = df_population['region'].apply(normalize_region_name)

    return df_air_quality, df_emissions, df_population

def debug_region_matching(df_air_quality, df_emissions, df_population):
    """Muestra información de debug sobre el matching de regiones"""
    print("\n🔍 Debug - Matching de regiones:")

    regions_air = set()
    regions_emissions = set()
    regions_population = set()

    if df_air_quality is not None and 'region' in df_air_quality.columns:
        regions_air = set(df_air_quality['region'].dropna())
        print(f"   Calidad del aire: {len(regions_air)} regiones")

    if df_emissions is not None and 'region' in df_emissions.columns:
        regions_emissions = set(df_emissions['region'].dropna())
        print(f"   Emisiones: {len(regions_emissions)} regiones")

    if df_population is not None and 'region' in df_population.columns:
        regions_population = set(df_population['region'].dropna())
        print(f"   Población: {len(regions_population)} regiones")

    # Mostrar intersecciones
    all_regions = regions_air | regions_emissions | regions_population
    print(f"   Total regiones únicas: {len(all_regions)}")

    if regions_air and regions_emissions:
        common_air_emissions = regions_air & regions_emissions
        print(f"   Regiones comunes aire-emisiones: {len(common_air_emissions)}")

    if regions_air and regions_population:
        common_air_population = regions_air & regions_population
        print(f"   Regiones comunes aire-población: {len(common_air_population)}")

# ===== APLICACIÓN PRINCIPAL =====

def create_app_layout():
    """Crea el layout principal de la aplicación con leyenda AQI fija lateral"""
    from components import create_enhanced_aqi_legend

    return dbc.Container([
        # Header con navegación y estilos mejorados
        html.Div([
            create_header()
        ], style=CUSTOM_STYLES['header']),

        # Contenedor principal con fondo personalizado y leyenda AQI lateral
        dbc.Row([
            # Columna principal (contenido dinámico)
            dbc.Col([
                html.Div(id="tab-content", style={
                    'background-color': CUSTOM_THEME['background'],
                    'padding': '20px',
                    'border-radius': '10px',
                    'min-height': '500px'
                }),
            ], width=10, xs=12, sm=12, md=12, lg=10, xl=10),

            # Columna lateral derecha fija para la leyenda AQI (oculta en xs/sm)
            dbc.Col([
                html.Div(
                    create_enhanced_aqi_legend(),
                    id="aqi-legend-panel",
                    style={
                        'position': 'sticky',
                        'top': '90px',
                        'zIndex': 100,
                        'marginTop': '10px',
                        'marginBottom': '10px',
                        'display': 'block'
                    }
                )
            ], width=2, className="d-none d-lg-block d-xl-block")
        ], style={'padding': '20px 0'}),

        # Botón flotante para mostrar leyenda AQI en móviles/tablets
        html.Div([
            dbc.Button(
                [html.I(className="fas fa-wind me-2"), "Ver Índice AQI"],
                id="aqi-legend-fab",
                color="primary",
                style={
                    'position': 'fixed',
                    'bottom': '30px',
                    'right': '30px',
                    'zIndex': 2000,
                    'borderRadius': '50px',
                    'boxShadow': '0 4px 12px rgba(44,62,80,0.15)',
                    'display': 'none'
                },
                n_clicks=0
            ),
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Índice de Calidad del Aire (AQI)")),
                    dbc.ModalBody(create_enhanced_aqi_legend())
                ],
                id="aqi-legend-modal",
                is_open=False,
                centered=True,
                size="lg",
                backdrop=True
            )
        ], id="aqi-legend-mobile"),

        # Footer con información adicional
        html.Footer([
            html.Hr(),
            html.P("Dashboard de Calidad del Aire en Chile - Análisis Computacion Científica",
                   className="text-center text-muted")
        ], style={'margin-top': '30px'}),

        # Stores para datos compartidos
        dcc.Store(id='selected-region-data'),
        dcc.Store(id='active-tab', data='stations')
    ],
    fluid=True,
    style={'background-color': CUSTOM_THEME['background']})

def main():
    """Función principal que ejecuta el dashboard"""
    print("🌟 DASHBOARD INTERACTIVO - CALIDAD DEL AIRE EN CHILE")
    print("=" * 60)

    # Cargar y procesar datos
    df_air_quality, df_emissions, df_population = load_data()

    if any(df is not None for df in [df_air_quality, df_emissions, df_population]):
        df_air_quality, df_emissions, df_population = process_data(
            df_air_quality, df_emissions, df_population
        )
        debug_region_matching(df_air_quality, df_emissions, df_population)
    else:
        print("⚠️  No se pudieron cargar los datos. Ejecute los scripts ETL primero.")
        print("   1. python data_processing/etl_air_quality_stations.py")
        print("   2. python data_processing/etl_emission_sources.py")
        print("   3. python data_processing/etl_population.py")
        return

    # Crear aplicación Dash con tema mejorado
    app = dash.Dash(
        __name__,
        external_stylesheets=[
            dbc.themes.FLATLY,  # Tema más moderno y legible
            "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css",
            {
                'href': 'https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap',
                'rel': 'stylesheet'
            }
        ],
        meta_tags=[
            {'name': 'viewport',
             'content': 'width=device-width, initial-scale=1.0'}
        ]
    )

    # Agregar estilos CSS personalizados
    app.index_string = '''
    <!DOCTYPE html>
    <html>
        <head>
            {%metas%}
            <title>{%title%}</title>
            {%favicon%}
            {%css%}
            <style>
                body {
                    font-family: 'Roboto', sans-serif;
                    line-height: 1.6;
                }
                .dash-table-container {
                    border-radius: 8px;
                    overflow: hidden;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }
                .dash-spreadsheet td, .dash-spreadsheet th {
                    padding: 12px 8px !important;
                }
                .card {
                    border-radius: 8px;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                    transition: transform 0.2s;
                }
                .card:hover {
                    transform: translateY(-2px);
                }
            </style>
        </head>
        <body>
            {%app_entry%}
            <footer>
                {%config%}
                {%scripts%}
                {%renderer%}
            </footer>
        </body>
    </html>
    '''

    # Configurar aplicación
    app.config.suppress_callback_exceptions = True
    app.title = "Dashboard Calidad del Aire Chile"

    # Definir layout
    app.layout = create_app_layout()

    # Registrar todos los callbacks
    register_callbacks(app, df_air_quality, df_emissions, df_population)

    # Mostrar/ocultar leyenda AQI en móviles/tablets con JS (solo para visualización)
    app.clientside_callback(
        """
        function(n_clicks, is_open) {
            if (window.innerWidth < 992) {
                document.getElementById('aqi-legend-fab').style.display = 'block';
            } else {
                document.getElementById('aqi-legend-fab').style.display = 'none';
            }
            if (n_clicks > 0) {
                return true;
            }
            return is_open;
        }
        """,
        Output("aqi-legend-modal", "is_open"),
        [Input("aqi-legend-fab", "n_clicks")],
        [State("aqi-legend-modal", "is_open")]
    )

    # Información de inicio
    print("\n🚀 Dashboard configurado exitosamente!")
    print("📊 Funcionalidades disponibles:")
    print("   • 🗺️  Mapa interactivo de calidad del aire")
    print("   • 📈 Análisis temporal por estación")
    print("   • 🏭 Análisis de fuentes de emisión")
    print("   • 🔗 Análisis de correlaciones")

    print(f"\n🌐 Acceda al dashboard en: http://localhost:8052")
    print("💡 Presione Ctrl+C para detener el servidor")
    print("-" * 60)

    try:
        # Ejecutar servidor
        app.run_server(
            debug=True,
            port=8052,
            host='127.0.0.1',
            dev_tools_hot_reload=True,
            dev_tools_ui=True
        )
    except KeyboardInterrupt:
        print("\n\n👋 Dashboard detenido correctamente")
        print("¡Gracias por usar el Dashboard de Calidad del Aire!")
    except Exception as e:
        print(f"\n❌ Error ejecutando el dashboard: {e}")
        print("Verifique que el puerto 8052 esté disponible")

# ===== PUNTO DE ENTRADA =====

if __name__ == '__main__':
    main()
